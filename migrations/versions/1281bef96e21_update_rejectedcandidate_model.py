"""Update RejectedCandidate model

Revision ID: 1281bef96e21
Revises: cabe464aba87
Create Date: 2024-11-18 00:24:19.544275

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1281bef96e21'
down_revision = 'cabe464aba87'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('rejected_candidate', schema=None) as batch_op:
        batch_op.add_column(sa.Column('passed', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('score', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('developer_feedback', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('overall_evaluation', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('questions_asked', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('answers', sa.Text(), nullable=True))
        batch_op.drop_column('feedback')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('rejected_candidate', schema=None) as batch_op:
        batch_op.add_column(sa.Column('feedback', sa.TEXT(), nullable=True))
        batch_op.drop_column('answers')
        batch_op.drop_column('questions_asked')
        batch_op.drop_column('overall_evaluation')
        batch_op.drop_column('developer_feedback')
        batch_op.drop_column('score')
        batch_op.drop_column('passed')

    # ### end Alembic commands ###
