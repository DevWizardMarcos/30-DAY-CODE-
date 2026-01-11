"""cria tabelas users e produtos

Revision ID: 459664270afa
Revises: 
Create Date: 2026-01-11 11:48:12.889983

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# Identificadores de revisão, usados pelo Alembic
revision: str = '459664270afa'
down_revision: Union[str, Sequence[str], None] = None  # Revisão anterior (nenhuma)
branch_labels: Union[str, Sequence[str], None] = None  # Labels de branch
depends_on: Union[str, Sequence[str], None] = None  # Dependências


def upgrade() -> None:
    """Atualiza o schema do banco (aplica as mudanças)."""
    # ### Comandos gerados automaticamente pelo Alembic - ajuste se necessário! ###
    op.create_table('produtos',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('nome', sa.String(), nullable=True),
    sa.Column('preco', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_name'), 'users', ['name'], unique=False)
    # ### Fim dos comandos Alembic ###


def downgrade() -> None:
    """Reverte o schema do banco (desfaz as mudanças)."""
    # ### Comandos gerados automaticamente pelo Alembic - ajuste se necessário! ###
    op.drop_index(op.f('ix_users_name'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_table('produtos')
    # ### Fim dos comandos Alembic ###
