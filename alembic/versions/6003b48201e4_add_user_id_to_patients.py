"""add user_id to patients

Revision ID: 6003b48201e4
Revises: 
Create Date: 2026-01-21 13:06:08.882699

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '6003b48201e4'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column(
        'patients',
        sa.Column('user_id', sa.Integer(), nullable=True)
    )
    op.create_foreign_key(
        'fk_patients_user_id',
        'patients',
        'users',
        ['user_id'],
        ['id']
    )


def downgrade():
    op.drop_constraint('fk_patients_user_id', 'patients', type_='foreignkey')
    op.drop_column('patients', 'user_id')
