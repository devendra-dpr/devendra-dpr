"""added type_ column in in ReviewSugg

Revision ID: d76c9cc456e2
Revises: 49c10bcb7c0d
Create Date: 2023-11-09 14:48:43.887562

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd76c9cc456e2'
down_revision = '49c10bcb7c0d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('review_sugg', schema=None) as batch_op:
        batch_op.add_column(sa.Column('type_', sa.Enum('good', 'neutral', 'bad', name='reviewtype'), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('review_sugg', schema=None) as batch_op:
        batch_op.drop_column('type_')

    # ### end Alembic commands ###
