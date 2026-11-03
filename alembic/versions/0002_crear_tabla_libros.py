"""crear_tabla_libros"""
from alembic import op
import sqlalchemy as sa

revision = '0002'
down_revision = '0001'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'libros',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('titulo', sa.String(), nullable=False),
        sa.Column('autor', sa.String(), nullable=False),
        sa.Column('isbn', sa.String(), unique=True, nullable=False),
        sa.Column('copias_disponibles', sa.Integer(), nullable=False),
        sa.Column('estado', sa.String(), nullable=False)
    )

def downgrade():
    op.drop_table('libros')
