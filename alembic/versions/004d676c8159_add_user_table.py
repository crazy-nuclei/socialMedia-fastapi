"""Add user table

Revision ID: 004d676c8159
Revises: 896eabe7ef6f
Create Date: 2023-09-14 14:48:35.215080

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '004d676c8159'
down_revision: Union[str, None] = '896eabe7ef6f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("users", 
                    sa.Column("id", sa.Integer(), primary_key=True, nullable= False),
                    sa.Column("email", sa.String(), nullable= False, unique=True),
                    sa.Column("password", sa.String(), nullable= False),
                    sa.Column("created_at", sa.DateTime(timezone=True), nullable= False, server_default=sa.text("Now()"))
                    )
    pass


def downgrade() -> None:
    op.drop_table("users")
    pass
