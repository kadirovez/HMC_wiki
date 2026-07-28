
MEDIA_S3_TYPES = {"image", "video"}


def extract_media_keys(content: dict | list | None) -> set[str]:
    """
    Recursively collects image/video S3 keys from a JSON document.
    """
    keys: set[str] = set()

    def walk(node):
        if isinstance(node, dict):
            if node.get("type") in MEDIA_S3_TYPES:
                attrs = node.get("attr") or {}
                key = attrs.get("key")
                if key:
                    keys.add(key)
            for value in node.values():
                walk(value)
        elif isinstance(node, list):
            for item in node:
                walk(item)

    walk(content)
    return keys


def diff_orphaned_keys(
        old_content: dict | list | None,
        new_content: dict | list | None,
) -> set[str]:
    old_keys = extract_media_keys(old_content)
    new_keys = extract_media_keys(new_content)
    return old_keys - new_keys

