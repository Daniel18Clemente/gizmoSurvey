# Simple Code Explanation

## What is This Project?

This is a **Survey Management System** built with Django. Think of it like a Google Forms app specifically designed for schools where:
- **Teachers** can create surveys and assign them to students
- **Students** can take surveys and submit their answers
- **Teachers** can view results with charts and statistics

---

## How It Works (In Simple Terms)

### The Basic Flow:

1. **Teacher creates a survey** → Adds questions → Assigns it to student sections
2. **Student logs in** → Sees assigned surveys → Takes the survey
3. **Teacher views responses** → Gets charts and analytics

---

## Main Components Explained

### 1. **Models (Database Structure)** 📊

Think of models as tables in a database that store information:

- **User** - Stores username, password, name (Django's built-in)
- **UserProfile** - Adds role (student/teacher) and section to users
- **Section** - Represents a class/group (like "CS101-A")
- **Survey** - The actual survey with title, description, due date
- **Question** - Questions in a survey (multiple choice, rating scale, text answers)
- **SurveyResponse** - When a student completes a survey
- **Answer** - Individual answers to each question

### 2. **Views (What Happens on Each Page)** 🌐

Views handle the logic for each webpage:

**Student Views:**
- `student_dashboard()` - Shows surveys assigned to the student
- `take_survey()` - Displays the survey form for students to fill
- `student_history()` - Shows past survey responses

**Teacher Views:**
- `teacher_dashboard()` - Overview of all surveys and statistics
- `create_survey()` - Form to create a new survey
- `edit_survey()` - Modify survey questions
💡 **Important Feature:** When a teacher edits a survey that already has responses, the system increments the version. Students must retake the survey for the new version.

- `survey_responses()` - List of all student responses
- `survey_analytics()` - Charts showing response statistics
- `manage_students()` - View/activate/deactivate students
- `manage_sections()` - Create/manage class sections

**Authentication Views:**
- `custom_login()` - User login page
- `register()` - New user signup

### 3. **Templates (HTML Pages)** 📄

HTML files that users see in their browser. Located in `myapp/templates/myapp/`:
- `home.html` - Landing page
- `login.html` - Login form
- `student_dashboard.html` - Student's main page
- `teacher_dashboard.html` - Teacher's main page
- `take_survey.html` - Survey form for students
- Plus many more for all features

### 4. **Forms (Data Input)** 📝

Handle user input validation and data collection:
- `SurveyForm` - Create/edit survey details
- `QuestionForm` - Add/edit questions
- `SurveyResponseForm` - Dynamic form generated based on survey questions
- `SectionForm` - Create sections
- And others for various features

---

## Key Features Explained Simply

### Version Control System
**What it does:** When a teacher edits a survey that students have already completed, the version number increases (1 → 2 → 3).

**Why it matters:** 
- Old student responses stay valid for historical reference
- Students must retake the survey for the new version
- This ensures all responses match the current survey questions

**How it works:**
```python
# When survey content changes and responses exist
if content_changed and survey.responses.exists():
    survey.version += 1  # Increment version
```

### Soft Delete (Inactive Status)
**What it does:** Instead of permanently deleting questions, students, or sections, they are marked as inactive.

**Why it matters:**
- Prevents data loss
- Can restore deleted items later
- Old responses remain intact with their original questions

### Analytics & Charts
**What it does:** Automatically creates visual charts from survey responses.

**Types of charts:**
- **Pie charts** - For multiple choice questions (show percentage of each option)
- **Bar charts** - For Likert scale questions (show distribution of ratings)
- **Word clouds** - For text responses (show most common words)

**How it works:**
- Counts all answers for each question
- Calculates percentages
- Passes data to Chart.js library to create visuals

### Student Access Control
**What it does:** Students can only see and take surveys assigned to their section.

**How it works:**
```python
# Get surveys assigned to student's section
assigned_surveys = Survey.objects.filter(
    sections=profile.section,
    is_active=True
)
```

---

## Database Relationships (Simple Version)

Think of these like connections between data:

```
Teacher → Creates → Survey
Survey → Contains → Questions
Survey → Assigned to → Sections
Student → Belongs to → Section
Student → Submits → SurveyResponse
SurveyResponse → Contains → Answers
```

---

## Authentication & Security

### How Users Log In
1. Enter username and password
2. System checks credentials
3. Checks if user is active
4. Redirects to appropriate dashboard (student or teacher)

### Role-Based Access
- **Students** can only access student features
- **Teachers** can only access teacher features
- If a student tries to access teacher pages, they get an error message

### Middleware Protection
- `ActiveUserMiddleware` - Checks if user account is active before allowing access
- Automatically logs out inactive users

---

## Code Flow Examples

### Example 1: Student Takes a Survey

```
1. Student clicks "Take Survey" button
   ↓
2. `take_survey()` view loads
   ↓
3. Checks: Is survey assigned to student's section? Is it still open?
   ↓
4. Loads survey questions
   ↓
5. Generates dynamic form based on question types
   ↓
6. Student submits form
   ↓
7. Validate answers
   ↓
8. Create SurveyResponse record
   ↓
9. Save each Answer record
   ↓
10. Redirect to dashboard with success message
```

### Example 2: Teacher Creates Survey

```
1. Teacher clicks "Create Survey"
   ↓
2. Fill in title, description, sections, due date
   ↓
3. Save survey
   ↓
4. Redirect to add questions page
   ↓
5. Add questions one by one (or bulk add)
   ↓
6. Set question type, options, required status
   ↓
7. Questions saved with order numbers
   ↓
8. Survey ready! Students can now see it
```

### Example 3: Teacher Views Analytics

```
1. Teacher clicks "View Analytics" on a survey
   ↓
2. `survey_analytics()` view loads
   ↓
3. Get all responses for this survey
   ↓
4. For each question, count answers:
   - Multiple choice: Count each option choice
   - Likert scale: Count each rating value
   - Text answers: Extract word frequencies
   ↓
5. Calculate percentages
   ↓
6. Pass data to Chart.js
   ↓
7. Display beautiful charts and statistics
```

---

## Important Functions

### `get_survey_analytics_data(survey)`
**Purpose:** Prepares all chart data for a survey
**Returns:** List of dictionaries with question data, stats, and chart information

### `process_text_for_wordcloud(text_responses)`
**Purpose:** Analyzes text responses to find most common words
**Returns:** Top 50 words with their frequencies

### `handle_batch_save(request, survey, questions_data)`
**Purpose:** Allows saving multiple questions at once
**Returns:** Success status with created question count

### `generate_version_timeline_data(survey, responses_query)`
**Purpose:** Tracks response trends over time, comparing current vs old versions
**Returns:** Timeline data with response counts per day

---

## File Structure (What's What)

```
gizmoSurvey/
├── manage.py           # Django project manager
├── db.sqlite3          # Database file (stores all data)
├── myapp/
│   ├── models.py       # Database table definitions
│   ├── views.py        # Page logic (what happens on each page)
│   ├── forms.py        # Form handling
│   ├── urls.py         # URL routing (which URL goes to which view)
│   ├── admin.py        # Django admin interface configuration
│   ├── templates/      # HTML pages
│   └── static/         # CSS, JavaScript, images
└── pythonproject/
    ├── settings.py     # Project configuration
    └── urls.py         # Main URL configuration
```

---

## Technology Stack

- **Django** - Web framework (Python)
- **SQLite** - Database
- **Bootstrap 5** - Frontend styling
- **Chart.js** - Chart/graph creation
- **JavaScript** - Interactive features

---

## Key Python Concepts Used

1. **Decorators** (`@login_required`) - Restricts access to logged-in users
2. **QuerySets** - Database queries (like filtering, ordering)
3. **JSON** - Storing complex data in database (like question options)
4. **Context** - Data passed to templates to display on pages
5. **Redirects** - Sending user to different page after action
6. **Messages** - Success/error notifications shown to users

---

## Summary

This is a complete survey application where:
- Teachers create surveys with various question types
- Students answer surveys within their assigned sections
- Teachers see results in beautiful charts and can export data
- The system tracks survey versions to handle edits properly
- Access is controlled based on user roles

**The core idea:** Make surveys easy for teachers to create and analyze, while making them simple and secure for students to complete.

