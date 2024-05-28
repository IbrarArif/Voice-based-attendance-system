"""Add student_name column to Attendance model

Revision ID: 6aa944b9618e
Revises: dfedec1d4364
Create Date: 2024-05-28 10:17:24.129819

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6aa944b9618e'
down_revision = 'dfedec1d4364'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('attendance', schema=None) as batch_op:
        batch_op.add_column(sa.Column('student_name', sa.String(length=80), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('attendance', schema=None) as batch_op:
        batch_op.drop_column('student_name')

    # ### end Alembic commands ###
