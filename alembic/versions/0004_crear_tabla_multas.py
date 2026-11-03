"""crear_tabla_multas"""
from alembic import op
import sqlalchemy as sa

revision = '0004'
down_revision = '0003'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'multas',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('usuario_id', sa.Integer(), sa.ForeignKey('usuarios.id'), nullable=False),
        sa.Column('prestamo_id', sa.Integer(), sa.ForeignKey('prestamos.id'), nullable=False),
        sa.Column('monto', sa.Float(), nullable=False),
        sa.Column('pagado', sa.Boolean(), default=False)
    )

def downgrade():
    op.drop_table('multas')
