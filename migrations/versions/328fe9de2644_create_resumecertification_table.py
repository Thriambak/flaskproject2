"""Create ResumeCertification table

Revision ID: 328fe9de2644
Revises: 59cd6c602d70
Create Date: 2024-12-31 14:18:31.173457

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '328fe9de2644'
down_revision = '59cd6c602d70'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('resume_certifications', schema=None) as batch_op:
        batch_op.alter_column('resume_path',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
        batch_op.drop_column('uploaded_at')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('resume_certifications', schema=None) as batch_op:
        batch_op.add_column(sa.Column('uploaded_at', sa.DATETIME(), nullable=True))
        batch_op.alter_column('resume_path',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)

    # ### end Alembic commands ###
