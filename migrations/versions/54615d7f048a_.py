"""empty message

Revision ID: 54615d7f048a
Revises: a5cffa318ac2
Create Date: 2024-07-07 15:51:32.915825

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '54615d7f048a'
down_revision = 'a5cffa318ac2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('personaje',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(), nullable=False),
    sa.Column('descripcion', sa.Text(), nullable=True),
    sa.Column('especie', sa.String(), nullable=True),
    sa.Column('afiliacion', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('nombre')
    )
    op.create_table('planeta',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(), nullable=False),
    sa.Column('descripcion', sa.Text(), nullable=True),
    sa.Column('clima', sa.String(), nullable=True),
    sa.Column('terreno', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('nombre')
    )
    op.create_table('usuario',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=250), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('nombre', sa.String(), nullable=False),
    sa.Column('apellido', sa.String(), nullable=False),
    sa.Column('fecha_subscripcion', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('favorito',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('usuario_id', sa.Integer(), nullable=False),
    sa.Column('planeta_id', sa.Integer(), nullable=True),
    sa.Column('personaje_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['personaje_id'], ['personaje.id'], ),
    sa.ForeignKeyConstraint(['planeta_id'], ['planeta.id'], ),
    sa.ForeignKeyConstraint(['usuario_id'], ['usuario.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('user')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('usuario',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=250), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('nombre', sa.String(), nullable=False),
        sa.Column('apellido', sa.String(), nullable=False),
        sa.Column('fecha_subscripcion', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    op.drop_table('favorito')
    op.drop_table('usuario')
    op.drop_table('planeta')
    op.drop_table('personaje')
    # ### end Alembic commands ###
