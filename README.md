# HMC Wiki API — Usage Guide

This document describes how to use the HMC Wiki backend API. The API is organized into four routers:

| Router | Prefix | Purpose |
|---|---|---|
| Wiki (read) | `/wiki` | Browse wiki content — tree, pages, files |
| Admin | `/admin` | Manage users and roles |
| Redactor (nodes) | `/files` | Create / rename / delete nodes (structure) |
| Editor (content) | `/edit` | Edit file content, autosave, publish, media uploads |

All endpoints require authentication (`get_current_user` dependency). Endpoints under `/admin`, `/files`, and `/edit` additionally require the `ADMIN` role (`require_role(UserRole.ADMIN)`), since only admins can modify structure or content. Regular authenticated users can only read via `/wiki`.

---

## 1. Wiki — Read Endpoints (`/wiki`)

These endpoints are used to browse the wiki: view the home page, open a directory tree, or read a file's content. Any authenticated user (viewer or admin) can call them.

### `GET /wiki/`
Returns the home page / main menu — the top-level list of all available pages a user can navigate into.

**Response:** `list[ShortNodeResponse]` — a short representation of each root-level page (id, title, slug, type, etc.).

**Use case:** Called when the frontend first loads the wiki, to render the main navigation menu.

---

### `GET /wiki/{slug}`
Returns the full directory tree for a given page: all its sections, folders, and files, nested according to the hierarchy.

**Path parameters:**
- `slug` (str) — the slug of the page (or node) to open.

**Response:** the full node tree under that slug (sections → folders → files).

**Use case:** Called when a user navigates into a page, to render its file explorer / sidebar tree.

---

### `GET /wiki/file/{slug}`
Returns the content of a specific file, with all internal media references (image/video keys) replaced by real, temporary download links.

**Path parameters:**
- `slug` (str) — the slug of the file being requested.

**Query parameters:**
- `parent_id` (UUID) — id of the parent folder, used to disambiguate/validate the file's location in the tree.

**Response:** file content (JSON produced by the frontend editor), with media keys swapped for presigned S3 URLs.

**Use case:** Called when a user opens a file to read it. Since media is stored privately in S3, the backend generates fresh presigned links on every read so the frontend never has to handle raw storage keys.

---

## 2. Admin — User Management (`/admin`)

Used to view users and manage their permission level. All endpoints require the `ADMIN` role.

### `GET /admin/`
Returns a list of all users, for the purpose of assigning/reviewing roles.

**Query parameters:**
- `skip` (int, default `0`) — pagination offset.
- `limit` (int, default `100`) — pagination page size.

**Response:** `list[UserListResponse]` — a reduced/safe representation of each user (e.g. name, surname, id — no sensitive fields).

**Auth:** Requires `ADMIN` role.

**Use case:** Rendering a user-management table in the admin panel.

---

### `PATCH /admin/{user_id}/user_role`
Changes another user's role (e.g. promotes a viewer to admin, or demotes an admin back to viewer).

**Path parameters:**
- `user_id` (int) — id of the user whose role is being changed.

**Body:** `UserRoleUpdate` — contains the new role value.

**Auth:** Requires `ADMIN` role.

**Use case:** Granting or revoking admin/editing rights for a user from the admin panel.

---

## 3. Redactor — Node Structure (`/files`)

Used to manage the *structure* of the wiki tree — creating, renaming, and deleting nodes (pages, sections, folders, files). All endpoints require the `ADMIN` role. Editing the actual *content* of a file is handled separately by the Editor router (`/edit`).

### `POST /files/node`
Creates a new node (page, section, folder, or file). The slug is generated automatically from the title.

**Body:** `NodeCreate` — includes the node's title, type, and parent id (except for pages, which are root nodes).

**Hierarchy rule enforced server-side:**
```
PAGE   → must be a root node (no parent)
SECTION → parent must be a PAGE
FOLDER  → parent must be a SECTION or another FOLDER
FILE    → parent must be a FOLDER
```

**Auth:** Requires `ADMIN` role.

**Use case:** Adding new structure to the wiki — e.g. creating a new page, or a folder/file inside an existing section.

---

### `PATCH /files/node`
Renames a node. Only the `title` can be changed — updating the title automatically regenerates the node's `slug` (uniqueness per parent is handled internally).

**Body:** `NodeTitleUpdate` — node id + new title.

**Auth:** Requires `ADMIN` role.

**Use case:** Renaming a page/section/folder/file. Note: since the slug changes, any client-side cached URLs referencing the old slug become invalid — the frontend should refresh navigation state after a successful rename.

---

### `DELETE /files/node`
Deletes a node and **all of its descendants** (cascading delete through the whole subtree).

**Body:** `NodeDelete` — id of the node to delete.

**Auth:** Requires `ADMIN` role.

**Use case:** Removing a page, section, folder, or file — along with everything nested inside it. This is destructive and irreversible, so the frontend should confirm with the user before calling it.

---

## 4. Editor — File Content Editing (`/edit`)

Used to actually edit the content of a file. Editing happens on the frontend using custom content-builder components, which serialize the document into JSON; the backend's job here is to manage locking, autosave, publishing, and media upload URLs. All endpoints require the `ADMIN` role.

### Editing model overview
- Only **one editor at a time** can work on a given file — this is enforced via a **pessimistic lock** (an editing session), not a multi-editor / last-write-wins model.
- Before a session can be started, the frontend should call `editor-status` to check whether the file is already locked by someone else.
- Once a session is active, the frontend autosaves the draft periodically ("small save") without publishing it.
- The user explicitly publishes/commits the draft to the live file via `editor-save`.
- Images and videos are uploaded directly from the frontend to storage; the backend only issues presigned upload URLs and stores the resulting storage key inside the file's JSON content. The same keys are resolved back into readable links whenever the file is fetched for viewing (see `GET /wiki/file/{slug}` above).

---

### `GET /edit/`
Starts a new editing session for a node, or reclaims an existing session if its TTL (lock lifetime) has already expired.

**Query parameters:**
- `node_id` (UUID) — id of the file/node to start editing.

**Auth:** Requires `ADMIN` role.

**Use case:** Called when a user opens a file in edit mode. If nobody else holds an active lock (or the previous lock expired), this acquires the lock for the current user and returns whatever the session requires to begin editing (e.g. draft content, session info).

---

### `GET /edit/editor-status`
Checks whether a node is currently locked for editing — **without** acquiring the lock itself.

**Query parameters:**
- `node_id` (UUID) — id of the node to check.

**Response:** `EditorStatus` — lock state (locked/free), and presumably who holds it / until when.

**Auth:** Requires `ADMIN` role.

**Use case:** Called before entering edit mode, so the frontend can warn the user ("this file is currently being edited by X") instead of blindly starting a session.

---

### `PATCH /edit/editor`
Autosaves the current draft inside an active editing session ("small save"). This does **not** create a version snapshot and does **not** publish the change — it just persists work-in-progress.

**Body:** `SaveRequest` — the current draft content (and relevant identifiers, e.g. node id).

**Auth:** Requires `ADMIN` role.

**Use case:** Called automatically by the frontend — both after a pause in typing, and on a fixed interval (e.g. every ~10 seconds) — to make sure in-progress edits aren't lost if the browser closes unexpectedly.

---

### `PATCH /edit/editor-save`
Publishes the draft: commits it to the main/live file content, making it visible to all readers.

**Body:** `SaveRequest` — the final content to publish (and relevant identifiers, e.g. node id).

**Auth:** Requires `ADMIN` role.

**Use case:** Called when the user explicitly saves/publishes their changes (as opposed to the periodic autosave, which only affects the draft).

---

### `POST /edit/file`
Generates a presigned upload URL so the frontend can upload a file (image or video) directly to storage.

**Body:** `FilePresignedRequest` — describes the file being uploaded (e.g. content type / filename).

**Response:** a presigned upload URL (and likely the generated storage key to reference in the JSON content).

**Auth:** Requires `ADMIN` role.

**Use case:** Whenever the user inserts an image or video in the editor. The frontend uploads the raw bytes directly to storage using this URL (never through the backend), then stores the returned key inside the document's JSON. That same key is later resolved into a real, temporary download link whenever the file is read (via `GET /wiki/file/{slug}`).

---

### `DELETE /edit/editor`
Ends the editing session: releases the lock and cleans up any orphaned draft images (media that was uploaded during editing but never ended up referenced in the saved content).

**Query parameters:**
- `node_id` (UUID) — id of the node whose session is being closed.

**Auth:** Requires `ADMIN` role.

**Use case:** Called when the user closes the editor (whether or not they published their changes), so the file becomes available for someone else to edit, and unused uploaded media doesn't pile up in storage.

---

## Typical Editing Flow (End-to-End)

1. **Check availability** — `GET /edit/editor-status?node_id=...` to see if the file is free.
2. **Start session** — `GET /edit/?node_id=...` to acquire the lock and load the draft.
3. **Edit** — user works in the frontend's content builder; every few seconds or after a pause:
   `PATCH /edit/editor` with the current draft (autosave, no publish).
4. **Upload media (as needed)** — `POST /edit/file` to get a presigned upload URL; frontend uploads directly to storage and stores the returned key in the JSON content.
5. **Publish** — `PATCH /edit/editor-save` to commit the draft to the live file.
6. **Close session** — `DELETE /edit/editor?node_id=...` to release the lock and clean up orphaned media.
7. **Anyone reading the file** afterwards calls `GET /wiki/file/{slug}?parent_id=...`, which resolves all media keys into fresh, temporary download links.

---

## Notes on Media Handling

- All images and videos live in a **private** storage bucket (S3) — never public.
- The JSON content of a file only ever stores a **storage key**, never a direct/permanent link.
- **Upload:** backend issues a presigned **PUT** URL → frontend uploads bytes directly to storage → backend is never sent the raw file.
- **Read:** backend issues presigned **GET** links, generated fresh each time a file is fetched — these are injected into the content in place of the raw keys.
- **Cleanup:** orphaned media (uploaded but not referenced in the final saved content) is removed by diffing old vs. new content's media keys at save/close time — there is no separate background sweep job for this.
