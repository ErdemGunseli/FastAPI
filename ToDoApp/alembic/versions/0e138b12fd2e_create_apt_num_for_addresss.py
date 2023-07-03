"""create apt_num for addresss

Revision ID: 0e138b12fd2e
Revises: 50670a180f54
Create Date: 2023-07-03 01:36:03.918056

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0e138b12fd2e'
down_revision = '50670a180f54'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("addresses", sa.Column("apt_num", sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column("addresses", "apt_num")
