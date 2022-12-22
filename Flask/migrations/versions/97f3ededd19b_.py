"""empty message

Revision ID: 97f3ededd19b
Revises: d9cd93b093cf
Create Date: 2022-12-21 15:51:19.373447

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '97f3ededd19b'
down_revision = 'd9cd93b093cf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pet_info', schema=None) as batch_op:
        batch_op.add_column(sa.Column('petInfo_key', sa.Integer(), nullable=False))
        batch_op.drop_index('pet_birth')
        batch_op.drop_index('pet_name')
        batch_op.drop_column('id')

    with op.batch_alter_table('question', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key(None, 'user', ['user_id'], ['user_key'], ondelete='CASCADE')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('question', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('user_id')

    with op.batch_alter_table('pet_info', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False))
        batch_op.create_index('pet_name', ['pet_name'], unique=False)
        batch_op.create_index('pet_birth', ['pet_birth'], unique=False)
        batch_op.drop_column('petInfo_key')

    # ### end Alembic commands ###