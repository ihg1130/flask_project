"""empty message

Revision ID: d23804992c1f
Revises: 4c8b5d6f06e3
Create Date: 2023-05-02 20:47:29.036602

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd23804992c1f'
down_revision = '4c8b5d6f06e3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('question', schema=None) as batch_op:
        batch_op.add_column(sa.Column('file_name', sa.String(length=255), nullable=False))
        batch_op.add_column(sa.Column('file_data', sa.LargeBinary(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('question', schema=None) as batch_op:
        batch_op.drop_column('file_data')
        batch_op.drop_column('file_name')

    # ### end Alembic commands ###
