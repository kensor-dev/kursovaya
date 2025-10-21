from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = 'e8f664807402'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_table('parent',
    sa.Column('parent_id', sa.Integer(), nullable=False),
    sa.Column('full_name', sa.Text(), nullable=False),
    sa.Column('contact_info', sa.Text(), nullable=True),
    sa.Column('student_relation', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('parent_id')
    )
    op.create_index(op.f('ix_parent_parent_id'), 'parent', ['parent_id'], unique=False)
    op.create_table('teacher',
    sa.Column('teacher_id', sa.Integer(), nullable=False),
    sa.Column('full_name', sa.Text(), nullable=False),
    sa.Column('contact_info', sa.Text(), nullable=True),
    sa.Column('position', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('teacher_id')
    )
    op.create_index(op.f('ix_teacher_teacher_id'), 'teacher', ['teacher_id'], unique=False)
    op.create_table('school_class',
    sa.Column('class_id', sa.Integer(), nullable=False),
    sa.Column('number_letter', sa.Text(), nullable=False),
    sa.Column('class_teacher_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['class_teacher_id'], ['teacher.teacher_id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('class_id')
    )
    op.create_index(op.f('ix_school_class_class_id'), 'school_class', ['class_id'], unique=False)
    op.create_table('subject',
    sa.Column('subject_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Text(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('teacher_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['teacher_id'], ['teacher.teacher_id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('subject_id')
    )
    op.create_index(op.f('ix_subject_subject_id'), 'subject', ['subject_id'], unique=False)
    op.create_table('journal',
    sa.Column('journal_id', sa.Integer(), nullable=False),
    sa.Column('class_id', sa.Integer(), nullable=True),
    sa.Column('subject_id', sa.Integer(), nullable=True),
    sa.Column('grade_list', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['class_id'], ['school_class.class_id'], ),
    sa.ForeignKeyConstraint(['subject_id'], ['subject.subject_id'], ),
    sa.PrimaryKeyConstraint('journal_id')
    )
    op.create_index(op.f('ix_journal_journal_id'), 'journal', ['journal_id'], unique=False)
    op.create_table('student',
    sa.Column('student_id', sa.Integer(), nullable=False),
    sa.Column('full_name', sa.Text(), nullable=False),
    sa.Column('date_of_birth', sa.Date(), nullable=True),
    sa.Column('class_id', sa.Integer(), nullable=True),
    sa.Column('contact_info', sa.Text(), nullable=True),
    sa.Column('additional_info', sa.Text(), nullable=True),
    sa.Column('parent_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['class_id'], ['school_class.class_id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['parent_id'], ['parent.parent_id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('student_id')
    )
    op.create_index(op.f('ix_student_student_id'), 'student', ['student_id'], unique=False)
    op.create_table('grade',
    sa.Column('grade_id', sa.Integer(), nullable=False),
    sa.Column('student_id', sa.Integer(), nullable=False),
    sa.Column('subject_id', sa.Integer(), nullable=False),
    sa.Column('teacher_id', sa.Integer(), nullable=True),
    sa.Column('date_issued', sa.Date(), nullable=True),
    sa.Column('grade', sa.Float(), nullable=True),
    sa.Column('comment', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['student_id'], ['student.student_id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['subject_id'], ['subject.subject_id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['teacher_id'], ['teacher.teacher_id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('grade_id')
    )
    op.create_index(op.f('ix_grade_grade_id'), 'grade', ['grade_id'], unique=False)

def downgrade() -> None:
    op.drop_index(op.f('ix_grade_grade_id'), table_name='grade')
    op.drop_table('grade')
    op.drop_index(op.f('ix_student_student_id'), table_name='student')
    op.drop_table('student')
    op.drop_index(op.f('ix_journal_journal_id'), table_name='journal')
    op.drop_table('journal')
    op.drop_index(op.f('ix_subject_subject_id'), table_name='subject')
    op.drop_table('subject')
    op.drop_index(op.f('ix_school_class_class_id'), table_name='school_class')
    op.drop_table('school_class')
    op.drop_index(op.f('ix_teacher_teacher_id'), table_name='teacher')
    op.drop_table('teacher')
    op.drop_index(op.f('ix_parent_parent_id'), table_name='parent')
    op.drop_table('parent')
