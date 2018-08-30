"""create user info table

Revision ID: cde47f0fc00d
Revises:
Create Date: 2018-08-30 17:41:19.012801

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cde47f0fc00d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'userinfo',
        sa.Column('follow_date', sa.Date),
        sa.Column('displayname', sa.String(255)),
        sa.Column('picture_url', sa.String(255)),
        sa.Column('status_message', sa.String(255)),
        sa.Column('user_id', sa.String(255),primary_key=True)
        )

def downgrade():
    op.drop_table('userinfo')
