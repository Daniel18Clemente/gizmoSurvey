# How to Refresh Django Database

This guide explains different ways to refresh/reset your Django database.

## Understanding Database Refresh

"Refreshing" a database typically means one of these:
1. **Complete Reset**: Delete all data and recreate tables from scratch
2. **Apply Migrations**: Update database schema to match your models
3. **Clear Data Only**: Remove all data but keep the structure

---

## Method 1: Complete Database Reset (Nuclear Option)

**Use this when:** You want to start completely fresh - delete all data and recreate everything.

### Steps:

1. **Delete the database file** (SQLite):
   ```bash
   # Navigate to your project directory
   cd gizmo/gizmoSurvey
   
   # Delete the database file
   rm db.sqlite3
   # On Windows Git Bash, you can also use:
   # del db.sqlite3
   ```

2. **Delete migration files** (except `__init__.py`):
   ```bash
   # Remove all migration files except __init__.py
   rm myapp/migrations/0*.py
   ```

3. **Create new migrations**:
   ```bash
   python manage.py makemigrations
   ```

4. **Apply migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser** (optional, for admin access):
   ```bash
   python manage.py createsuperuser
   ```

---

## Method 2: Reset Without Deleting Migration Files

**Use this when:** You want to keep your migration history but reset the database.

### Steps:

1. **Delete the database file**:
   ```bash
   rm db.sqlite3
   ```

2. **Reapply all migrations**:
   ```bash
   python manage.py migrate
   ```

This recreates the database using your existing migrations.

---

## Method 3: Apply New Migrations (Incremental Update)

**Use this when:** You've changed your models and need to update the database schema.

### Steps:

1. **Create migrations for model changes**:
   ```bash
   python manage.py makemigrations
   ```

2. **Apply migrations**:
   ```bash
   python manage.py migrate
   ```

---

## Method 4: Clear All Data (Keep Structure)

**Use this when:** You want to remove all data but keep the database structure.

### Using Django Shell:

```bash
python manage.py shell
```

Then in the shell:
```python
from myapp.models import *
from django.contrib.auth.models import User

# Delete all custom app data
SurveyResponse.objects.all().delete()
Answer.objects.all().delete()
Question.objects.all().delete()
Survey.objects.all().delete()
UserProfile.objects.all().delete()
Section.objects.all().delete()

# Optional: Delete all users except superusers
User.objects.filter(is_superuser=False).delete()
```

Or use Django's `flush` command (removes all data including users):
```bash
python manage.py flush
```

---

## Method 5: Reset Specific App Only

**Use this when:** You only want to reset one app's tables.

```bash
# Fake the migrations (marks them as unapplied)
python manage.py migrate myapp zero

# Reapply migrations
python manage.py migrate myapp
```

---

## Seeding Database with Sample Data

**Use this when:** You want to populate your database with test data after resetting.

### Steps:

1. **Make sure you're in the correct directory**:
   ```bash
   cd gizmo/gizmoSurvey
   ```

2. **Run the seed command**:
   ```bash
   python manage.py create_sample_data
   ```

### What Gets Created:

The seed command creates:
- **2 Sections**: CS101-A and CS101-B (Computer Science 101 sections)
- **1 Teacher**: Dr. Jane Smith (username: `teacher1`, password: `password123`)
- **4 Students**: 
  - John Doe (username: `student1`, password: `password123`)
  - Jane Wilson (username: `student2`, password: `password123`)
  - Mike Johnson (username: `student3`, password: `password123`)
  - Sarah Brown (username: `student4`, password: `password123`)
- **1 Survey**: Course Feedback Survey with 5 questions (Likert scale, multiple choice, and text questions)

### Troubleshooting Seed Command:

**Problem**: Command not found or "Unknown command: create_sample_data"

**Solutions**:
1. **Make sure you're in the right directory**:
   ```bash
   # Navigate to your project root (where manage.py is located)
   cd gizmo/gizmoSurvey
   ```

2. **Verify the command exists**:
   ```bash
   python manage.py help create_sample_data
   ```

3. **Check that migrations are applied**:
   ```bash
   python manage.py migrate
   ```

4. **If using Windows PowerShell**, make sure you're using the full path:
   ```powershell
   cd "C:\Users\YourName\Downloads\IT-403---Project-main\gizmo\gizmoSurvey"
   python manage.py create_sample_data
   ```

**Note**: The seed command uses `get_or_create()`, so you can run it multiple times safely - it won't create duplicates.

---

## Common Commands Reference

```bash
# Check migration status
python manage.py showmigrations

# See what SQL would be executed
python manage.py sqlmigrate myapp 0001

# Check for issues
python manage.py check

# Create superuser
python manage.py createsuperuser

# Load sample data (if you have fixtures)
python manage.py loaddata fixture_name.json
```

---

## Important Notes

⚠️ **WARNING**: 
- **Always backup your database** before resetting if you have important data!
- Resetting will **delete all data** permanently
- Make sure your Django server is **not running** when deleting the database file

💡 **Tips**:
- Use `python manage.py showmigrations` to see which migrations are applied
- Check `pythonproject/settings.py` to see your database configuration
- For production databases, use proper backup/restore procedures

---

## Quick Reset Script (For Development)

If you frequently need to reset, you can create a script:

**reset_db.sh** (Linux/Mac/Git Bash):
```bash
#!/bin/bash
cd "$(dirname "$0")"
rm -f db.sqlite3
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete
python manage.py makemigrations
python manage.py migrate
python manage.py create_sample_data
python manage.py createsuperuser
```

**reset_db.bat** (Windows):
```batch
@echo off
cd /d "%~dp0"
del db.sqlite3
python manage.py migrate
python manage.py create_sample_data
python manage.py createsuperuser
```

Make executable: `chmod +x reset_db.sh` (Linux/Mac)

---

## Complete Refresh + Seed Workflow

**Full reset with sample data** (recommended for development):

```bash
# 1. Navigate to project directory
cd gizmo/gizmoSurvey

# 2. Delete the database
rm db.sqlite3          # Linux/Mac/Git Bash
# OR
del db.sqlite3          # Windows CMD
# OR
Remove-Item db.sqlite3  # PowerShell

# 3. Recreate database with migrations
python manage.py migrate

# 4. Seed with sample data
python manage.py create_sample_data

# 5. (Optional) Create admin superuser
python manage.py createsuperuser
```

**One-liner** (PowerShell):
```powershell
cd "C:\Users\Daniel Clemente\Downloads\IT-403---Project-main\gizmo\gizmoSurvey" ; Remove-Item db.sqlite3 -ErrorAction SilentlyContinue ; python manage.py migrate ; python manage.py create_sample_data
```

