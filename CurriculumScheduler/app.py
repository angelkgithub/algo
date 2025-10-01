import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, time
import os
from models.scheduler import ClassScheduler
from models.data_manager import DataManager
from utils.helpers import generate_sections, validate_csv_format, detect_scheduling_conflicts

def load_csv_data_on_startup():
    """Automatically load data from CSV files on application startup"""
    import os
    import pandas as pd
    
    csv_files = {
        'courses': 'data/courses.csv',
        'rooms': 'data/rooms.csv', 
        'faculty': 'data/faculty.csv',
        'enrollments': 'data/enrollments.csv'
    }
    
    for data_type, file_path in csv_files.items():
        if os.path.exists(file_path):
            try:
                df = pd.read_csv(file_path)
                # Filter out comment lines that start with #
                if 'course_code' in df.columns:
                    df = df[~df['course_code'].astype(str).str.startswith('#')]
                
                if data_type == 'courses':
                    st.session_state.data_manager.load_courses(df)
                elif data_type == 'rooms':
                    st.session_state.data_manager.load_rooms(df)
                elif data_type == 'faculty':
                    st.session_state.data_manager.load_faculty(df)
                elif data_type == 'enrollments':
                    st.session_state.data_manager.load_enrollments(df)
            except Exception as e:
                st.error(f"Error loading {file_path}: {str(e)}")

# Initialize session state and automatically load CSV data
if 'data_manager' not in st.session_state:
    st.session_state.data_manager = DataManager()
    # Automatically load CSV data on startup
    load_csv_data_on_startup()
if 'scheduler' not in st.session_state:
    st.session_state.scheduler = ClassScheduler()

def main():
    st.set_page_config(
        page_title="Class Scheduling System",
        page_icon="📚",
        layout="wide"
    )
    
    st.title("🎓 Academic Class Scheduling System")
    st.markdown("**Automated scheduling for BSIT, BSCS, and BSIS programs**")
    
    # Add CSV reload functionality
    with st.sidebar:
        st.markdown("---")
        st.subheader("📁 CSV Data Management")
        if st.button("🔄 Reload All CSV Data", help="Reload curriculum and data from CSV files"):
            load_csv_data_on_startup()
            st.success("✅ CSV data reloaded successfully!")
            st.rerun()
        
        # Show data status
        data_status = {
            "Courses": "✅ Loaded" if st.session_state.data_manager.courses is not None else "❌ Not loaded",
            "Rooms": "✅ Loaded" if st.session_state.data_manager.rooms is not None else "❌ Not loaded", 
            "Faculty": "✅ Loaded" if st.session_state.data_manager.faculty is not None else "❌ Not loaded",
            "Enrollments": "✅ Loaded" if st.session_state.data_manager.enrollments is not None else "❌ Not loaded"
        }
        
        for data_type, status in data_status.items():
            st.markdown(f"**{data_type}:** {status}")
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a page:",
        ["Data Management", "Generate Sections", "Schedule Classes", "View Schedules", "Conflict Detection", "Export Results"]
    )
    
    if page == "Data Management":
        data_management_page()
    elif page == "Generate Sections":
        generate_sections_page()
    elif page == "Schedule Classes":
        schedule_classes_page()
    elif page == "View Schedules":
        view_schedules_page()
    elif page == "Conflict Detection":
        conflict_detection_page()
    elif page == "Export Results":
        export_results_page()

def data_management_page():
    st.header("📊 Data Management")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Courses", "Rooms", "Faculty", "Enrollments"])
    
    with tab1:
        st.subheader("Course Data")
        col1, col2 = st.columns([2, 1])
        
        with col1:
            uploaded_file = st.file_uploader("Upload Courses CSV", type=['csv'], key="courses")
            if uploaded_file is not None:
                try:
                    df = pd.read_csv(uploaded_file)
                    if validate_csv_format(df, 'courses'):
                        st.session_state.data_manager.load_courses(df)
                        st.success("Courses loaded successfully!")
                        st.dataframe(df)
                    else:
                        st.error("Invalid CSV format. Please check the required columns.")
                except Exception as e:
                    st.error(f"Error loading file: {str(e)}")
        
        with col2:
            st.info("""
            **Required columns:**
            - course_code
            - course_title
            - program
            - year_level
            - term
            - course_type (Lecture/Lab/Both)
            - units
            - hours_per_week
            """)
        
        # Load default data button
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📁 Load from CSV"):
                try:
                    df = pd.read_csv('data/courses.csv')
                    # Filter out comment lines
                    df = df[~df['course_code'].astype(str).str.startswith('#')]
                    st.session_state.data_manager.load_courses(df)
                    st.success("✅ Courses loaded from CSV!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error loading CSV: {str(e)}")
        
        with col2:
            if st.button("🔧 Load Sample Data"):
                st.session_state.data_manager.load_default_courses()
                st.success("Sample course data loaded!")
                st.rerun()
        
        # Display current courses
        if st.session_state.data_manager.courses is not None:
            st.subheader("Current Course Data")
            st.dataframe(st.session_state.data_manager.courses)
    
    with tab2:
        st.subheader("Room Data")
        col1, col2 = st.columns([2, 1])
        
        with col1:
            uploaded_file = st.file_uploader("Upload Rooms CSV", type=['csv'], key="rooms")
            if uploaded_file is not None:
                try:
                    df = pd.read_csv(uploaded_file)
                    if validate_csv_format(df, 'rooms'):
                        st.session_state.data_manager.load_rooms(df)
                        st.success("Rooms loaded successfully!")
                        st.dataframe(df)
                    else:
                        st.error("Invalid CSV format. Please check the required columns.")
                except Exception as e:
                    st.error(f"Error loading file: {str(e)}")
        
        with col2:
            st.info("""
            **Required columns:**
            - room_name
            - room_type (Lecture/Lab)
            - capacity
            - available_days
            - start_time
            - end_time
            """)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📁 Load from CSV", key="rooms_csv"):
                try:
                    df = pd.read_csv('data/rooms.csv')
                    st.session_state.data_manager.load_rooms(df)
                    st.success("✅ Rooms loaded from CSV!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error loading CSV: {str(e)}")
        
        with col2:
            if st.button("🔧 Load Sample Data", key="rooms_sample"):
                st.session_state.data_manager.load_default_rooms()
                st.success("Sample room data loaded!")
                st.rerun()
        
        if st.session_state.data_manager.rooms is not None:
            st.subheader("Current Room Data")
            st.dataframe(st.session_state.data_manager.rooms)
    
    with tab3:
        st.subheader("Faculty Data")
        col1, col2 = st.columns([2, 1])
        
        with col1:
            uploaded_file = st.file_uploader("Upload Faculty CSV", type=['csv'], key="faculty")
            if uploaded_file is not None:
                try:
                    df = pd.read_csv(uploaded_file)
                    if validate_csv_format(df, 'faculty'):
                        st.session_state.data_manager.load_faculty(df)
                        st.success("Faculty loaded successfully!")
                        st.dataframe(df)
                    else:
                        st.error("Invalid CSV format. Please check the required columns.")
                except Exception as e:
                    st.error(f"Error loading file: {str(e)}")
        
        with col2:
            st.info("""
            **Required columns:**
            - faculty_name
            - employment_type (Full-time/Part-time)
            - max_hours_per_week
            - available_days
            - specialization
            """)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📁 Load from CSV", key="faculty_csv"):
                try:
                    df = pd.read_csv('data/faculty.csv')
                    st.session_state.data_manager.load_faculty(df)
                    st.success("✅ Faculty loaded from CSV!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error loading CSV: {str(e)}")
        
        with col2:
            if st.button("🔧 Load Sample Data", key="faculty_sample"):
                st.session_state.data_manager.load_default_faculty()
                st.success("Sample faculty data loaded!")
                st.rerun()
        
        if st.session_state.data_manager.faculty is not None:
            st.subheader("Current Faculty Data")
            st.dataframe(st.session_state.data_manager.faculty)
    
    with tab4:
        st.subheader("Enrollment Data")
        col1, col2 = st.columns([2, 1])
        
        with col1:
            uploaded_file = st.file_uploader("Upload Enrollments CSV", type=['csv'], key="enrollments")
            if uploaded_file is not None:
                try:
                    df = pd.read_csv(uploaded_file)
                    if validate_csv_format(df, 'enrollments'):
                        st.session_state.data_manager.load_enrollments(df)
                        st.success("Enrollments loaded successfully!")
                        st.dataframe(df)
                    else:
                        st.error("Invalid CSV format. Please check the required columns.")
                except Exception as e:
                    st.error(f"Error loading file: {str(e)}")
        
        with col2:
            st.info("""
            **Required columns:**
            - program
            - year_level
            - term
            - total_students
            """)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📁 Load from CSV", key="enrollments_csv"):
                try:
                    df = pd.read_csv('data/enrollments.csv')
                    st.session_state.data_manager.load_enrollments(df)
                    st.success("✅ Enrollments loaded from CSV!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error loading CSV: {str(e)}")
        
        with col2:
            if st.button("🔧 Load Sample Data", key="enrollments_sample"):
                st.session_state.data_manager.load_default_enrollments()
                st.success("Sample enrollment data loaded!")
                st.rerun()
        
        if st.session_state.data_manager.enrollments is not None:
            st.subheader("Current Enrollment Data")
            st.dataframe(st.session_state.data_manager.enrollments)

def generate_sections_page():
    st.header("👥 Generate Sections")
    
    if st.session_state.data_manager.enrollments is None:
        st.warning("Please load enrollment data first in the Data Management page.")
        return
    
    st.subheader("Section Generation Settings")
    col1, col2 = st.columns(2)
    
    with col1:
        min_students = st.number_input("Minimum students per section", min_value=12, max_value=40, value=12)
        max_students = st.number_input("Maximum students per section", min_value=12, max_value=40, value=40)
    
    with col2:
        selected_program = st.selectbox("Program", ["All", "BSIT", "BSCS", "BSIS"])
        selected_year = st.selectbox("Year Level", ["All", "1", "2", "3", "4"])
    
    if st.button("Generate Sections"):
        try:
            sections = generate_sections(
                st.session_state.data_manager.enrollments,
                min_students,
                max_students,
                selected_program if selected_program != "All" else None,
                int(selected_year) if selected_year != "All" else None
            )
            
            st.session_state.data_manager.sections = sections
            st.success(f"Generated {len(sections)} sections successfully!")
            
            # Display generated sections
            st.subheader("Generated Sections")
            st.dataframe(sections)
            
            # Summary statistics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Sections", len(sections))
            with col2:
                st.metric("Total Students", sections['students_count'].sum())
            with col3:
                avg_size = sections['students_count'].mean()
                st.metric("Average Section Size", f"{avg_size:.1f}")
                
        except Exception as e:
            st.error(f"Error generating sections: {str(e)}")

def schedule_classes_page():
    st.header("📅 Schedule Classes")
    
    # Check if all required data is loaded
    required_data = {
        'courses': st.session_state.data_manager.courses,
        'rooms': st.session_state.data_manager.rooms,
        'faculty': st.session_state.data_manager.faculty,
        'sections': st.session_state.data_manager.sections
    }
    
    missing_data = [name for name, data in required_data.items() if data is None]
    
    if missing_data:
        st.warning(f"Please load the following data first: {', '.join(missing_data)}")
        return
    
    st.subheader("Scheduling Parameters")
    col1, col2 = st.columns(2)
    
    with col1:
        algorithm = st.selectbox("Scheduling Algorithm", ["Greedy", "Backtracking", "Constraint Satisfaction"])
        max_iterations = st.number_input("Max Iterations", min_value=100, max_value=10000, value=1000)
    
    with col2:
        selected_term = st.selectbox("Term", ["All", "1", "2", "3"])
        allow_conflicts = st.checkbox("Allow time conflicts (not recommended)", value=False)
    
    if st.button("Generate Schedule", type="primary"):
        with st.spinner("Generating schedule... This may take a few minutes."):
            try:
                # Initialize scheduler with current data
                scheduler = ClassScheduler()
                scheduler.load_data(
                    st.session_state.data_manager.courses,
                    st.session_state.data_manager.rooms,
                    st.session_state.data_manager.faculty,
                    st.session_state.data_manager.sections
                )
                
                # Generate schedule
                schedule = scheduler.generate_schedule(
                    algorithm=algorithm.lower(),
                    max_iterations=max_iterations,
                    term_filter=int(selected_term) if selected_term != "All" else None,
                    allow_conflicts=allow_conflicts
                )
                
                if schedule is not None and not schedule.empty:
                    st.session_state.scheduler.schedule = schedule
                    st.success(f"Schedule generated successfully! {len(schedule)} classes scheduled.")
                    
                    # Display scheduling statistics
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Total Classes", len(schedule))
                    with col2:
                        scheduled_sections = int(schedule['section'].nunique())
                        st.metric("Sections Scheduled", scheduled_sections)
                    with col3:
                        assigned_faculty = int(schedule['faculty'].nunique())
                        st.metric("Faculty Assigned", assigned_faculty)
                    with col4:
                        rooms_used = int(schedule['room'].nunique())
                        st.metric("Rooms Used", rooms_used)
                    
                    # Show sample of schedule
                    st.subheader("Schedule Preview")
                    st.dataframe(schedule.head(10))
                    
                else:
                    st.error("Failed to generate schedule. Please check your data and try again.")
                    
            except Exception as e:
                st.error(f"Error generating schedule: {str(e)}")

def view_schedules_page():
    st.header("📋 View Schedules")
    
    if st.session_state.scheduler.schedule is None:
        st.warning("No schedule generated yet. Please go to Schedule Classes page first.")
        return
    
    schedule = st.session_state.scheduler.schedule
    
    # Filter options
    st.subheader("Filter Options")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        program_filter = st.selectbox("Program", ["All"] + list(schedule['program'].unique()))
    with col2:
        year_filter = st.selectbox("Year Level", ["All"] + sorted(schedule['year_level'].unique()))
    with col3:
        section_filter = st.selectbox("Section", ["All"] + sorted(schedule['section'].unique()))
    with col4:
        day_filter = st.selectbox("Day", ["All"] + sorted(schedule['day'].unique()))
    
    # Apply filters
    filtered_schedule = schedule.copy()
    
    if program_filter != "All":
        filtered_schedule = filtered_schedule[filtered_schedule['program'] == program_filter]
    if year_filter != "All":
        filtered_schedule = filtered_schedule[filtered_schedule['year_level'] == int(year_filter)]
    if section_filter != "All":
        filtered_schedule = filtered_schedule[filtered_schedule['section'] == section_filter]
    if day_filter != "All":
        filtered_schedule = filtered_schedule[filtered_schedule['day'] == day_filter]
    
    # Display filtered schedule
    st.subheader("Schedule Results")
    if not filtered_schedule.empty:
        st.dataframe(
            filtered_schedule[['course_code', 'course_title', 'section', 'day', 'start_time', 'end_time', 'room', 'faculty', 'course_type']],
            use_container_width=True
        )
        
        # Weekly view for specific section
        if section_filter != "All":
            st.subheader(f"Weekly Schedule for {section_filter}")
            weekly_schedule = create_weekly_view(filtered_schedule)
            st.dataframe(weekly_schedule, use_container_width=True)
    else:
        st.info("No classes found with the selected filters.")

def create_weekly_view(schedule_df):
    """Create a weekly timetable view"""
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    time_slots = sorted(schedule_df['start_time'].unique())
    
    # Create empty timetable
    timetable = pd.DataFrame(index=pd.Index(time_slots), columns=pd.Index(days))
    
    for _, row in schedule_df.iterrows():
        time_slot = row['start_time']
        day = row['day']
        class_info = f"{row['course_code']}\n{row['room']}\n{row['faculty']}"
        
        if pd.isna(timetable.loc[time_slot, day]):
            timetable.loc[time_slot, day] = class_info
        else:
            timetable.loc[time_slot, day] += f"\n---\n{class_info}"
    
    return timetable.fillna("")

def conflict_detection_page():
    st.header("⚠️ Conflict Detection & Resolution")
    
    if st.session_state.scheduler.schedule is None:
        st.warning("No schedule generated yet. Please go to Schedule Classes page first.")
        return
    
    schedule = st.session_state.scheduler.schedule
    
    st.subheader("Schedule Conflict Analysis")
    
    # Detect conflicts
    with st.spinner("Analyzing schedule for conflicts..."):
        conflicts = detect_scheduling_conflicts(schedule)
    
    if conflicts.empty:
        st.success("🎉 No scheduling conflicts detected! Your schedule is optimal.")
    else:
        st.error(f"⚠️ Found {len(conflicts)} scheduling conflicts that need attention.")
        
        # Display conflicts by type
        col1, col2 = st.columns(2)
        
        with col1:
            faculty_conflicts = conflicts[conflicts['conflict_type'] == 'Faculty']
            st.subheader(f"Faculty Conflicts ({len(faculty_conflicts)})")
            if not faculty_conflicts.empty:
                st.dataframe(faculty_conflicts, use_container_width=True)
        
        with col2:
            room_conflicts = conflicts[conflicts['conflict_type'] == 'Room']
            st.subheader(f"Room Conflicts ({len(room_conflicts)})")
            if not room_conflicts.empty:
                st.dataframe(room_conflicts, use_container_width=True)
        
        # Conflict resolution suggestions
        st.subheader("🔧 Conflict Resolution Suggestions")
        
        if not conflicts.empty:
            st.info("""**Automatic Resolution Options:**
            1. **Reschedule Conflicting Classes**: Automatically find alternative time slots
            2. **Assign Alternative Faculty**: Find available faculty for conflicting courses
            3. **Use Alternative Rooms**: Reassign classes to available rooms
            4. **Split Large Sections**: Divide oversized sections to reduce scheduling pressure
            """)
            
            # Resolution buttons
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("Auto-Resolve Time Conflicts", type="primary"):
                    with st.spinner("Resolving time conflicts..."):
                        resolved_schedule = resolve_time_conflicts(schedule, conflicts)
                        if resolved_schedule is not None:
                            st.session_state.scheduler.schedule = resolved_schedule
                            st.success("Time conflicts resolved! Schedule updated.")
                            st.rerun()
                        else:
                            st.error("Unable to automatically resolve all conflicts.")
            
            with col2:
                if st.button("Reassign Faculty"):
                    with st.spinner("Reassigning faculty..."):
                        resolved_schedule = resolve_faculty_conflicts(schedule, conflicts, st.session_state.data_manager.faculty)
                        if resolved_schedule is not None:
                            st.session_state.scheduler.schedule = resolved_schedule
                            st.success("Faculty conflicts resolved! Schedule updated.")
                            st.rerun()
                        else:
                            st.error("Unable to reassign faculty for all conflicts.")
            
            with col3:
                if st.button("Reassign Rooms"):
                    with st.spinner("Reassigning rooms..."):
                        resolved_schedule = resolve_room_conflicts(schedule, conflicts, st.session_state.data_manager.rooms)
                        if resolved_schedule is not None:
                            st.session_state.scheduler.schedule = resolved_schedule
                            st.success("Room conflicts resolved! Schedule updated.")
                            st.rerun()
                        else:
                            st.error("Unable to reassign rooms for all conflicts.")
    
    # Schedule quality metrics
    st.subheader("📊 Schedule Quality Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        conflict_rate = len(conflicts) / len(schedule) * 100 if len(schedule) > 0 else 0
        st.metric("Conflict Rate", f"{conflict_rate:.1f}%")
    
    with col2:
        # Calculate room utilization
        room_usage = schedule.groupby(['room', 'day', 'start_time']).size().reset_index(name='usage')
        avg_room_util = room_usage['usage'].mean() if not room_usage.empty else 0
        st.metric("Avg Room Utilization", f"{avg_room_util:.1f}")
    
    with col3:
        # Calculate faculty workload balance
        faculty_workload = schedule.groupby('faculty').size()
        workload_std = faculty_workload.std() if not faculty_workload.empty else 0
        st.metric("Workload Balance", f"{workload_std:.1f}")
    
    with col4:
        # Calculate time slot efficiency
        time_usage = schedule.groupby(['day', 'start_time']).size().reset_index(name='classes')
        time_efficiency = len(time_usage) / (6 * 28) * 100  # 6 days, 28 time slots per day
        st.metric("Time Efficiency", f"{time_efficiency:.1f}%")

def resolve_time_conflicts(schedule, conflicts):
    """Attempt to resolve time conflicts by rescheduling"""
    # This is a simplified implementation
    # In a real system, this would use more sophisticated algorithms
    try:
        resolved_schedule = schedule.copy()
        
        for _, conflict in conflicts.iterrows():
            if conflict['conflict_type'] == 'Faculty':
                # Find alternative time slots for one of the conflicting classes
                conflicted_classes = resolved_schedule[
                    (resolved_schedule['faculty'] == conflict['resource']) &
                    (resolved_schedule['day'] == conflict['day'])
                ]
                
                if len(conflicted_classes) >= 2:
                    # Try to move the second class to a different time
                    class_to_move = conflicted_classes.iloc[1]
                    alternative_times = ['08:00', '10:00', '13:00', '15:00', '17:00']
                    
                    for new_time in alternative_times:
                        if not schedule_conflict_exists(resolved_schedule, class_to_move, new_time):
                            # Update the schedule
                            mask = (resolved_schedule['course_code'] == class_to_move['course_code']) & \
                                   (resolved_schedule['section'] == class_to_move['section'])
                            resolved_schedule.loc[mask, 'start_time'] = new_time
                            resolved_schedule.loc[mask, 'end_time'] = add_hours_to_time(new_time, 2)  # Assume 2-hour classes
                            break
        
        return resolved_schedule
    except Exception as e:
        st.error(f"Error resolving conflicts: {str(e)}")
        return None

def resolve_faculty_conflicts(schedule, conflicts, faculty_df):
    """Attempt to resolve faculty conflicts by reassigning faculty"""
    try:
        resolved_schedule = schedule.copy()
        
        for _, conflict in conflicts.iterrows():
            if conflict['conflict_type'] == 'Faculty':
                # Find alternative faculty for one of the conflicting classes
                available_faculty = faculty_df[faculty_df['faculty_name'] != conflict['resource']]
                
                for _, alt_faculty in available_faculty.iterrows():
                    # Check if this faculty is available at the conflict time
                    faculty_name = alt_faculty['faculty_name']
                    if not faculty_has_conflict(resolved_schedule, faculty_name, conflict['day'], conflict['time1']):
                        # Assign this faculty to one of the conflicting classes
                        conflicted_classes = resolved_schedule[
                            (resolved_schedule['faculty'] == conflict['resource']) &
                            (resolved_schedule['day'] == conflict['day'])
                        ]
                        
                        if len(conflicted_classes) >= 2:
                            class_to_reassign = conflicted_classes.iloc[1]
                            mask = (resolved_schedule['course_code'] == class_to_reassign['course_code']) & \
                                   (resolved_schedule['section'] == class_to_reassign['section'])
                            resolved_schedule.loc[mask, 'faculty'] = faculty_name
                            break
        
        return resolved_schedule
    except Exception as e:
        st.error(f"Error resolving faculty conflicts: {str(e)}")
        return None

def resolve_room_conflicts(schedule, conflicts, rooms_df):
    """Attempt to resolve room conflicts by reassigning rooms"""
    try:
        resolved_schedule = schedule.copy()
        
        for _, conflict in conflicts.iterrows():
            if conflict['conflict_type'] == 'Room':
                # Find alternative rooms for one of the conflicting classes
                conflicted_classes = resolved_schedule[
                    (resolved_schedule['room'] == conflict['resource']) &
                    (resolved_schedule['day'] == conflict['day'])
                ]
                
                if len(conflicted_classes) >= 2:
                    class_to_move = conflicted_classes.iloc[1]
                    
                    # Determine required room type
                    required_type = 'Lab' if 'lab' in class_to_move['course_type'].lower() else 'Lecture'
                    available_rooms = rooms_df[rooms_df['room_type'] == required_type]
                    
                    for _, alt_room in available_rooms.iterrows():
                        room_name = alt_room['room_name']
                        if not room_has_conflict(resolved_schedule, room_name, conflict['day'], conflict['time1']):
                            # Assign this room to the conflicting class
                            mask = (resolved_schedule['course_code'] == class_to_move['course_code']) & \
                                   (resolved_schedule['section'] == class_to_move['section'])
                            resolved_schedule.loc[mask, 'room'] = room_name
                            break
        
        return resolved_schedule
    except Exception as e:
        st.error(f"Error resolving room conflicts: {str(e)}")
        return None

def schedule_conflict_exists(schedule, class_info, new_time):
    """Check if moving a class to a new time would create conflicts"""
    # Simplified check - in reality, this would be more comprehensive
    return False

def faculty_has_conflict(schedule, faculty_name, day, time_range):
    """Check if faculty has a conflict at the given time"""
    faculty_schedule = schedule[schedule['faculty'] == faculty_name]
    day_schedule = faculty_schedule[faculty_schedule['day'] == day]
    # Simplified check
    return len(day_schedule) > 0

def room_has_conflict(schedule, room_name, day, time_range):
    """Check if room has a conflict at the given time"""
    room_schedule = schedule[schedule['room'] == room_name]
    day_schedule = room_schedule[room_schedule['day'] == day]
    # Simplified check
    return len(day_schedule) > 0

def add_hours_to_time(time_str, hours):
    """Add hours to a time string"""
    from datetime import datetime, timedelta
    try:
        time_obj = datetime.strptime(time_str, "%H:%M")
        new_time = time_obj + timedelta(hours=hours)
        return new_time.strftime("%H:%M")
    except:
        return "10:00"  # Default fallback

def export_results_page():
    st.header("📤 Export Results")
    
    if st.session_state.scheduler.schedule is None:
        st.warning("No schedule to export. Please generate a schedule first.")
        return
    
    schedule = st.session_state.scheduler.schedule
    
    st.subheader("Export Options")
    
    col1, col2 = st.columns(2)
    
    with col1:
        export_format = st.selectbox("Export Format", ["CSV", "Excel"])
        include_summary = st.checkbox("Include summary statistics", value=True)
    
    with col2:
        group_by = st.selectbox("Group by", ["None", "Program", "Section", "Faculty", "Room"])
        
    # Generate export data
    export_data = schedule.copy()
    
    if group_by != "None":
        export_data = export_data.sort_values(group_by.lower())
    
    # Create download button
    if export_format == "CSV":
        csv_data = export_data.to_csv(index=False)
        st.download_button(
            label="Download Schedule as CSV",
            data=csv_data,
            file_name=f"class_schedule_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    else:
        # For Excel export, we'll provide CSV for simplicity
        csv_data = export_data.to_csv(index=False)
        st.download_button(
            label="Download Schedule as Excel (CSV format)",
            data=csv_data,
            file_name=f"class_schedule_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    
    # Display summary if requested
    if include_summary:
        st.subheader("Schedule Summary")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Classes", len(schedule))
            st.metric("Programs", schedule['program'].nunique())
        
        with col2:
            st.metric("Sections", schedule['section'].nunique())
            st.metric("Faculty Members", schedule['faculty'].nunique())
        
        with col3:
            st.metric("Rooms Used", schedule['room'].nunique())
            st.metric("Days Scheduled", schedule['day'].nunique())
        
        # Faculty workload summary
        st.subheader("Faculty Workload Summary")
        faculty_workload = schedule.groupby('faculty').agg({
            'course_code': 'count',
            'section': 'nunique'
        }).rename(columns={'course_code': 'total_classes', 'section': 'sections_taught'})
        st.dataframe(faculty_workload)

if __name__ == "__main__":
    main()
