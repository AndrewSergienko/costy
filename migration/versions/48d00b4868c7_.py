"""empty message

Revision ID: 48d00b4868c7
Revises: 8db0b3c70d3d
Create Date: 2023-06-11 17:47:49.545536

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "48d00b4868c7"
down_revision = "8db0b3c70d3d"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("limits", sa.Column("user_id", sa.Integer(), nullable=True))
    op.create_foreign_key(None, "limits", "users", ["user_id"], ["id"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "limits", type_="foreignkey")
    op.drop_column("limits", "user_id")
    # ### end Alembic commands ###
