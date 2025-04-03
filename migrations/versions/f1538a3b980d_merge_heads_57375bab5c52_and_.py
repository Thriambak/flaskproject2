"""Merge heads 57375bab5c52 and 778d7789cd7d

Revision ID: f1538a3b980d
Revises: 57375bab5c52, 778d7789cd7d
Create Date: 2025-04-02 23:17:44.080633

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f1538a3b980d'
down_revision = ('57375bab5c52', '778d7789cd7d')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
