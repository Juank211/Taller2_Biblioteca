"""crear_tabla_usuarios"""
from alembic import op
import sqlalchemy as sa

revision = '0001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'usuarios',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('nombre', sa.String(), nullable=False),
        sa.Column('email', sa.String(), unique=True, nullable=False),
        sa.Column('password_hash', sa.String(), nullable=False),
        sa.Column('rol', sa.String(), nullable=False),
        sa.Column('activo', sa.Boolean(), default=True),
        sa.Column('fecha_creacion', sa.DateTime(), server_default=sa.func.now())
    )

def downgrade():
    op.drop_table('usuarios')
