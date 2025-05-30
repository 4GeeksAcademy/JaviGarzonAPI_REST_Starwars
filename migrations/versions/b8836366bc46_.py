"""empty message

Revision ID: b8836366bc46
Revises: ac87936423a5
Create Date: 2025-03-19 10:00:02.865293

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b8836366bc46'
down_revision = 'ac87936423a5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('planet', schema=None) as batch_op:
        batch_op.add_column(sa.Column('weapons', sa.String(length=100), nullable=False))
        batch_op.add_column(sa.Column('tool', sa.String(length=100), nullable=False))
        batch_op.drop_column('Tool')
        batch_op.drop_column('Weapons')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('planet', schema=None) as batch_op:
        batch_op.add_column(sa.Column('Weapons', sa.VARCHAR(length=100), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('Tool', sa.VARCHAR(length=100), autoincrement=False, nullable=False))
        batch_op.drop_column('tool')
        batch_op.drop_column('weapons')

    # ### end Alembic commands ###
