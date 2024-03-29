"""bankapi

Revision ID: 8f0d001e35c6
Revises: 14d9cdbdf029
Create Date: 2024-03-14 19:20:38.568784

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '8f0d001e35c6'
down_revision: Union[str, None] = '14d9cdbdf029'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bankapis',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('access_data', sa.JSON(), nullable=True),
    sa.Column('updated_at', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('categories', sa.Column('mcc', sa.Integer(), nullable=True))
    op.add_column('operations', sa.Column('bank_name', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('operations', 'bank_name')
    op.drop_column('categories', 'mcc')
    op.drop_table('bankapis')
    # ### end Alembic commands ###
