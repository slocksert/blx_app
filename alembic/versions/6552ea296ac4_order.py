"""order

Revision ID: 6552ea296ac4
Revises: 58457c77acd6
Create Date: 2022-11-26 18:32:00.873944

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6552ea296ac4'
down_revision = '58457c77acd6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('order', schema=None) as batch_op:
        batch_op.add_column(sa.Column('delivery_adress', sa.String(), nullable=True))
        batch_op.drop_column('adress')

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('order', schema=None) as batch_op:
        batch_op.add_column(sa.Column('adress', sa.VARCHAR(), nullable=True))
        batch_op.drop_column('delivery_adress')

    # ### end Alembic commands ###
