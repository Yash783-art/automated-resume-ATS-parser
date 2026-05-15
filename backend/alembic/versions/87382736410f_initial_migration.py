"""initial_migration

Revision ID: 87382736410f
Revises: 
Create Date: 2026-05-14 00:39:36.344106

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '87382736410f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create Users table
    op.create_table(
        'users',
        sa.Column('clerk_id', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.PrimaryKeyConstraint('clerk_id')
    )
    op.create_index(op.f('ix_users_clerk_id'), 'users', ['clerk_id'], unique=False)
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)

    # Create Resumes table
    op.create_table(
        'resumes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=True),
        sa.Column('filename', sa.String(), nullable=True),
        sa.Column('r2_key', sa.String(), nullable=True),
        sa.Column('uploaded_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('status', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.clerk_id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('r2_key')
    )
    op.create_index(op.f('ix_resumes_id'), 'resumes', ['id'], unique=False)

    # Create ParsedResumes table
    op.create_table(
        'parsed_resumes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('resume_id', sa.Integer(), nullable=True),
        sa.Column('raw_text', sa.Text(), nullable=True),
        sa.Column('structured_json', sa.JSON(), nullable=True),
        sa.Column('parsed_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.Column('confidence_score', sa.Float(), nullable=True),
        sa.ForeignKeyConstraint(['resume_id'], ['resumes.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_parsed_resumes_id'), 'parsed_resumes', ['id'], unique=False)

    # Create JobDescriptions table
    op.create_table(
        'job_descriptions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=True),
        sa.Column('title', sa.String(), nullable=True),
        sa.Column('content', sa.Text(), nullable=True),
        sa.Column('extracted_keywords_json', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.Column('is_template', sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.clerk_id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_job_descriptions_id'), 'job_descriptions', ['id'], unique=False)

    # Create MatchResults table
    op.create_table(
        'match_results',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('resume_id', sa.Integer(), nullable=True),
        sa.Column('jd_id', sa.Integer(), nullable=True),
        sa.Column('overall_score', sa.Float(), nullable=True),
        sa.Column('skills_score', sa.Float(), nullable=True),
        sa.Column('experience_score', sa.Float(), nullable=True),
        sa.Column('education_score', sa.Float(), nullable=True),
        sa.Column('matched_keywords', sa.JSON(), nullable=True),
        sa.Column('missing_keywords', sa.JSON(), nullable=True),
        sa.Column('scored_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.ForeignKeyConstraint(['jd_id'], ['job_descriptions.id'], ),
        sa.ForeignKeyConstraint(['resume_id'], ['resumes.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('match_results')
    op.drop_index(op.f('ix_job_descriptions_id'), table_name='job_descriptions')
    op.drop_table('job_descriptions')
    op.drop_index(op.f('ix_parsed_resumes_id'), table_name='parsed_resumes')
    op.drop_table('parsed_resumes')
    op.drop_index(op.f('ix_resumes_id'), table_name='resumes')
    op.drop_table('resumes')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_index(op.f('ix_users_clerk_id'), table_name='users')
    op.drop_table('users')
