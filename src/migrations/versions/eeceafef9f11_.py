"""empty message

Revision ID: eeceafef9f11
Revises: c4103bdd1d07
Create Date: 2023-06-20 12:37:23.190915

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eeceafef9f11'
down_revision = 'c4103bdd1d07'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('book', sa.Column('status', sa.String(length=30), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('book', 'status')
    # ### end Alembic commands ###
