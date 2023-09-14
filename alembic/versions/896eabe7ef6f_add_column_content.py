"""Add column content

Revision ID: 896eabe7ef6f
Revises: 63be4ecfed4f
Create Date: 2023-09-14 14:42:38.879760

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '896eabe7ef6f'
down_revision: Union[str, None] = '63be4ecfed4f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False ))
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    pass
