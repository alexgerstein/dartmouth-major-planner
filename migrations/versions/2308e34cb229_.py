"""empty message

Revision ID: 2308e34cb229
Revises: 9c318f9462a4
Create Date: 2016-06-25 17:15:57.002889

"""

# revision identifiers, used by Alembic.
revision = '2308e34cb229'
down_revision = '9c318f9462a4'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('course', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_course_department_id'), ['department_id'], unique=False)

    with op.batch_alter_table('offering', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_offering_course_id'), ['course_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_offering_hour_id'), ['hour_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_offering_median'), ['median'], unique=False)
        batch_op.create_index(batch_op.f('ix_offering_term_id'), ['term_id'], unique=False)

    with op.batch_alter_table('plan', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_plan_user_id'), ['user_id'], unique=False)

    with op.batch_alter_table('plan_offerings', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_plan_offerings_offering_id'), ['offering_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_plan_offerings_plan_id'), ['plan_id'], unique=False)

    with op.batch_alter_table('plan_terms', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_plan_terms_plan_id'), ['plan_id'], unique=False)

    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('plan_terms', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_plan_terms_plan_id'))

    with op.batch_alter_table('plan_offerings', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_plan_offerings_plan_id'))
        batch_op.drop_index(batch_op.f('ix_plan_offerings_offering_id'))

    with op.batch_alter_table('plan', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_plan_user_id'))

    with op.batch_alter_table('offering', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_offering_term_id'))
        batch_op.drop_index(batch_op.f('ix_offering_median'))
        batch_op.drop_index(batch_op.f('ix_offering_hour_id'))
        batch_op.drop_index(batch_op.f('ix_offering_course_id'))

    with op.batch_alter_table('course', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_course_department_id'))

    ### end Alembic commands ###
