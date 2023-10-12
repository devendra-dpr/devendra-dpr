"""db table updated

Revision ID: d530288e713f
Revises: 
Create Date: 2023-10-12 11:33:19.871961

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd530288e713f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('stores',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('store_name', sa.String(), nullable=False),
    sa.Column('max_clicks', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user_clicks', schema=None) as batch_op:
        batch_op.add_column(sa.Column('store_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key("fk_store_user_click", 'stores', ['store_id'], ['id'])
        batch_op.drop_column('store_name')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_clicks', schema=None) as batch_op:
        batch_op.add_column(sa.Column('store_name', sa.VARCHAR(), nullable=False))
        batch_op.drop_constraint("fk_store_user_click", type_='foreignkey')
        batch_op.drop_column('store_id')

    op.drop_table('stores')
    # ### end Alembic commands ###
