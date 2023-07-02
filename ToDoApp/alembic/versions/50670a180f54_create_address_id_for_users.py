"""create address_id for users


Revision ID: 50670a180f54
Revises: 4870b27a963c
Create Date: 2023-07-02 23:03:19.214641

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '50670a180f54'
down_revision = '4870b27a963c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users', sa.Column('address_id', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_users_address_id',
                          # The name of the table that the foreign key is being added to:
                          source_table='users',
                          # The table in which this attribute is the primary key:
                          referent_table='addresses',
                          # Column name for the foreign key:
                          local_cols=['address_id'],
                          # The name of the primary key in the addresses table:
                          remote_cols=['id'],
                          # If an address is deleted, all users with that address will also be deleted:
                          ondelete="CASCADE")


def downgrade() -> None:
    op.drop_constraint('fk_users_address_id', table_name='users')
    op.drop_column('users', 'address_id')
