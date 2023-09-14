"""Add last few columns to post table

Revision ID: 40c12b9b2699
Revises: f8ce639ff2a6
Create Date: 2023-09-14 15:05:17.849168

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '40c12b9b2699'
down_revision: Union[str, None] = 'f8ce639ff2a6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("published", sa.Boolean, nullable=False, server_default="True"))
    op.add_column("posts", sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")))
    
    pass


def downgrade() -> None:
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
    pass
