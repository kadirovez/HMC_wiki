"""small fix

Revision ID: 0e5541fde22e
Revises: 73086c789320
Create Date: 2026-07-21 12:05:52.912544

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0e5541fde22e'
down_revision: Union[str, Sequence[str], None] = '73086c789320'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint(
        "nodes_parent_id_fkey",  
        "nodes",
        type_="foreignkey",
    )
    op.create_foreign_key(
        "nodes_parent_id_fkey",
        "nodes",
        "nodes",
        ["parent_id"],
        ["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    op.drop_constraint(
        "nodes_parent_id_fkey",
        "nodes",
        type_="foreignkey",
    )
    op.create_foreign_key(
        "nodes_parent_id_fkey",
        "nodes",
        "nodes",
        ["parent_id"],
        ["id"],
    )
