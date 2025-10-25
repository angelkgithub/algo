# scripts/check_conflicts.py
import random
import pandas as pd
from models.scheduler import ClassScheduler
from utils.helpers import detect_scheduling_conflicts

# Make behavior reproducible
random.seed(0)

# 1) Minimal courses DataFrame
courses_df = pd.DataFrame([
    {
        "course_code": "CS101",
        "course_title": "Intro to CS",
        "program": "BSCS",
        "year_level": 1,
        "term": 1,
        "course_type": "Lecture",
        "units": 3,
        "hours_per_week": 2
    },
    {
        "course_code": "CS102",
        "course_title": "Programming I",
        "program": "BSCS",
        "year_level": 1,
        "term": 1,
        "course_type": "Lecture",
        "units": 3,
        "hours_per_week": 2
    }
])

# 2) Rooms (enough rooms so scheduler can avoid conflicts)
rooms_df = pd.DataFrame([
    {"room_name": "R101", "room_type": "Lecture", "capacity": 40, "available_days": "Mon-Fri", "start_time": "07:00", "end_time": "21:00"},
    {"room_name": "R102", "room_type": "Lecture", "capacity": 40, "available_days": "Mon-Fri", "start_time": "07:00", "end_time": "21:00"},
])

# 3) Faculty (multiple faculty so scheduler can distribute)
faculty_df = pd.DataFrame([
    {"faculty_name": "Alice", "employment_type": "Full-time", "max_hours_per_week": 20, "available_days": "Mon-Fri", "specialization": "CS"},
    {"faculty_name": "Bob", "employment_type": "Full-time", "max_hours_per_week": 20, "available_days": "Mon-Fri", "specialization": "CS"},
])

# 4) Sections (one section that needs the two courses)
sections_df = pd.DataFrame([
    {"section_name": "BSCS11A", "program": "BSCS", "year_level": 1, "term": 1, "students_count": 30, "min_capacity_required": 30},
])

# 5) Run scheduler
scheduler = ClassScheduler()
scheduler.load_data(courses_df, rooms_df, faculty_df, sections_df)

schedule_df = scheduler.generate_schedule(algorithm="greedy", allow_conflicts=False)

print("Generated schedule entries:", len(schedule_df))
print(schedule_df if not schedule_df.empty else "No schedule entries generated")

# 6) Check conflicts using helper
conflicts_df = detect_scheduling_conflicts(schedule_df)

if conflicts_df.empty:
    print("PASS: No scheduling conflicts detected.")
else:
    print("FAIL: Conflicts detected:")
    print(conflicts_df.to_string(index=False))