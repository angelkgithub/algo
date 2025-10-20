import pandas as pd
import numpy as np
from datetime import datetime, time, timedelta
import random
from typing import Dict, List, Optional, Tuple

class ClassScheduler:
    def __init__(self):
        self.courses = None
        self.rooms = None
        self.faculty = None
        self.sections = None
        self.schedule = None
        
        # Time slots (7:00 AM to 9:00 PM)
        self.time_slots = self._generate_time_slots()
        self.days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        
        # Track day pairing usage for even distribution
        self.day_pairing_counter = 0
        
    def _generate_time_slots(self):
        """Generate available time slots"""
        slots = []
        start_hour = 7  # 7:00 AM
        end_hour = 21   # 9:00 PM
        
        for hour in range(start_hour, end_hour):
            for minute in [0, 30]:  # 30-minute intervals
                if hour < end_hour or (hour == end_hour and minute == 0):
                    time_str = f"{hour:02d}:{minute:02d}"
                    slots.append(time_str)
        return slots
    
    def load_data(self, courses_df, rooms_df, faculty_df, sections_df):
        """Load all required data for scheduling"""
        self.courses = courses_df.copy()
        self.rooms = rooms_df.copy()
        self.faculty = faculty_df.copy()
        self.sections = sections_df.copy()
        
    def generate_schedule(self, algorithm="greedy", max_iterations=1000, term_filter=None, allow_conflicts=False):
        """Main method to generate class schedule"""
        if any(data is None for data in [self.courses, self.rooms, self.faculty, self.sections]):
            raise ValueError("All data (courses, rooms, faculty, sections) must be loaded first")
        
        # Filter courses by term if specified
        if self.courses is None:
            raise ValueError("Courses data not loaded")
        courses_to_schedule = self.courses.copy()
        if term_filter:
            courses_to_schedule = courses_to_schedule[courses_to_schedule['term'] == term_filter]
        
        if algorithm == "greedy":
            return self._greedy_scheduling(courses_to_schedule, allow_conflicts)
        elif algorithm == "backtracking":
            return self._backtracking_scheduling(courses_to_schedule, max_iterations, allow_conflicts)
        elif algorithm == "constraint satisfaction":
            return self._constraint_satisfaction_scheduling(courses_to_schedule, max_iterations, allow_conflicts)
        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")
    
    def _greedy_scheduling(self, courses_to_schedule, allow_conflicts=False):
        """Greedy scheduling algorithm"""
        schedule_list = []
        faculty_schedule = {}  # Track faculty assignments
        room_schedule = {}     # Track room assignments
        section_schedule = {}  # Track section assignments
        
        # Initialize tracking dictionaries
        if self.faculty is None or self.rooms is None:
            raise ValueError("Faculty or rooms data not loaded")
        for faculty_name in self.faculty['faculty_name']:
            faculty_schedule[faculty_name] = {}
        
        for room_name in self.rooms['room_name']:
            room_schedule[room_name] = {}
        
        # Process each section
        if self.sections is None:
            raise ValueError("Sections data not loaded")
        for _, section_row in self.sections.iterrows():
            section_name = section_row['section_name']
            program = section_row['program']
            year_level = section_row['year_level']
            term = section_row['term']
            
            section_schedule[section_name] = {}
            
            # Get courses for this section
            section_courses = courses_to_schedule[
                (courses_to_schedule['program'] == program) &
                (courses_to_schedule['year_level'] == year_level) &
                (courses_to_schedule['term'] == term)
            ]
            
            # Schedule each course for this section
            for _, course_row in section_courses.iterrows():
                assigned = self._assign_course_to_section(
                    course_row, section_row, schedule_list,
                    faculty_schedule, room_schedule, section_schedule,
                    allow_conflicts
                )
                
                if not assigned and not allow_conflicts:
                    print(f"Warning: Could not schedule {course_row['course_code']} for {section_name}")
        
        # Convert to DataFrame
        if schedule_list:
            schedule_df = pd.DataFrame(schedule_list)
            return schedule_df
        else:
            return pd.DataFrame()
    
    def _assign_course_to_section(self, course_row, section_row, schedule_list, 
                                faculty_schedule, room_schedule, section_schedule, allow_conflicts):
        """Assign a single course to a section"""
        course_code = course_row['course_code']
        course_title = course_row['course_title']
        course_type = course_row['course_type']
        hours_per_week = course_row['hours_per_week']
        section_name = section_row['section_name']
        
        # Determine required room type
        required_room_type = 'Lab' if 'lab' in course_type.lower() else 'Lecture'
        
        # Find suitable faculty
        suitable_faculty = self._find_suitable_faculty(course_row)
        if suitable_faculty.empty:
            return False
        
        # Find suitable rooms
        if self.rooms is None:
            return False
        suitable_rooms = self.rooms[self.rooms['room_type'] == required_room_type]
        if suitable_rooms.empty:
            return False
        
        # Determine scheduling pattern based on course type and hours
        if course_type.lower() == 'both':
            # Handle lecture + lab courses
            return self._schedule_lecture_lab_course(
                course_row, section_row, schedule_list,
                faculty_schedule, room_schedule, section_schedule,
                suitable_faculty, allow_conflicts
            )
        else:
            # Handle pure lecture or pure lab courses
            return self._schedule_single_type_course(
                course_row, section_row, schedule_list,
                faculty_schedule, room_schedule, section_schedule,
                suitable_faculty, suitable_rooms, allow_conflicts
            )
    
    def _schedule_lecture_lab_course(self, course_row, section_row, schedule_list,
                                   faculty_schedule, room_schedule, section_schedule,
                                   suitable_faculty, allow_conflicts):
        """Schedule a course that has both lecture and lab components"""
        section_name = section_row['section_name']
        hours_per_week = course_row['hours_per_week']
        
        # Split hours between lecture and lab (e.g., 6 hours = 3 lecture + 3 lab)
        lecture_hours = hours_per_week // 2
        lab_hours = hours_per_week - lecture_hours
        
        # Schedule lecture component
        if self.rooms is None:
            return False
        lecture_rooms = self.rooms[self.rooms['room_type'] == 'Lecture']
        lecture_assigned = self._schedule_course_component(
            course_row, section_row, 'Lecture', lecture_hours, schedule_list,
            faculty_schedule, room_schedule, section_schedule,
            suitable_faculty, lecture_rooms, allow_conflicts
        )
        
        if not lecture_assigned and not allow_conflicts:
            return False
        
        # Schedule lab component
        if self.rooms is None:
            return False
        lab_rooms = self.rooms[self.rooms['room_type'] == 'Lab']
        lab_assigned = self._schedule_course_component(
            course_row, section_row, 'Lab', lab_hours, schedule_list,
            faculty_schedule, room_schedule, section_schedule,
            suitable_faculty, lab_rooms, allow_conflicts
        )
        
        return lecture_assigned and lab_assigned
    
    def _schedule_single_type_course(self, course_row, section_row, schedule_list,
                                   faculty_schedule, room_schedule, section_schedule,
                                   suitable_faculty, suitable_rooms, allow_conflicts):
        """Schedule a course that is purely lecture or purely lab"""
        hours_per_week = course_row['hours_per_week']
        course_type = 'Lecture' if 'lecture' in course_row['course_type'].lower() else 'Lab'
        
        return self._schedule_course_component(
            course_row, section_row, course_type, hours_per_week, schedule_list,
            faculty_schedule, room_schedule, section_schedule,
            suitable_faculty, suitable_rooms, allow_conflicts
        )
    
    def _schedule_course_component(self, course_row, section_row, component_type, hours,
                                 schedule_list, faculty_schedule, room_schedule, section_schedule,
                                 suitable_faculty, suitable_rooms, allow_conflicts):
        """Schedule a specific component of a course (lecture or lab)"""
        section_name = section_row['section_name']
        course_code = course_row['course_code']
        course_title = course_row['course_title']
        
        # Determine time patterns based on hours and component type
        time_patterns = self._get_time_patterns(hours, component_type)
        
        for pattern in time_patterns:
            # Try to find a suitable assignment
            for _, faculty_row in suitable_faculty.iterrows():
                faculty_name = faculty_row['faculty_name']
                
                for _, room_row in suitable_rooms.iterrows():
                    room_name = room_row['room_name']
                    
                    # Try to schedule this pattern
                    if self._can_assign_pattern(
                        pattern, faculty_name, room_name, section_name,
                        faculty_schedule, room_schedule, section_schedule, allow_conflicts
                    ):
                        # Make the assignment
                        self._make_assignment(
                            pattern, course_row, section_row, faculty_name, room_name,
                            component_type, schedule_list, faculty_schedule,
                            room_schedule, section_schedule
                        )
                        return True
        
        return False
    
    def _get_time_patterns(self, hours, component_type='Lecture'):
        """Generate possible time patterns for given hours with specific day pairings"""
        patterns = []
        
        # Define preferred day pairings for two-session courses
        base_day_pairings = [
            ('Monday', 'Thursday'),
            ('Tuesday', 'Friday'),
            ('Wednesday', 'Saturday')
        ]
        
        # Rotate day pairings to distribute courses evenly across the week
        # Each successfully scheduled course component will use a different day pairing first
        rotation = self.day_pairing_counter % 3
        day_pairings = base_day_pairings[rotation:] + base_day_pairings[:rotation]
        
        # For lab classes with 2 hours or more, always split across two days
        # For lecture classes, split if 2-4 hours
        should_split = (component_type == 'Lab' and hours >= 2) or (hours > 2 and hours <= 4)
        
        if hours <= 2 and not should_split:
            # Single session patterns for very short classes (1 hour lectures)
            for day in self.days:
                for start_time in self.time_slots[:-4]:
                    end_time = self._add_hours_to_time(start_time, hours)
                    if end_time in self.time_slots:
                        patterns.append([{
                            'day': day,
                            'start_time': start_time,
                            'end_time': end_time,
                            'duration': hours
                        }])
        
        elif hours == 2 and component_type == 'Lab':
            # Split 2-hour labs into two 1-hour sessions
            session_hours = 1
            
            for day1, day2 in day_pairings:
                for start_time in self.time_slots[:-2]:
                    end_time = self._add_hours_to_time(start_time, session_hours)
                    if end_time in self.time_slots:
                        patterns.append([
                            {
                                'day': day1,
                                'start_time': start_time,
                                'end_time': end_time,
                                'duration': session_hours
                            },
                            {
                                'day': day2,
                                'start_time': start_time,
                                'end_time': end_time,
                                'duration': session_hours
                            }
                        ])
        
        elif hours <= 4:
            # Split into 2 balanced sessions using specific day pairings
            session_hours = hours / 2
            slots_needed = int(session_hours * 2)
            
            for day1, day2 in day_pairings:
                for start_time in self.time_slots[:-slots_needed if slots_needed > 0 else -1]:
                    end_time = self._add_hours_to_time(start_time, session_hours)
                    if end_time in self.time_slots:
                        patterns.append([
                            {
                                'day': day1,
                                'start_time': start_time,
                                'end_time': end_time,
                                'duration': session_hours
                            },
                            {
                                'day': day2,
                                'start_time': start_time,
                                'end_time': end_time,
                                'duration': session_hours
                            }
                        ])
        
        else:
            # For longer courses (>4 hours), split into 2 balanced sessions across specific day pairs
            session_hours = hours / 2
            slots_needed = int(session_hours * 2)
            
            for day1, day2 in day_pairings:
                for start_time in self.time_slots[:-slots_needed if slots_needed > 0 else -1]:
                    end_time = self._add_hours_to_time(start_time, session_hours)
                    if end_time in self.time_slots:
                        patterns.append([
                            {
                                'day': day1,
                                'start_time': start_time,
                                'end_time': end_time,
                                'duration': session_hours
                            },
                            {
                                'day': day2,
                                'start_time': start_time,
                                'end_time': end_time,
                                'duration': session_hours
                            }
                        ])
        
        return patterns
    
    def _get_day_combinations(self, num_days):
        """Get combinations of days for multi-session courses"""
        from itertools import combinations
        return list(combinations(self.days, num_days))
    
    def _add_hours_to_time(self, time_str, hours):
        """Add hours to a time string"""
        try:
            time_obj = datetime.strptime(time_str, "%H:%M").time()
            datetime_obj = datetime.combine(datetime.today(), time_obj)
            new_datetime = datetime_obj + timedelta(hours=hours)
            return new_datetime.strftime("%H:%M")
        except:
            return None
    
    def _can_assign_pattern(self, pattern, faculty_name, room_name, section_name,
                          faculty_schedule, room_schedule, section_schedule, allow_conflicts):
        """Check if a time pattern can be assigned without conflicts"""
        if allow_conflicts:
            return True
        
        for session in pattern:
            day = session['day']
            start_time = session['start_time']
            end_time = session['end_time']
            
            # Check faculty availability
            if day in faculty_schedule[faculty_name]:
                for existing_session in faculty_schedule[faculty_name][day]:
                    if self._times_overlap(start_time, end_time, 
                                         existing_session['start_time'], 
                                         existing_session['end_time']):
                        return False
            
            # Check room availability
            if day in room_schedule[room_name]:
                for existing_session in room_schedule[room_name][day]:
                    if self._times_overlap(start_time, end_time,
                                         existing_session['start_time'],
                                         existing_session['end_time']):
                        return False
            
            # Check section availability
            if day in section_schedule[section_name]:
                for existing_session in section_schedule[section_name][day]:
                    if self._times_overlap(start_time, end_time,
                                         existing_session['start_time'],
                                         existing_session['end_time']):
                        return False
        
        return True
    
    def _times_overlap(self, start1, end1, start2, end2):
        """Check if two time periods overlap"""
        try:
            start1_dt = datetime.strptime(start1, "%H:%M").time()
            end1_dt = datetime.strptime(end1, "%H:%M").time()
            start2_dt = datetime.strptime(start2, "%H:%M").time()
            end2_dt = datetime.strptime(end2, "%H:%M").time()
            
            return not (end1_dt <= start2_dt or end2_dt <= start1_dt)
        except:
            return False
    
    def _make_assignment(self, pattern, course_row, section_row, faculty_name, room_name,
                       component_type, schedule_list, faculty_schedule, room_schedule, section_schedule):
        """Make the actual assignment and update tracking structures"""
        section_name = section_row['section_name']
        
        for session in pattern:
            day = session['day']
            start_time = session['start_time']
            end_time = session['end_time']
            
            # Add to schedule list
            schedule_entry = {
                'course_code': course_row['course_code'],
                'course_title': course_row['course_title'],
                'program': section_row['program'],
                'year_level': section_row['year_level'],
                'term': section_row['term'],
                'section': section_name,
                'day': day,
                'start_time': start_time,
                'end_time': end_time,
                'room': room_name,
                'faculty': faculty_name,
                'course_type': component_type,
                'students_count': section_row['students_count']
            }
            schedule_list.append(schedule_entry)
            
            # Update tracking structures
            session_info = {
                'start_time': start_time,
                'end_time': end_time,
                'course': course_row['course_code'],
                'section': section_name
            }
            
            # Update faculty schedule
            if day not in faculty_schedule[faculty_name]:
                faculty_schedule[faculty_name][day] = []
            faculty_schedule[faculty_name][day].append(session_info)
            
            # Update room schedule
            if day not in room_schedule[room_name]:
                room_schedule[room_name][day] = []
            room_schedule[room_name][day].append(session_info)
            
            # Update section schedule
            if day not in section_schedule[section_name]:
                section_schedule[section_name][day] = []
            section_schedule[section_name][day].append(session_info)
        
        # Increment counter after successful assignment for even day-pairing distribution
        self.day_pairing_counter += 1
    
    def _find_suitable_faculty(self, course_row):
        """Find faculty members suitable for teaching a course"""
        # For now, return all faculty - in real implementation, 
        # this would filter by specialization
        if self.faculty is None:
            return pd.DataFrame()
        return self.faculty.copy()
    
    def _backtracking_scheduling(self, courses_to_schedule, max_iterations, allow_conflicts):
        """Backtracking scheduling algorithm with intelligent constraint solving"""
        schedule_list = []
        faculty_schedule = {}
        room_schedule = {}
        section_schedule = {}
        
        # Initialize tracking dictionaries
        if self.faculty is None or self.rooms is None or self.sections is None:
            raise ValueError("Required data not loaded")
            
        for faculty_name in self.faculty['faculty_name']:
            faculty_schedule[faculty_name] = {}
        for room_name in self.rooms['room_name']:
            room_schedule[room_name] = {}
        
        # Create assignment variables for backtracking
        assignments = []
        
        # Collect all courses that need to be scheduled
        for _, section_row in self.sections.iterrows():
            section_name = section_row['section_name']
            program = section_row['program']
            year_level = section_row['year_level']
            term = section_row['term']
            
            section_schedule[section_name] = {}
            
            # Get courses for this section
            section_courses = courses_to_schedule[
                (courses_to_schedule['program'] == program) &
                (courses_to_schedule['year_level'] == year_level) &
                (courses_to_schedule['term'] == term)
            ]
            
            for _, course_row in section_courses.iterrows():
                assignments.append({
                    'course': course_row,
                    'section': section_row,
                    'assigned': False,
                    'assignment': None
                })
        
        # Sort assignments by constraint complexity (most constrained first)
        assignments.sort(key=lambda x: self._calculate_constraint_complexity(x), reverse=True)
        
        # Start backtracking
        if self._backtrack_assign(assignments, 0, schedule_list, faculty_schedule, 
                                room_schedule, section_schedule, max_iterations, allow_conflicts):
            return pd.DataFrame(schedule_list) if schedule_list else pd.DataFrame()
        else:
            # If backtracking fails, fall back to greedy with conflicts allowed
            print("Backtracking failed, falling back to greedy algorithm")
            return self._greedy_scheduling(courses_to_schedule, True)
    
    def _calculate_constraint_complexity(self, assignment):
        """Calculate how constrained an assignment is (higher = more constrained)"""
        course = assignment['course']
        complexity = 0
        
        # Lab courses are more constrained
        if 'lab' in course['course_type'].lower() or course['course_type'].lower() == 'both':
            complexity += 10
        
        # Longer courses are more constrained
        complexity += course['hours_per_week']
        
        # Courses with specific requirements are more constrained
        if course['course_type'].lower() == 'both':
            complexity += 5
        
        return complexity
    
    def _backtrack_assign(self, assignments, index, schedule_list, faculty_schedule, 
                         room_schedule, section_schedule, max_iterations, allow_conflicts):
        """Recursive backtracking assignment function"""
        if index >= len(assignments):
            return True  # All assignments made successfully
        
        if len(schedule_list) > max_iterations:
            return False  # Exceeded iteration limit
        
        assignment = assignments[index]
        course_row = assignment['course']
        section_row = assignment['section']
        
        # Get all possible assignments for this course-section pair
        possible_assignments = self._get_possible_assignments(course_row, section_row, 
                                                            faculty_schedule, room_schedule, 
                                                            section_schedule, allow_conflicts)
        
        # Try each possible assignment
        for assignment_option in possible_assignments:
            # Make the assignment
            self._make_assignment_backtrack(assignment_option, course_row, section_row, 
                                          schedule_list, faculty_schedule, 
                                          room_schedule, section_schedule)
            
            # Recursively try to assign the rest
            if self._backtrack_assign(assignments, index + 1, schedule_list, 
                                    faculty_schedule, room_schedule, section_schedule, 
                                    max_iterations, allow_conflicts):
                return True
            
            # Backtrack: undo the assignment
            self._undo_assignment_backtrack(assignment_option, course_row, section_row, 
                                           schedule_list, faculty_schedule, 
                                           room_schedule, section_schedule)
        
        return False  # No valid assignment found
    
    def _get_possible_assignments(self, course_row, section_row, faculty_schedule, 
                                room_schedule, section_schedule, allow_conflicts):
        """Get all possible assignments for a course-section pair"""
        possible_assignments = []
        
        # Determine required room type
        required_room_type = 'Lab' if 'lab' in course_row['course_type'].lower() else 'Lecture'
        suitable_rooms = self.rooms[self.rooms['room_type'] == required_room_type]
        suitable_faculty = self._find_suitable_faculty(course_row)
        
        hours_per_week = course_row['hours_per_week']
        time_patterns = self._get_time_patterns(hours_per_week)
        
        for pattern in time_patterns:
            for _, faculty_row in suitable_faculty.iterrows():
                faculty_name = faculty_row['faculty_name']
                for _, room_row in suitable_rooms.iterrows():
                    room_name = room_row['room_name']
                    
                    if allow_conflicts or self._can_assign_pattern(
                        pattern, faculty_name, room_name, section_row['section_name'],
                        faculty_schedule, room_schedule, section_schedule, allow_conflicts
                    ):
                        possible_assignments.append({
                            'pattern': pattern,
                            'faculty': faculty_name,
                            'room': room_name
                        })
        
        # Sort by preference (e.g., prefer earlier times, specific faculty, etc.)
        possible_assignments.sort(key=lambda x: self._assignment_preference(x))
        
        return possible_assignments
    
    def _assignment_preference(self, assignment_option):
        """Calculate preference score for an assignment (lower = more preferred)"""
        pattern = assignment_option['pattern']
        preference = 0
        
        # Prefer earlier time slots
        if pattern:
            first_session = pattern[0]
            start_hour = int(first_session['start_time'].split(':')[0])
            preference += start_hour
        
        # Prefer certain days (e.g., Monday-Friday over Saturday)
        if pattern and any(session['day'] == 'Saturday' for session in pattern):
            preference += 20
        
        return preference
    
    def _make_assignment_backtrack(self, assignment_option, course_row, section_row, 
                                 schedule_list, faculty_schedule, room_schedule, section_schedule):
        """Make an assignment during backtracking"""
        pattern = assignment_option['pattern']
        faculty_name = assignment_option['faculty']
        room_name = assignment_option['room']
        section_name = section_row['section_name']
        
        component_type = 'Lecture' if 'lecture' in course_row['course_type'].lower() else 'Lab'
        if course_row['course_type'].lower() == 'both':
            component_type = 'Both'
        
        assignment_data = []
        
        for session in pattern:
            day = session['day']
            start_time = session['start_time']
            end_time = session['end_time']
            
            # Add to schedule list
            schedule_entry = {
                'course_code': course_row['course_code'],
                'course_title': course_row['course_title'],
                'program': section_row['program'],
                'year_level': section_row['year_level'],
                'term': section_row['term'],
                'section': section_name,
                'day': day,
                'start_time': start_time,
                'end_time': end_time,
                'room': room_name,
                'faculty': faculty_name,
                'course_type': component_type,
                'students_count': section_row['students_count']
            }
            schedule_list.append(schedule_entry)
            assignment_data.append(len(schedule_list) - 1)  # Store indices for backtracking
            
            # Update tracking structures
            session_info = {
                'start_time': start_time,
                'end_time': end_time,
                'course': course_row['course_code'],
                'section': section_name
            }
            
            # Update faculty schedule
            if day not in faculty_schedule[faculty_name]:
                faculty_schedule[faculty_name][day] = []
            faculty_schedule[faculty_name][day].append(session_info)
            
            # Update room schedule
            if day not in room_schedule[room_name]:
                room_schedule[room_name][day] = []
            room_schedule[room_name][day].append(session_info)
            
            # Update section schedule
            if day not in section_schedule[section_name]:
                section_schedule[section_name][day] = []
            section_schedule[section_name][day].append(session_info)
        
        # Store assignment data for backtracking
        assignment_option['assignment_data'] = assignment_data
        
        # Increment counter after successful assignment for even day-pairing distribution
        self.day_pairing_counter += 1
    
    def _undo_assignment_backtrack(self, assignment_option, course_row, section_row, 
                                 schedule_list, faculty_schedule, room_schedule, section_schedule):
        """Undo an assignment during backtracking"""
        if 'assignment_data' not in assignment_option:
            return
        
        pattern = assignment_option['pattern']
        faculty_name = assignment_option['faculty']
        room_name = assignment_option['room']
        section_name = section_row['section_name']
        assignment_data = assignment_option['assignment_data']
        
        # Remove from schedule list (in reverse order)
        for idx in reversed(assignment_data):
            if idx < len(schedule_list):
                schedule_list.pop(idx)
        
        # Remove from tracking structures
        for session in pattern:
            day = session['day']
            
            # Remove from faculty schedule
            if day in faculty_schedule[faculty_name]:
                faculty_schedule[faculty_name][day] = [
                    s for s in faculty_schedule[faculty_name][day]
                    if not (s['course'] == course_row['course_code'] and s['section'] == section_name)
                ]
                if not faculty_schedule[faculty_name][day]:
                    del faculty_schedule[faculty_name][day]
            
            # Remove from room schedule
            if day in room_schedule[room_name]:
                room_schedule[room_name][day] = [
                    s for s in room_schedule[room_name][day]
                    if not (s['course'] == course_row['course_code'] and s['section'] == section_name)
                ]
                if not room_schedule[room_name][day]:
                    del room_schedule[room_name][day]
            
            # Remove from section schedule
            if day in section_schedule[section_name]:
                section_schedule[section_name][day] = [
                    s for s in section_schedule[section_name][day]
                    if not (s['course'] == course_row['course_code'])
                ]
                if not section_schedule[section_name][day]:
                    del section_schedule[section_name][day]
        
        # Decrement counter when undoing assignment to maintain accuracy
        self.day_pairing_counter -= 1
    
    def _constraint_satisfaction_scheduling(self, courses_to_schedule, max_iterations, allow_conflicts):
        """Constraint Satisfaction Problem (CSP) based scheduling algorithm"""
        # Initialize CSP variables
        variables = []  # Each variable represents a course-section assignment
        domains = {}   # Possible values for each variable
        constraints = []  # Constraints between variables
        
        if self.faculty is None or self.rooms is None or self.sections is None:
            raise ValueError("Required data not loaded")
        
        # Create variables for each course-section pair
        for _, section_row in self.sections.iterrows():
            section_name = section_row['section_name']
            program = section_row['program']
            year_level = section_row['year_level']
            term = section_row['term']
            
            # Get courses for this section
            section_courses = courses_to_schedule[
                (courses_to_schedule['program'] == program) &
                (courses_to_schedule['year_level'] == year_level) &
                (courses_to_schedule['term'] == term)
            ]
            
            for _, course_row in section_courses.iterrows():
                var_name = f"{course_row['course_code']}_{section_name}"
                variables.append(var_name)
                
                # Generate domain (possible assignments)
                domains[var_name] = self._generate_csp_domain(course_row, section_row)
        
        # Generate constraints
        constraints = self._generate_csp_constraints(variables, domains)
        
        # Solve CSP using Arc Consistency + Backtracking
        solution = self._solve_csp(variables, domains, constraints, max_iterations, allow_conflicts)
        
        if solution:
            return self._convert_csp_solution_to_schedule(solution, courses_to_schedule)
        else:
            print("CSP solving failed, falling back to greedy algorithm")
            return self._greedy_scheduling(courses_to_schedule, True)
    
    def _generate_csp_domain(self, course_row, section_row):
        """Generate domain of possible assignments for a course-section pair"""
        domain = []
        
        # Determine required room type
        required_room_type = 'Lab' if 'lab' in course_row['course_type'].lower() else 'Lecture'
        suitable_rooms = self.rooms[self.rooms['room_type'] == required_room_type]
        suitable_faculty = self._find_suitable_faculty(course_row)
        
        hours_per_week = course_row['hours_per_week']
        time_patterns = self._get_time_patterns(hours_per_week)
        
        for pattern in time_patterns:
            for _, faculty_row in suitable_faculty.iterrows():
                faculty_name = faculty_row['faculty_name']
                for _, room_row in suitable_rooms.iterrows():
                    room_name = room_row['room_name']
                    
                    domain.append({
                        'pattern': pattern,
                        'faculty': faculty_name,
                        'room': room_name,
                        'course': course_row,
                        'section': section_row
                    })
        
        return domain
    
    def _generate_csp_constraints(self, variables, domains):
        """Generate constraints between variables"""
        constraints = []
        
        # Generate pairwise constraints
        for i, var1 in enumerate(variables):
            for j, var2 in enumerate(variables):
                if i < j:  # Avoid duplicate constraints
                    constraints.append({
                        'var1': var1,
                        'var2': var2,
                        'type': 'no_conflict'
                    })
        
        return constraints
    
    def _solve_csp(self, variables, domains, constraints, max_iterations, allow_conflicts):
        """Solve CSP using Arc Consistency and Backtracking"""
        # Apply arc consistency to reduce domains
        if not allow_conflicts:
            domains = self._apply_arc_consistency(variables, domains, constraints)
            
            # Check if any domain became empty
            if any(not domains[var] for var in variables):
                return None
        
        # Use backtracking to find solution
        assignment = {}
        return self._csp_backtrack(variables, domains, constraints, assignment, max_iterations, allow_conflicts)
    
    def _apply_arc_consistency(self, variables, domains, constraints):
        """Apply AC-3 algorithm for arc consistency"""
        queue = [(c['var1'], c['var2']) for c in constraints] + [(c['var2'], c['var1']) for c in constraints]
        
        while queue:
            var1, var2 = queue.pop(0)
            
            if self._revise_domain(var1, var2, domains):
                if not domains[var1]:
                    return {}  # Inconsistent
                
                # Add neighbors back to queue
                for constraint in constraints:
                    if constraint['var1'] == var1 and constraint['var2'] != var2:
                        queue.append((constraint['var2'], var1))
                    elif constraint['var2'] == var1 and constraint['var1'] != var2:
                        queue.append((constraint['var1'], var1))
        
        return domains
    
    def _revise_domain(self, var1, var2, domains):
        """Revise domain of var1 with respect to var2"""
        revised = False
        
        for value1 in domains[var1][:]:
            satisfies_constraint = False
            
            for value2 in domains[var2]:
                if self._values_satisfy_constraint(value1, value2):
                    satisfies_constraint = True
                    break
            
            if not satisfies_constraint:
                domains[var1].remove(value1)
                revised = True
        
        return revised
    
    def _values_satisfy_constraint(self, value1, value2):
        """Check if two values satisfy the constraint (no conflicts)"""
        # Check for faculty conflicts
        if value1['faculty'] == value2['faculty']:
            if self._time_patterns_overlap(value1['pattern'], value2['pattern']):
                return False
        
        # Check for room conflicts
        if value1['room'] == value2['room']:
            if self._time_patterns_overlap(value1['pattern'], value2['pattern']):
                return False
        
        # Check for section conflicts
        if value1['section']['section_name'] == value2['section']['section_name']:
            if self._time_patterns_overlap(value1['pattern'], value2['pattern']):
                return False
        
        return True
    
    def _time_patterns_overlap(self, pattern1, pattern2):
        """Check if two time patterns overlap"""
        for session1 in pattern1:
            for session2 in pattern2:
                if (session1['day'] == session2['day'] and
                    self._times_overlap(session1['start_time'], session1['end_time'],
                                      session2['start_time'], session2['end_time'])):
                    return True
        return False
    
    def _csp_backtrack(self, variables, domains, constraints, assignment, max_iterations, allow_conflicts):
        """Backtracking search for CSP"""
        if len(assignment) == len(variables):
            return assignment  # Complete assignment found
        
        if len(assignment) > max_iterations:
            return None  # Exceeded iteration limit
        
        # Select unassigned variable (using MRV heuristic)
        unassigned_vars = [var for var in variables if var not in assignment]
        var = min(unassigned_vars, key=lambda v: len(domains[v]))
        
        # Try each value in domain (using LCV heuristic)
        domain_values = sorted(domains[var], key=lambda val: self._count_conflicts(var, val, assignment, constraints))
        
        for value in domain_values:
            if allow_conflicts or self._assignment_consistent(var, value, assignment, constraints):
                assignment[var] = value
                
                # Make inference (forward checking)
                inference = self._forward_check(var, value, variables, domains, assignment, constraints)
                
                if inference is not None or allow_conflicts:
                    # Apply inference
                    old_domains = {}
                    if inference:
                        for inf_var, removed_values in inference.items():
                            old_domains[inf_var] = domains[inf_var][:]
                            for removed_val in removed_values:
                                if removed_val in domains[inf_var]:
                                    domains[inf_var].remove(removed_val)
                    
                    result = self._csp_backtrack(variables, domains, constraints, assignment, max_iterations, allow_conflicts)
                    if result is not None:
                        return result
                    
                    # Restore domains
                    for inf_var, old_domain in old_domains.items():
                        domains[inf_var] = old_domain
                
                del assignment[var]
        
        return None
    
    def _assignment_consistent(self, var, value, assignment, constraints):
        """Check if assignment is consistent with current partial assignment"""
        for assigned_var, assigned_value in assignment.items():
            if not self._values_satisfy_constraint(value, assigned_value):
                return False
        return True
    
    def _forward_check(self, var, value, variables, domains, assignment, constraints):
        """Forward checking inference"""
        inference = {}
        
        for other_var in variables:
            if other_var != var and other_var not in assignment:
                removed_values = []
                for other_value in domains[other_var][:]:
                    if not self._values_satisfy_constraint(value, other_value):
                        removed_values.append(other_value)
                
                if removed_values:
                    inference[other_var] = removed_values
                    # Check if domain becomes empty
                    if len(removed_values) == len(domains[other_var]):
                        return None
        
        return inference
    
    def _count_conflicts(self, var, value, assignment, constraints):
        """Count conflicts for LCV heuristic"""
        conflicts = 0
        for assigned_var, assigned_value in assignment.items():
            if not self._values_satisfy_constraint(value, assigned_value):
                conflicts += 1
        return conflicts
    
    def _convert_csp_solution_to_schedule(self, solution, courses_to_schedule):
        """Convert CSP solution to schedule DataFrame"""
        schedule_list = []
        
        for var_name, assignment in solution.items():
            course_row = assignment['course']
            section_row = assignment['section']
            pattern = assignment['pattern']
            faculty_name = assignment['faculty']
            room_name = assignment['room']
            
            component_type = 'Lecture' if 'lecture' in course_row['course_type'].lower() else 'Lab'
            if course_row['course_type'].lower() == 'both':
                component_type = 'Both'
            
            for session in pattern:
                schedule_entry = {
                    'course_code': course_row['course_code'],
                    'course_title': course_row['course_title'],
                    'program': section_row['program'],
                    'year_level': section_row['year_level'],
                    'term': section_row['term'],
                    'section': section_row['section_name'],
                    'day': session['day'],
                    'start_time': session['start_time'],
                    'end_time': session['end_time'],
                    'room': room_name,
                    'faculty': faculty_name,
                    'course_type': component_type,
                    'students_count': section_row['students_count']
                }
                schedule_list.append(schedule_entry)
        
        return pd.DataFrame(schedule_list)
