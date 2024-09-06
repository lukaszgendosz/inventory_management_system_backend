"""empty message

Revision ID: 575c7c1f67cf
Revises: 16ba75ab93a4
Create Date: 2024-08-30 21:52:43.691488

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '575c7c1f67cf'
down_revision: Union[str, None] = '16ba75ab93a4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'tokens', ['id'])
    op.drop_column('tokens', 'is_refresh')
    op.drop_column('tokens', 'exp')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tokens', sa.Column('exp', postgresql.TIMESTAMP(), autoincrement=False, nullable=False))
    op.add_column('tokens', sa.Column('is_refresh', sa.BOOLEAN(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'tokens', type_='unique')
    # ### end Alembic commands ###
