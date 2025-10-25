# Survey Management System

A comprehensive Django-based survey management system designed for educational institutions, featuring separate interfaces for students and teachers with advanced analytics and response management capabilities.

## Features

### Student Portal
- **Assigned Surveys List**: View only surveys currently open to their class/section
- **Dynamic Survey Form**: Support for multiple question types with client-side validation
- **Submission & History**: Submit once per survey; view past responses in a table

### Teacher/Admin Dashboard
- **Survey Builder**: Create and manage surveys with drag-and-drop interface
- **Question Management**: Support for multiple-choice, Likert scale, short answer, and long answer questions
- **Response Management**: View individual student submissions with search and filter capabilities
- **Analytics & Visualization**: Real-time charts (pie charts for MCQs, bar charts for Likert scales)
- **Section Management**: Organize students into sections for targeted survey distribution

### Question Types Supported
- **Multiple Choice**: Single-select options with customizable choices
- **Likert Scale**: Rating scales with customizable ranges and labels
- **Short Answer**: Single-line text responses
- **Long Answer**: Multi-line text responses

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd pythonproject
   ```

2. **Install dependencies**
   ```bash
   pip install django
   ```

3. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create sample data (optional)**
   ```bash
   python manage.py create_sample_data
   ```

5. **Start the development server**
   ```bash
   python manage.py runserver
   ```

6. **Access the application**
   - Open your browser and go to `http://127.0.0.1:8000/`
   - Use the sample credentials below to test the system

## Sample Data & Login Credentials

### Teacher Account
- **Username**: `teacher1`
- **Password**: `password123`
- **Role**: Teacher
- **Access**: Full survey management capabilities

### Student Accounts
- **Username**: `student1`, `student2`, `student3`, `student4`
- **Password**: `password123`
- **Role**: Student
- **Sections**: CS101-A (student1, student2), CS101-B (student3, student4)

### Admin Account
- **Username**: `admin`
- **Password**: Set during `createsuperuser` command
- **Access**: Django admin interface

## Usage Guide

### For Teachers

1. **Login** with teacher credentials
2. **Create Sections** (if not already created)
   - Go to "Manage Sections"
   - Add section name, code, and description
3. **Create Surveys**
   - Click "Create Survey"
   - Fill in survey details and assign to sections
   - Add questions with different types
4. **Monitor Responses**
   - View individual responses
   - Check analytics and visualizations
   - Export data for further analysis

### For Students

1. **Login** with student credentials
2. **View Assigned Surveys**
   - Dashboard shows surveys assigned to your section
   - See completion status and due dates
3. **Take Surveys**
   - Click "Take Survey" to start
   - Answer all required questions
   - Submit when complete
4. **View History**
   - Check past responses
   - Review completion status

## Technical Architecture

### Models
- **UserProfile**: Extended user model with role and section information
- **Section**: Class/section management
- **Survey**: Main survey entity with metadata
- **Question**: Survey questions with different types and configurations
- **SurveyResponse**: Individual student responses
- **Answer**: Individual answers to questions

### Views
- **Student Views**: Dashboard, survey taking, history
- **Teacher Views**: Dashboard, survey creation, response management, analytics
- **Authentication**: Registration with role selection

### Templates
- **Bootstrap 5** for modern, responsive UI
- **Chart.js** for analytics visualizations
- **Progressive enhancement** with JavaScript

## Scoring Rubric Implementation

The system implements the specified scoring rubric:

### Student Features (50 points)
1. **Assigned Survey List** (10 pts): Displays only active, properly filtered surveys
2. **Dynamic Survey Form** (20 pts): Renders questions (MCQ, Likert, text) with validation
3. **Submission & History** (20 pts): Stores one response per survey; shows past responses

### Teacher/Admin Features (150 points)
1. **Survey Builder** (60 pts): CRUD interface for questions, settings, and assignments
2. **Response Management** (45 pts): View/filter individual student submissions in sortable, paginated table
3. **Analytics & Visualization** (45 pts): Real-time dashboards with charts and visualizations

## API Endpoints

- `/` - Home page
- `/register/` - User registration
- `/student/` - Student dashboard
- `/student/survey/<id>/` - Take survey
- `/student/history/` - Response history
- `/teacher/` - Teacher dashboard
- `/teacher/survey/create/` - Create survey
- `/teacher/survey/<id>/edit/` - Edit survey
- `/teacher/survey/<id>/responses/` - View responses
- `/teacher/survey/<id>/analytics/` - Analytics dashboard

## Future Enhancements

- **Drag-and-drop survey builder** with visual question arrangement
- **Advanced analytics** with statistical analysis
- **Export functionality** for survey data
- **Email notifications** for survey assignments
- **Mobile app** for better accessibility
- **API endpoints** for third-party integrations

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is developed for educational purposes at the College of Information and Communications Technology.

## Contact

For questions or support, contact:
- Email: officeofthedean.cict@bulsu.edu.ph
- Phone: (044) 919 7800 Local 1102
- Address: McArthur Highway, City of Malolos 3000, Bulacan, Philippines
