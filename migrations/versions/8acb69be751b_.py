"""empty message

Revision ID: 8acb69be751b
Revises: 30cf1f58f76a
Create Date: 2023-06-10 23:43:38.407355

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8acb69be751b'
down_revision = '30cf1f58f76a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('chumo', schema=None) as batch_op:
        batch_op.alter_column('content',
               existing_type=sa.TEXT(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('chumo', schema=None) as batch_op:
        batch_op.alter_column('content',
               existing_type=sa.TEXT(),
               nullable=False)

    # ### end Alembic commands ###
