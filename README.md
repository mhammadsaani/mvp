# Teacher-Student Platform

A Django-based online platform connecting students with teachers based on their requirements.

## Features

### Student Module
- Students can post requirements about the type of teacher they are looking for
- Student contact information is hidden by default
- Only 10 teachers can bid initially on a job post
- If requirements are not met, students can request more teachers (5 per cycle)
- Students can search for teacher profiles and contact them directly
- Students can view teacher timetables once confirmed

### Teacher Module
- Teachers are created by admin (cannot register directly)
- Teachers can create descriptive profiles with expertise, experience, and rates
- Teachers can upload certifications to their profile
- Teachers can buy coins to contact students
- Free contact for top 5 teachers if job post is less than 5 minutes old
- Similarity index threshold of 60% required to bid on jobs
- Teachers can create timetables with class details

### Admin Module
- Full control over the platform
- Can create teacher profiles
- Can remove job posts and teacher profiles
- Can block students and teachers
- Can manage teacher certifications and coins

## Installation

1. Clone the repository:
```
git clone https://github.com/yourusername/teacherstudent.git
cd teacherstudent
```

2. Create a virtual environment and activate it:
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```
pip install -r requirements.txt
```

4. Apply migrations:
```
python manage.py migrate
```

5. Create a superuser:
```
python manage.py createsuperuser
```

6. Run the development server:
```
python manage.py runserver
```

## Usage

1. Access the admin panel at `/admin` to create teacher accounts
2. Students can register directly on the platform
3. Students can post job requirements and search for teachers
4. Teachers can bid on student job posts if their similarity index is above 60%
5. Admin can manage all aspects of the platform

## Technologies Used

- Django 5.2
- Bootstrap 5
- SQLite (development) / PostgreSQL (production)
- JavaScript
- HTML/CSS

## License

This project is licensed under the MIT License - see the LICENSE file for details.