from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from myapp.models import UserProfile, Section, Survey, Question


class Command(BaseCommand):
    help = 'Create sample data for testing the survey system'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Create sections
        section1, created = Section.objects.get_or_create(
            code='CS101-A',
            defaults={
                'name': 'Computer Science 101 - Section A',
                'description': 'Introduction to Computer Science - Morning Section'
            }
        )
        
        section2, created = Section.objects.get_or_create(
            code='CS101-B',
            defaults={
                'name': 'Computer Science 101 - Section B',
                'description': 'Introduction to Computer Science - Afternoon Section'
            }
        )
        
        # Create teacher
        teacher, created = User.objects.get_or_create(
            username='teacher1',
            defaults={
                'first_name': 'Dr. Jane',
                'last_name': 'Smith',
                'email': 'jane.smith@university.edu'
            }
        )
        if created:
            teacher.set_password('password123')
            teacher.save()
            
        teacher_profile, created = UserProfile.objects.get_or_create(
            user=teacher,
            defaults={
                'role': 'teacher'
            }
        )
        
        # Create students
        students_data = [
            ('student1', 'John', 'Doe', 'john.doe@student.edu', 'CS101-A', 'S001'),
            ('student2', 'Jane', 'Wilson', 'jane.wilson@student.edu', 'CS101-A', 'S002'),
            ('student3', 'Mike', 'Johnson', 'mike.johnson@student.edu', 'CS101-B', 'S003'),
            ('student4', 'Sarah', 'Brown', 'sarah.brown@student.edu', 'CS101-B', 'S004'),
        ]
        
        for username, first_name, last_name, email, section_code, student_id in students_data:
            student, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email
                }
            )
            if created:
                student.set_password('password123')
                student.save()
                
            section = Section.objects.get(code=section_code)
            UserProfile.objects.get_or_create(
                user=student,
                defaults={
                    'role': 'student',
                    'section': section,
                    'student_id': student_id
                }
            )
        
        # Create sample survey
        survey, created = Survey.objects.get_or_create(
            title='Course Feedback Survey',
            defaults={
                'description': 'Please provide your feedback about the course content, instructor, and overall experience.',
                'created_by': teacher,
                'due_date': timezone.now() + timedelta(days=7),
                'is_active': True
            }
        )
        
        if created:
            survey.sections.add(section1, section2)
            
            # Create questions
            questions_data = [
                {
                    'question_text': 'How would you rate the overall course content?',
                    'question_type': 'likert_scale',
                    'likert_min': 1,
                    'likert_max': 5,
                    'likert_labels': ['Poor', 'Fair', 'Good', 'Very Good', 'Excellent'],
                    'is_required': True,
                    'order': 1
                },
                {
                    'question_text': 'Which topics did you find most interesting?',
                    'question_type': 'multiple_choice',
                    'options': ['Programming', 'Algorithms', 'Data Structures', 'Software Engineering'],
                    'is_required': True,
                    'order': 2
                },
                {
                    'question_text': 'How many hours per week did you spend on this course?',
                    'question_type': 'multiple_choice',
                    'options': ['1-5 hours', '6-10 hours', '11-15 hours', '16+ hours'],
                    'is_required': True,
                    'order': 3
                },
                {
                    'question_text': 'What suggestions do you have for improving the course?',
                    'question_type': 'long_answer',
                    'is_required': False,
                    'order': 4
                },
                {
                    'question_text': 'Would you recommend this course to other students?',
                    'question_type': 'multiple_choice',
                    'options': ['Yes', 'No', 'Maybe'],
                    'is_required': True,
                    'order': 5
                }
            ]
            
            for q_data in questions_data:
                Question.objects.create(survey=survey, **q_data)
        
        self.stdout.write(
            self.style.SUCCESS('Sample data created successfully!')
        )
        self.stdout.write('Created:')
        self.stdout.write(f'- 2 Sections: {section1.name}, {section2.name}')
        self.stdout.write(f'- 1 Teacher: {teacher.get_full_name()}')
        self.stdout.write(f'- 4 Students: John Doe, Jane Wilson, Mike Johnson, Sarah Brown')
        self.stdout.write(f'- 1 Survey: {survey.title} with 5 questions')
        self.stdout.write('')
        self.stdout.write('Login credentials:')
        self.stdout.write('Teacher: username=teacher1, password=password123')
        self.stdout.write('Students: username=student1-4, password=password123')
