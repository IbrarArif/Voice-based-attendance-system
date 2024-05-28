"""Add teacher_name column to Course model

Revision ID: 2e12d2d5131c
Revises: 6aa944b9618e
Create Date: 2024-05-28 10:39:47.483107

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2e12d2d5131c'
down_revision = '6aa944b9618e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('course', schema=None) as batch_op:
        batch_op.add_column(sa.Column('teacher_name', sa.String(length=80), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('course', schema=None) as batch_op:
        batch_op.drop_column('teacher_name')

    # ### end Alembic commands ###
