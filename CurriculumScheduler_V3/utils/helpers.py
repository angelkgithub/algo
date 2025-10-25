import pandas as pd
import numpy as np
from typing import Optional, List, Dict

def validate_csv_format(df: pd.DataFrame, data_type: str) -> bool:
    """Validate CSV format based on data type"""
    required_columns = {
        'courses': ['course_code', 'course_title', 'program', 'year_level', 'term', 'course_type', 'units', 'hours_per_week'],
        'rooms': ['room_name', 'room_type', 'capacity', 'available_days', 'start_time', 'end_time'],
        'enrollments': ['program', 'year_level', 'term', 'total_students']
    }
    
    if data_type not in required_columns:
        return False
    
    missing_columns = [col for col in required_columns[data_type] if col not in df.columns]
    return len(missing_columns) == 0

def generate_sections(enrollments_df: pd.DataFrame, min_students: int = 12, max_students: int = 40, 
                     program_filter: Optional[str] = None, year_filter: Optional[int] = None) -> pd.DataFrame:
    """Generate sections based on enrollment data"""
    sections_list = []
    
    # Filter enrollments if specified
    filtered_enrollments = enrollments_df.copy()
    if program_filter:
        filtered_enrollments = filtered_enrollments[filtered_enrollments['program'] == program_filter]
    if year_filter:
        filtered_enrollments = filtered_enrollments[filtered_enrollments['year_level'] == year_filter]
    
    # Track last used section letters for each program-year combination
    last_section_letter = {}
    
    for _, enrollment_row in filtered_enrollments.iterrows():
        program = enrollment_row['program']
        year_level = enrollment_row['year_level']
        term = enrollment_row['term']
        total_students = enrollment_row['total_students']
        
        if total_students == 0:
            continue
        
        # Generate sections for this enrollment
        remaining_students = total_students
        section_counter = 0
        
        while remaining_students > 0:
            # Determine number of students for this section
            if remaining_students <= max_students:
                students_in_section = remaining_students
            else:
                # Try to balance sections
                num_remaining_sections = (remaining_students - 1) // max_students + 1
                students_in_section = min(max_students, 
                                        max(min_students, remaining_students // num_remaining_sections))
            
            # Generate section name
            section_letter = chr(ord('A') + section_counter)
            section_name = f"{program}{year_level}{section_letter}"
            
            # Add section to list
            sections_list.append({
                'section_name': section_name,
                'program': program,
                'year_level': year_level,
                'term': term,
                'students_count': students_in_section,
                'min_capacity_required': students_in_section
            })
            
            remaining_students -= students_in_section
            section_counter += 1
    
    return pd.DataFrame(sections_list)

def get_next_section_letter(program: str, year_level: int, last_section_tracker: Dict) -> str:
    """Get the next available section letter for a program-year combination"""
    key = (program, year_level)
    if key not in last_section_tracker:
        last_section_tracker[key] = 'A'
        return 'A'
    else:
        next_letter = chr(ord(last_section_tracker[key]) + 1)
        last_section_tracker[key] = next_letter
        return next_letter

def calculate_room_utilization(schedule_df: pd.DataFrame) -> pd.DataFrame:
    """Calculate room utilization from schedule"""
    if schedule_df.empty:
        return pd.DataFrame()
    
    room_utilization = schedule_df.groupby('room').agg({
        'course_code': 'count',
        'section': 'nunique',
        'day': lambda x: len(set(x))  # Number of different days used
    })
    room_utilization.columns = ['total_classes', 'sections_served', 'days_utilized']
    
    return room_utilization

def detect_scheduling_conflicts(schedule_df: pd.DataFrame) -> pd.DataFrame:
    """Detect scheduling conflicts in the generated schedule"""
    conflicts = []
    
    if schedule_df.empty:
        return pd.DataFrame()
    
    # Check for room conflicts
    for room in schedule_df['room'].unique():
        room_schedule = schedule_df[schedule_df['room'] == room]
        
        for idx1, row1 in room_schedule.iterrows():
            for idx2, row2 in room_schedule.iterrows():
                if int(idx1) >= int(idx2):  # Avoid duplicate checks
                    continue
                
                if (row1['day'] == row2['day'] and 
                    times_overlap(str(row1['start_time']), str(row1['end_time']), 
                                str(row2['start_time']), str(row2['end_time']))):
                    conflicts.append({
                        'conflict_type': 'Room',
                        'resource': room,
                        'day': row1['day'],
                        'time1': f"{row1['start_time']}-{row1['end_time']}",
                        'time2': f"{row2['start_time']}-{row2['end_time']}",
                        'course1': f"{row1['course_code']} ({row1['section']})",
                        'course2': f"{row2['course_code']} ({row2['section']})"
                    })
    
    return pd.DataFrame(conflicts)

def times_overlap(start1: str, end1: str, start2: str, end2: str) -> bool:
    """Check if two time periods overlap"""
    try:
        from datetime import datetime
        
        start1_dt = datetime.strptime(start1, "%H:%M").time()
        end1_dt = datetime.strptime(end1, "%H:%M").time()
        start2_dt = datetime.strptime(start2, "%H:%M").time()
        end2_dt = datetime.strptime(end2, "%H:%M").time()
        
        return not (end1_dt <= start2_dt or end2_dt <= start1_dt)
    except:
        return False

def export_schedule_to_csv(schedule_df: pd.DataFrame, filename: str = "schedule.csv") -> str:
    """Export schedule to CSV format"""
    if schedule_df.empty:
        return ""
    
    return schedule_df.to_csv(index=False)

def generate_weekly_timetable(schedule_df: pd.DataFrame, section_name: str) -> pd.DataFrame:
    """Generate a weekly timetable for a specific section"""
    if schedule_df.empty:
        return pd.DataFrame()
    
    section_schedule = schedule_df[schedule_df['section'] == section_name]
    
    if section_schedule.empty:
        return pd.DataFrame()
    
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    time_slots = sorted(section_schedule['start_time'].drop_duplicates().tolist())
    
    # Create empty timetable
    timetable = pd.DataFrame(index=pd.Index(time_slots), columns=pd.Index(days))
    
    for _, row in section_schedule.iterrows():
        time_slot = row['start_time']
        day = row['day']
        class_info = f"{row['course_code']}\n{row['room']}"
        
        if pd.isna(timetable.loc[time_slot, day]):
            timetable.loc[time_slot, day] = class_info
        else:
            timetable.loc[time_slot, day] += f"\n---\n{class_info}"
    
    return timetable.fillna("")
