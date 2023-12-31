"""empty message

Revision ID: 326324af66fa
Revises: 3e5ec0f87408
Create Date: 2023-06-21 08:35:46.953254

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '326324af66fa'
down_revision = '3e5ec0f87408'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('book_loan_ticket', 'time_lend',
               existing_type=postgresql.TIMESTAMP(),
               type_=sa.String(length=80),
               nullable=True)
    op.alter_column('book_loan_ticket', 'return_date',
               existing_type=postgresql.TIMESTAMP(),
               type_=sa.String(length=80),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('book_loan_ticket', 'return_date',
               existing_type=sa.String(length=80),
               type_=postgresql.TIMESTAMP(),
               existing_nullable=True)
    op.alter_column('book_loan_ticket', 'time_lend',
               existing_type=sa.String(length=80),
               type_=postgresql.TIMESTAMP(),
               nullable=False)
    # ### end Alembic commands ###
