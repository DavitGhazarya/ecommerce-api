"""fix user role enum

Revision ID: de21ecc6fb16
Revises: 5331be05d4da
Create Date: 2026-07-24 23:01:18.426108

"""

from alembic import op


revision = 'de21ecc6fb16'
down_revision = '5331be05d4da'
branch_labels = None
depends_on = None


def upgrade() -> None:

    op.execute(
        "ALTER TYPE user_role ADD VALUE IF NOT EXISTS 'seller'"
    )

    op.execute(
        "ALTER TYPE user_role ADD VALUE IF NOT EXISTS 'user'"
    )

    op.execute(
        "ALTER TYPE user_role ADD VALUE IF NOT EXISTS 'admin'"
    )


def downgrade() -> None:
    pass