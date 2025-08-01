"""split models and add question/response

Revision ID: 04d8dad75204
Revises: edf12d09bae5
Create Date: 2025-08-02 11:59:06.103308

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '04d8dad75204'
down_revision = 'edf12d09bae5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password_hash', sa.String(), nullable=False),
    sa.Column('role', sa.Enum('admin', 'enumerator', 'participant', name='userrole'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_users_email'), ['email'], unique=True)
        batch_op.create_index(batch_op.f('ix_users_id'), ['id'], unique=False)

    op.create_table('surveys',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('survey_type', sa.String(length=50), nullable=True),
    sa.Column('nss_template_type', sa.String(length=50), nullable=True),
    sa.Column('languages', sa.JSON(), nullable=True),
    sa.Column('adaptive_enabled', sa.Boolean(), nullable=True),
    sa.Column('voice_enabled', sa.Boolean(), nullable=True),
    sa.Column('status', sa.String(length=50), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('surveys', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_surveys_id'), ['id'], unique=False)

    op.create_table('enumerator_assignments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('enumerator_id', sa.Integer(), nullable=True),
    sa.Column('survey_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['enumerator_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['survey_id'], ['surveys.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('enumerator_assignments', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_enumerator_assignments_id'), ['id'], unique=False)

    op.create_table('questions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('survey_id', sa.Integer(), nullable=True),
    sa.Column('question_text', sa.Text(), nullable=False),
    sa.Column('question_type', sa.String(length=50), nullable=True),
    sa.Column('options', sa.JSON(), nullable=True),
    sa.Column('validation_rules', sa.JSON(), nullable=True),
    sa.Column('order_index', sa.Integer(), nullable=True),
    sa.Column('is_mandatory', sa.Boolean(), nullable=True),
    sa.Column('translations', sa.JSON(), nullable=True),
    sa.Column('nss_code', sa.String(length=50), nullable=True),
    sa.Column('lgd_location_type', sa.String(length=50), nullable=True),
    sa.ForeignKeyConstraint(['survey_id'], ['surveys.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('questions', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_questions_id'), ['id'], unique=False)

    op.create_table('responses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('survey_id', sa.Integer(), nullable=True),
    sa.Column('question_id', sa.Integer(), nullable=True),
    sa.Column('respondent_id', sa.String(length=100), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('answer', sa.JSON(), nullable=True),
    sa.Column('confidence_score', sa.Integer(), nullable=True),
    sa.Column('validation_status', sa.String(length=50), nullable=True),
    sa.Column('extra_metadata', sa.JSON(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.ForeignKeyConstraint(['question_id'], ['questions.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['survey_id'], ['surveys.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('responses', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_responses_id'), ['id'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('responses', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_responses_id'))

    op.drop_table('responses')
    with op.batch_alter_table('questions', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_questions_id'))

    op.drop_table('questions')
    with op.batch_alter_table('enumerator_assignments', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_enumerator_assignments_id'))

    op.drop_table('enumerator_assignments')
    with op.batch_alter_table('surveys', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_surveys_id'))

    op.drop_table('surveys')
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_users_id'))
        batch_op.drop_index(batch_op.f('ix_users_email'))

    op.drop_table('users')
    # ### end Alembic commands ###
