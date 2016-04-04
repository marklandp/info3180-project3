"""empty message

Revision ID: 127ff5f3e92c
Revises: ce28a6bd886b
Create Date: 2016-04-02 02:52:45.596723

"""

# revision identifiers, used by Alembic.
revision = '127ff5f3e92c'
down_revision = 'ce28a6bd886b'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('wishes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=180), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.Column('thumbnail', sa.String(length=255), nullable=True),
    sa.Column('user', sa.Integer(), nullable=True),
    sa.Column('url', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['user'], ['user_info.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('wishes')
    ### end Alembic commands ###