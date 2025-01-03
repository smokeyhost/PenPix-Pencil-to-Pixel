"""Create class model

Revision ID: 7ff86cc83b6f
Revises: e2e011db9539
Create Date: 2024-11-13 21:25:00.043230

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7ff86cc83b6f'
down_revision = 'e2e011db9539'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.add_column(sa.Column('class_id', sa.String(length=36), nullable=False))
        batch_op.create_foreign_key(None, 'class', ['class_id'], ['id'])
        batch_op.drop_column('class_schedule')
        batch_op.drop_column('class_group')

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('profile_image')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('profile_image', sa.BLOB(), nullable=True))

    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.add_column(sa.Column('class_group', sa.VARCHAR(length=100), nullable=False))
        batch_op.add_column(sa.Column('class_schedule', sa.VARCHAR(length=100), nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('class_id')

    # ### end Alembic commands ###
