"""empty message

Revision ID: c4103bdd1d07
Revises: 
Create Date: 2023-06-20 11:10:41.842432

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c4103bdd1d07'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('author',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=False),
    sa.Column('gender', sa.String(length=50), nullable=True),
    sa.Column('country', sa.String(length=80), nullable=True),
    sa.Column('books_in_lib', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('patron',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('date_of_birth', sa.String(length=80), nullable=True),
    sa.Column('gender', sa.String(length=20), nullable=True),
    sa.Column('address', sa.String(length=120), nullable=True),
    sa.Column('books_borrowed', sa.Integer(), nullable=True),
    sa.Column('membership_time', sa.String(length=120), nullable=True),
    sa.Column('books_borrowing', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('book',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=200), nullable=False),
    sa.Column('author', sa.String(length=120), nullable=True),
    sa.Column('numbers_in_stock', sa.Integer(), nullable=True),
    sa.Column('add_date', sa.String(length=120), nullable=True),
    sa.Column('days_for_borrow', sa.Integer(), nullable=False),
    sa.Column('genres', sa.String(length=120), nullable=True),
    sa.Column('pages', sa.Integer(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['author_id'], ['author.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('book_lend',
    sa.Column('id', sa.Integer(), nullable=True),
    sa.Column('book_id', sa.Integer(), nullable=False),
    sa.Column('patron_id', sa.Integer(), nullable=False),
    sa.Column('time_lend', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['book_id'], ['book.id'], ),
    sa.ForeignKeyConstraint(['patron_id'], ['patron.id'], ),
    sa.PrimaryKeyConstraint('book_id', 'patron_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('book_lend')
    op.drop_table('book')
    op.drop_table('patron')
    op.drop_table('author')
    # ### end Alembic commands ###
