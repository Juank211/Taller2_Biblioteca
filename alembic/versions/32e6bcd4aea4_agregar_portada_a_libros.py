"""
Agregar columnas para portada de libros

Revision ID: 32e6bcd4aea4
Revisión: Agregar portada_url y portada_public_id a la tabla libros
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = '32e6bcd4aea4'
down_revision = '0005_crear_tabla_lista_negra_tokens'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('libros', sa.Column('portada_url', sa.String(), nullable=True))
    op.add_column('libros', sa.Column('portada_public_id', sa.String(), nullable=True))


def downgrade():
    op.drop_column('libros', 'portada_url')
    op.drop_column('libros', 'portada_public_id')