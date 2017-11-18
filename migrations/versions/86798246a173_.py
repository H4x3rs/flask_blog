"""empty message

Revision ID: 86798246a173
Revises: 4747fa988243
Create Date: 2017-11-09 20:35:16.669194

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '86798246a173'
down_revision = '4747fa988243'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('roles',
    sa.Column('id', sa.String(length=50), nullable=False),
    sa.Column('role', sa.String(length=150), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('role')
    )
    op.create_table('users_roles',
    sa.Column('user_id', sa.String(length=50), nullable=True),
    sa.Column('role_id', sa.String(length=50), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], )
    )
    op.drop_column(u'comments', 'email')
    op.drop_column(u'comments', 'name')
    op.create_unique_constraint(None, 'users', ['email'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.add_column(u'comments', sa.Column('name', mysql.VARCHAR(length=150), nullable=False))
    op.add_column(u'comments', sa.Column('email', mysql.VARCHAR(length=150), nullable=False))
    op.drop_table('users_roles')
    op.drop_table('roles')
    # ### end Alembic commands ###