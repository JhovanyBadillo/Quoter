"""datos_completos field added to model Usuario

Revision ID: a31d6258de94
Revises: 10e5979ce350
Create Date: 2020-05-24 18:03:05.236560

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a31d6258de94'
down_revision = '10e5979ce350'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('usuarios', sa.Column('datos_completos', sa.String(length=1), nullable=True, default='N'))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('usuarios', 'datos_completos')
    # ### end Alembic commands ###
