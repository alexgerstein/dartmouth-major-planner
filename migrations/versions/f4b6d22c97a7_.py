"""empty message

Revision ID: f4b6d22c97a7
Revises: 2308e34cb229
Create Date: 2016-06-25 22:06:23.396492

"""

# revision identifiers, used by Alembic.
revision = 'f4b6d22c97a7'
down_revision = '2308e34cb229'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('last_paid', sa.Date(), nullable=True))
        batch_op.drop_column('last_paid_at')

    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('last_paid_at', sa.DATE(), nullable=True))
        batch_op.drop_column('last_paid')

    ### end Alembic commands ###