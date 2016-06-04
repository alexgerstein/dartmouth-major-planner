"""empty message

Revision ID: 9c318f9462a4
Revises: 39306d04feb7
Create Date: 2016-06-04 14:46:47.973242

"""

# revision identifiers, used by Alembic.
revision = '9c318f9462a4'
down_revision = '39306d04feb7'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('plan', schema=None) as batch_op:
        batch_op.add_column(sa.Column('fifth_year', sa.Boolean(), nullable=True))

    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('plan', schema=None) as batch_op:
        batch_op.drop_column('fifth_year')

    ### end Alembic commands ###
