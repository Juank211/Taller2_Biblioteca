"""crear_tabla_lista_negra_tokens"""
from alembic import op
import sqlalchemy as sa

revision = '0005'
down_revision = '0004'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'lista_negra_tokens',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('jti', sa.String(), unique=True, nullable=False),
        sa.Column('expiracion', sa.DateTime(), nullable=False),
        sa.Column('fecha_revocacion', sa.DateTime(), server_default=sa.func.now())
    )

def downgrade():
    op.drop_table('lista_negra_tokens')
