"""Create ResumeCertification table

Revision ID: 0d131e9f142b
Revises: 328fe9de2644
Create Date: 2024-12-31 14:20:50.673128

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0d131e9f142b'
down_revision = '328fe9de2644'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('resume_certifications', schema=None) as batch_op:
        batch_op.add_column(sa.Column('uploaded_at', sa.DateTime(), nullable=True))
        batch_op.alter_column('resume_path',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('resume_certifications', schema=None) as batch_op:
        batch_op.alter_column('resume_path',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
        batch_op.drop_column('uploaded_at')

    # ### end Alembic commands ###