"""Creating phone number for user table column

Revision ID: d75505400e6d
Revises: 
Create Date: 2025-12-12 22:47:37.468906

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd75505400e6d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('contact_numb', sa.String, nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'contact_numb')
