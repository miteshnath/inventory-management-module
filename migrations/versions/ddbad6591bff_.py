"""empty message

Revision ID: ddbad6591bff
Revises: 55cddcd4abd0
Create Date: 2020-09-11 04:19:38.971808

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ddbad6591bff'
down_revision = '55cddcd4abd0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('roles', 'dp')
    op.drop_constraint('users_public_id_key', 'users', type_='unique')
    op.drop_column('users', 'public_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('public_id', sa.VARCHAR(length=100), autoincrement=False, nullable=True))
    op.create_unique_constraint('users_public_id_key', 'users', ['public_id'])
    op.add_column('roles', sa.Column('dp', sa.VARCHAR(length=120), autoincrement=False, nullable=True))
    # ### end Alembic commands ###