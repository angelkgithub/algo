# tests/test_scheduler_conflicts.py
import random
import pandas as pd
from models.scheduler import ClassScheduler
from utils.helpers import detect_scheduling_conflicts

def test_greedy_schedule_has_no_conflicts():
    random.seed(0)

    courses_df = pd.DataFrame([
        {"course_code": "CS101", "course_title": "Intro to CS", "program": "BSCS", "year_level": 1, "term": 1, "course_type": "Lecture", "units": 3, "hours_per_week": 2},
        {"course_code": "CS102", "course_title": "Programming I", "program": "BSCS", "year_level": 1, "term": 1, "course_type": "Lecture", "units": 3, "hours_per_week": 2},
    ])

    rooms_df = pd.DataFrame([
        {"room_name": "R101", "room_type": "Lecture", "capacity": 40, "available_days": "Mon-Fri", "start_time": "07:00", "end_time": "21:00"},
        {"room_name": "R102", "room_type": "Lecture", "capacity": 40, "available_days": "Mon-Fri", "start_time": "07:00", "end_time": "21:00"},
    ])

    faculty_df = pd.DataFrame([
        {"faculty_name": "Alice", "employment_type": "Full-time", "max_hours_per_week": 20, "available_days": "Mon-Fri", "specialization": "CS"},
        {"faculty_name": "Bob", "employment_type": "Full-time", "max_hours_per_week": 20, "available_days": "Mon-Fri", "specialization": "CS"},
    ])

    sections_df = pd.DataFrame([
        {"section_name": "BSCS11A", "program": "BSCS", "year_level": 1, "term": 1, "students_count": 30, "min_capacity_required": 30},
    ])

    scheduler = ClassScheduler()
    scheduler.load_data(courses_df, rooms_df, faculty_df, sections_df)

    schedule_df = scheduler.generate_schedule(algorithm="greedy", allow_conflicts=False)

    # Sanity: a schedule should be generated for these inputs
    assert not schedule_df.empty, "Scheduler produced no entries for simple test data"

    conflicts_df = detect_scheduling_conflicts(schedule_df)

    # Assert no conflicts found
    assert conflicts_df.empty, f"Found conflicts:\n{conflicts_df.to_string(index=False)}"