"""crear_tabla_prestamos"""
from alembic import op
import sqlalchemy as sa

revision = '0003'
down_revision = '0002'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'prestamos',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('usuario_id', sa.Integer(), sa.ForeignKey('usuarios.id'), nullable=False),
        sa.Column('libro_id', sa.Integer(), sa.ForeignKey('libros.id'), nullable=False),
        sa.Column('fecha_prestamo', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('fecha_devuelto', sa.DateTime(), nullable=True),
        sa.Column('estado', sa.String(), nullable=False)
    )

def downgrade():
    op.drop_table('prestamos')
