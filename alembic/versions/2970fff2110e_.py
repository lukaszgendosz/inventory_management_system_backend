"""empty message

Revision ID: 2970fff2110e
Revises: 6612b0bdabee
Create Date: 2024-09-28 22:04:33.798640

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2970fff2110e'
down_revision: Union[str, None] = '6612b0bdabee'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('assets', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_unique_constraint(None, 'assets', ['id'])
    op.create_foreign_key(None, 'assets', 'users', ['user_id'], ['id'])
    op.create_unique_constraint(None, 'categories', ['id'])
    op.create_unique_constraint(None, 'manufacturers', ['id'])
    op.create_unique_constraint(None, 'models', ['id'])
    op.create_unique_constraint(None, 'suppliers', ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'suppliers', type_='unique')
    op.drop_constraint(None, 'models', type_='unique')
    op.drop_constraint(None, 'manufacturers', type_='unique')
    op.drop_constraint(None, 'categories', type_='unique')
    op.drop_constraint(None, 'assets', type_='foreignkey')
    op.drop_constraint(None, 'assets', type_='unique')
    op.drop_column('assets', 'user_id')
    # ### end Alembic commands ###
