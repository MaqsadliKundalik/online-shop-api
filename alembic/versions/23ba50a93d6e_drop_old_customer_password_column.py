"""drop_old_customer_password_column

Revision ID: 23ba50a93d6e
Revises: b4c2a9e1418d
Create Date: 2026-01-16 16:34:17.953612

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '23ba50a93d6e'
down_revision: Union[str, Sequence[str], None] = 'b4c2a9e1418d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
