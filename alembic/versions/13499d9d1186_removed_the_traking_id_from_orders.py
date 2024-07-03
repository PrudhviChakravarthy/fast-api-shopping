"""removed the traking id from orders

Revision ID: 13499d9d1186
Revises: 1cf82a2065a9
Create Date: 2024-07-02 18:14:14.737424

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '13499d9d1186'
down_revision: Union[str, None] = '1cf82a2065a9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('orders', 'tracking_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('orders', sa.Column('tracking_id', sa.UUID(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###