"""create address table

Revision ID: 4870b27a963c
Revises: ee0643ff1d4f
Create Date: 2023-07-02 22:31:41.030389

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4870b27a963c'
down_revision = 'ee0643ff1d4f'
branch_labels = None
depends_on = None

# If we open up the previous migration file, we can see that there down_revision is set to None.
# Notice that for this file, down_revision is set to the revision number of the previous file.
# down_revision specifies the revision ID of the previous migration that this migration depends on.
# It represents the order in which the migrations should be applied or rolled back.
# For our case, since the 2 migrations are independent, we could set down_revision to None.


def upgrade() -> None:
    # Creating the addresses table:
    op.create_table("addresses", sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
                    sa.Column("address1", sa.String(), nullable=False),
                    sa.Column("address2", sa.String(), nullable=False),
                    sa.Column("city", sa.String(), nullable=False),
                    sa.Column("state", sa.String(), nullable=False),
                    sa.Column("country", sa.String(), nullable=False),
                    sa.Column("postal_code", sa.String(), nullable=False)
                    # Could also set the primary key this way:
                    # sa.PrimaryKeyConstraint("id")
                    )


def downgrade() -> None:
    # Reversing the migration changes:
    op.drop_table("address")
