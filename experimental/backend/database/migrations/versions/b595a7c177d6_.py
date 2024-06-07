"""empty message

Revision ID: b595a7c177d6
Revises: 516f55fb3e43
Create Date: 2024-06-07 19:31:38.954458

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b595a7c177d6'
down_revision = '516f55fb3e43'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('skill', sa.UnicodeText(), nullable=True))
        batch_op.drop_column('skills')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('skills', sa.TEXT(), nullable=True))
        batch_op.drop_column('skill')

    # ### end Alembic commands ###
