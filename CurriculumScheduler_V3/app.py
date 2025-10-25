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
    st.set_page_config(page_title="Class Scheduling System",
                       page_icon="📚",
                       layout="wide")

    st.title("🎓 Academic Class Scheduling System")
    st.markdown("**Automated scheduling for BSIT, BSCS, and BSIS programs**")

    # Add CSV reload functionality
    with st.sidebar:
        st.markdown("---")
        st.subheader("📁 CSV Data Management")
        if st.button("🔄 Reload All CSV Data",
                     help="Reload curriculum and data from CSV files"):
            load_csv_data_on_startup()
            st.success("✅ CSV data reloaded successfully!")
            st.rerun()

        # Show data status
        data_status = {
            "Courses":
            "✅ Loaded" if st.session_state.data_manager.courses is not None
            else "❌ Not loaded",
            "Rooms":
            "✅ Loaded" if st.session_state.data_manager.rooms is not None else
            "❌ Not loaded",

            "Enrollments":
            "✅ Loaded" if st.session_state.data_manager.enrollments is not None
            else "❌ Not loaded"
        }

        for data_type, status in data_status.items():
            st.markdown(f"**{data_type}:** {status}")

    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Choose a page:", [
        "Data Management", "Generate Sections", "Schedule Classes",
        "View Schedules", "Conflict Detection", "View Rooms", "Export Results"
    ])

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
    elif page == "View Rooms":
        view_rooms_page()
    elif page == "Export Results":
        export_results_page()


def data_management_page():
    st.header("📊 Data Management")

    tab1, tab2, tab3 = st.tabs(
        ["Courses", "Rooms", "Enrollments"])

    with tab1:
        st.subheader("Course Data")
        col1, col2 = st.columns([2, 1])

        with col1:
            uploaded_file = st.file_uploader("Upload Courses CSV",
                                             type=['csv'],
                                             key="courses")
            if uploaded_file is not None:
                try:
                    df = pd.read_csv(uploaded_file)
                    if validate_csv_format(df, 'courses'):
                        st.session_state.data_manager.load_courses(df)
                        st.success("Courses loaded successfully!")
                        st.dataframe(df)
                    else:
                        st.error(
                            "Invalid CSV format. Please check the required columns."
                        )
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
            uploaded_file = st.file_uploader("Upload Rooms CSV",
                                             type=['csv'],
                                             key="rooms")
            if uploaded_file is not None:
                try:
                    df = pd.read_csv(uploaded_file)
                    if validate_csv_format(df, 'rooms'):
                        st.session_state.data_manager.load_rooms(df)
                        st.success("Rooms loaded successfully!")
                        st.dataframe(df)
                    else:
                        st.error(
                            "Invalid CSV format. Please check the required columns."
                        )
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
        st.subheader("Enrollment Data")
        col1, col2 = st.columns([2, 1])

        with col1:
            uploaded_file = st.file_uploader("Upload Enrollments CSV",
                                             type=['csv'],
                                             key="enrollments")
            if uploaded_file is not None:
                try:
                    df = pd.read_csv(uploaded_file)
                    if validate_csv_format(df, 'enrollments'):
                        st.session_state.data_manager.load_enrollments(df)
                        st.success("Enrollments loaded successfully!")
                        st.dataframe(df)
                    else:
                        st.error(
                            "Invalid CSV format. Please check the required columns."
                        )
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
        st.warning(
            "Please load enrollment data first in the Data Management page.")
        return

    st.subheader("Section Generation Settings")
    col1, col2 = st.columns(2)

    with col1:
        min_students = st.number_input("Minimum students per section",
                                       min_value=12,
                                       max_value=40,
                                       value=12)
        max_students = st.number_input("Maximum students per section",
                                       min_value=12,
                                       max_value=40,
                                       value=40)

    with col2:
        selected_program = st.selectbox("Program",
                                        ["All", "BSIT", "BSCS", "BSIS"])
        selected_year = st.selectbox("Year Level", ["All", "1", "2", "3", "4"])

    if st.button("Generate Sections"):
        try:
            sections = generate_sections(
                st.session_state.data_manager.enrollments, min_students,
                max_students,
                selected_program if selected_program != "All" else None,
                int(selected_year) if selected_year != "All" else None)

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
        'sections': st.session_state.data_manager.sections
    }

    missing_data = [
        name for name, data in required_data.items() if data is None
    ]

    if missing_data:
        st.warning(
            f"Please load the following data first: {', '.join(missing_data)}")
        return

    st.subheader("Scheduling Parameters")
    col1, col2 = st.columns(2)

    with col1:
        algorithm = st.selectbox("Scheduling Algorithm", ["Greedy"])

    with col2:
        selected_term = st.selectbox("Term", ["1", "2", "3"])
        allow_conflicts = st.checkbox("Allow time conflicts (not recommended)",
                                      value=False)

    if st.button("Generate Schedule", type="primary"):
        with st.spinner("Generating schedule... This may take a few minutes."):
            try:
                # Initialize scheduler with current data
                scheduler = ClassScheduler()
                scheduler.load_data(st.session_state.data_manager.courses,
                                    st.session_state.data_manager.rooms,
                                    st.session_state.data_manager.sections)

                # Generate schedule
                schedule = scheduler.generate_schedule(
                    algorithm=algorithm.lower(),
                    max_iterations=1000,
                    term_filter=int(selected_term),
                )

                if schedule is not None and not schedule.empty:
                    st.session_state.scheduler.schedule = schedule
                    st.success(
                        f"Schedule generated successfully! {len(schedule)} classes scheduled."
                    )

                    # Display scheduling statistics
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Total Classes", len(schedule))
                    with col2:
                        scheduled_sections = int(schedule['section'].nunique())
                        st.metric("Sections Scheduled", scheduled_sections)
                    with col4:
                        rooms_used = int(schedule['room'].nunique())
                        st.metric("Rooms Used", rooms_used)

                    # Show sample of schedule
                    st.subheader("Schedule Preview")
                    st.dataframe(schedule.head(10))

                else:
                    st.error(
                        "Failed to generate schedule. Please check your data and try again."
                    )

            except Exception as e:
                st.error(f"Error generating schedule: {str(e)}")


def view_schedules_page():
    st.header("📋 View Schedules")

    if st.session_state.scheduler.schedule is None:
        st.warning(
            "No schedule generated yet. Please go to Schedule Classes page first."
        )
        return

    schedule = st.session_state.scheduler.schedule

    # Filter options
    st.subheader("Filter Options")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        program_filter = st.selectbox("Program", ["All"] +
                                      list(schedule['program'].unique()))
    with col2:
        year_filter = st.selectbox("Year Level", ["All"] +
                                   sorted(schedule['year_level'].unique()))
    with col3:
        section_filter = st.selectbox("Section", ["All"] +
                                      sorted(schedule['section'].unique()))
    with col4:
        day_filter = st.selectbox("Day",
                                  ["All"] + sorted(schedule['day'].unique()))

    # Apply filters
    filtered_schedule = schedule.copy()

    if program_filter != "All":
        filtered_schedule = filtered_schedule[filtered_schedule['program'] ==
                                              program_filter]
    if year_filter != "All":
        filtered_schedule = filtered_schedule[filtered_schedule['year_level']
                                              == int(year_filter)]
    if section_filter != "All":
        filtered_schedule = filtered_schedule[filtered_schedule['section'] ==
                                              section_filter]
    if day_filter != "All":
        filtered_schedule = filtered_schedule[filtered_schedule['day'] ==
                                              day_filter]

    # Display filtered schedule
    st.subheader("Schedule Results")
    if not filtered_schedule.empty:
        st.dataframe(filtered_schedule[[
            'course_code', 'course_title', 'section', 'day', 'start_time',
            'end_time', 'room', 'course_type'
        ]],
                     use_container_width=True)

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
    timetable = pd.DataFrame(index=pd.Index(time_slots),
                             columns=pd.Index(days))

    for _, row in schedule_df.iterrows():
        time_slot = row['start_time']
        day = row['day']
        class_info = f"{row['course_code']}\n{row['room']}"

        if pd.isna(timetable.loc[time_slot, day]):
            timetable.loc[time_slot, day] = class_info
        else:
            timetable.loc[time_slot, day] += f"\n---\n{class_info}"

    return timetable.fillna("")


def conflict_detection_page():
    st.header("⚠️ Conflict Detection")
    
    if st.session_state.scheduler.schedule is None:
        st.warning("No schedule generated yet. Please go to Schedule Classes page first.")
        return
    
    schedule = st.session_state.scheduler.schedule
    
    st.markdown("""
    This tool checks your generated schedule for conflicts:
    - **Faculty Conflicts**: Same faculty teaching two classes at the same time
    - **Room Conflicts**: Same room booked for two classes at the same time
    """)
    
    if st.button("🔍 Check for Conflicts", type="primary"):
        with st.spinner("Analyzing schedule for conflicts..."):
            conflicts_df = detect_scheduling_conflicts(schedule)
            
            if conflicts_df.empty:
                st.success("🎉 **No conflicts detected!** Your schedule is conflict-free.")
                
                # Show summary statistics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Classes Checked", len(schedule))
                with col3:
                    st.metric("Rooms Checked", schedule['room'].nunique())
            else:
                st.error(f"⚠️ **Found {len(conflicts_df)} conflict(s)** in your schedule!")
                
                # Show conflict summary
                col2 = st.columns(2)
                with col2:
                    room_conflicts = len(conflicts_df[conflicts_df['conflict_type'] == 'Room'])
                    st.metric("Room Conflicts", room_conflicts, delta_color="inverse")
                
                # Display conflicts
                st.subheader("Conflict Details")
                
                
                # Room conflicts
                if room_conflicts > 0:
                    st.markdown("### 🏫 Room Conflicts")
                    room_conflicts_df = conflicts_df[conflicts_df['conflict_type'] == 'Room']
                    for idx, conflict in room_conflicts_df.iterrows():
                        with st.expander(f"⚠️ {conflict['resource']} - {conflict['day']}", expanded=True):
                            st.warning(f"""
                            **Room:** {conflict['resource']}  
                            **Day:** {conflict['day']}  
                            **Conflict:**
                            - Class 1: {conflict['course1']} at {conflict['time1']}
                            - Class 2: {conflict['course2']} at {conflict['time2']}
                            """)
                
                # Export conflicts
                st.subheader("Export Conflicts")
                csv_data = conflicts_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Conflict Report (CSV)",
                    data=csv_data,
                    file_name="schedule_conflicts.csv",
                    mime="text/csv"
                )


def view_rooms_page():
    st.header("🏫 View Rooms")

    if st.session_state.scheduler.schedule is None:
        st.warning(
            "No schedule generated yet. Please go to Schedule Classes page first."
        )
        return

    schedule = st.session_state.scheduler.schedule

    st.subheader("Room Utilization Overview")

    # Get unique rooms from the schedule
    available_rooms = sorted(schedule['room'].unique())

    # Filter options
    col1, col2 = st.columns(2)

    with col1:
        selected_room = st.selectbox("Select Room",
                                     ["All Rooms"] + list(available_rooms))

    with col2:
        selected_day = st.selectbox("Select Day", [
            "All Days", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
            "Saturday"
        ])

    # Room utilization statistics
    st.subheader("📊 Room Utilization Statistics")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        total_rooms = len(available_rooms)
        st.metric("Total Rooms", total_rooms)

    with col2:
        total_classes = len(schedule)
        st.metric("Total Classes Scheduled", total_classes)

    with col3:
        avg_classes_per_room = total_classes / total_rooms if total_rooms > 0 else 0
        st.metric("Avg Classes per Room", f"{avg_classes_per_room:.1f}")

    with col4:
        # Calculate overall utilization (classes scheduled / total possible slots)
        # Assuming 7 AM - 9 PM = 14 hours, 6 days = 84 hours per week per room
        max_hours_per_week = 14 * 6
        total_scheduled_hours = schedule['hours_per_week'].sum(
        ) if 'hours_per_week' in schedule.columns else len(schedule) * 2
        utilization_rate = (
            total_scheduled_hours /
            (max_hours_per_week * total_rooms)) * 100 if total_rooms > 0 else 0
        st.metric("Overall Utilization", f"{utilization_rate:.1f}%")

    # Display room schedules
    st.subheader("📅 Room Schedules")

    if selected_room == "All Rooms":
        # Show all rooms
        for room in available_rooms:
            with st.expander(f"📍 {room}", expanded=False):
                room_schedule = schedule[schedule['room'] == room].copy()

                if selected_day != "All Days":
                    room_schedule = room_schedule[room_schedule['day'] ==
                                                  selected_day]

                if not room_schedule.empty:
                    # Create a weekly timetable for this room
                    room_timetable = create_room_timetable(room_schedule)
                    st.dataframe(room_timetable, use_container_width=True)

                    # Show class count
                    st.caption(f"Total classes: {len(room_schedule)}")
                else:
                    st.info(f"No classes scheduled for this room" +
                            (f" on {selected_day}" if selected_day !=
                             "All Days" else ""))
    else:
        # Show selected room
        room_schedule = schedule[schedule['room'] == selected_room].copy()

        if selected_day != "All Days":
            room_schedule = room_schedule[room_schedule['day'] == selected_day]

        if not room_schedule.empty:
            # Create a weekly timetable for this room
            st.subheader(f"Weekly Schedule for {selected_room}")
            room_timetable = create_room_timetable(room_schedule)
            st.dataframe(room_timetable, use_container_width=True, height=600)

            # Show detailed class list
            st.subheader("Class Details")

            # Sort by day and time
            room_schedule_sorted = room_schedule.sort_values(
                ['day', 'start_time'])

            # Display as a formatted table
            display_columns = [
                'day', 'start_time', 'end_time', 'course_code', 'course_title',
                'section', 'course_type'
            ]
            available_columns = [
                col for col in display_columns
                if col in room_schedule_sorted.columns
            ]
            st.dataframe(room_schedule_sorted[available_columns],
                         use_container_width=True)

            st.caption(f"Total classes: {len(room_schedule)}")
        else:
            st.info(f"No classes scheduled for {selected_room}" + (
                f" on {selected_day}" if selected_day != "All Days" else ""))


def create_room_timetable(room_schedule_df):
    """Create a weekly timetable view for a room showing 7:00 AM - 9:00 PM"""
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

    # Generate all time slots from 7:00 AM to 9:00 PM
    time_slots = []
    for hour in range(7, 21):  # 7 AM to 9 PM
        time_slots.append(f"{hour:02d}:00")
        time_slots.append(f"{hour:02d}:30")

    # Create empty timetable
    timetable = pd.DataFrame(index=pd.Index(time_slots, name='Time'),
                             columns=pd.Index(days))
    timetable = timetable.fillna("")

    # Fill in the scheduled classes
    for _, row in room_schedule_df.iterrows():
        start_time = row['start_time']
        day = row['day']

        # Format class information
        course_info = f"{row['course_code']}"
        if 'section' in row:
            course_info += f"\n{row['section']}"
        if 'course_type' in row:
            course_info += f"\n({row['course_type']})"
        if 'start_time' in row and 'end_time' in row:
            course_info += f"\n{row['start_time']} - {row['end_time']}"

        # Find the matching time slot
        if start_time in timetable.index and day in timetable.columns:
            if timetable.loc[start_time, day] == "":
                timetable.loc[start_time, day] = course_info
            else:
                # If there's already a class, append (conflict indicator)
                timetable.loc[start_time, day] += f"\n---\n{course_info}"

    return timetable


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
        group_by = st.selectbox(
            "Group by", ["None", "Program", "Section", "Room"])

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
            file_name=
            f"class_schedule_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv")
    else:
        # For Excel export, we'll provide CSV for simplicity
        csv_data = export_data.to_csv(index=False)
        st.download_button(
            label="Download Schedule as Excel (CSV format)",
            data=csv_data,
            file_name=
            f"class_schedule_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv")

    # Display summary if requested
    if include_summary:
        st.subheader("Schedule Summary")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total Classes", len(schedule))
            st.metric("Programs", schedule['program'].nunique())

        with col2:
            st.metric("Sections", schedule['section'].nunique())

        with col3:
            st.metric("Rooms Used", schedule['room'].nunique())
            st.metric("Days Scheduled", schedule['day'].nunique())



if __name__ == "__main__":
    main()
