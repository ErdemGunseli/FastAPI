"""create phone number for user col

Revision ID: ee0643ff1d4f
Revises: 
Create Date: 2023-07-02 21:19:43.989027

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'ee0643ff1d4f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Adding the SQL to create a new phone number column:
    # First argument is the table name, second is the column name, third is the column type.
    op.add_column('users', sa.Column('phone_number', sa.String(length=20), nullable=True))

    # Now, to upgrade, run the following command:
    # alembic upgrade <revision#>
    # In this case the revision number is ee0643ff1d4f


def downgrade() -> None:
    # Adding the SQL to drop the phone number column - reverse the migration
    # First argument is the table name, second is the column name.
    op.drop_column('users', 'phone_number')

    # Now, to downgrade, run the following command:
    # alembic downgrade <revision#>
    # or
    # alembic downgrade -1
