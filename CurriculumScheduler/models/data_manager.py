import pandas as pd
import numpy as np
from typing import Optional, Dict, List

class DataManager:
    def __init__(self):
        self.courses: Optional[pd.DataFrame] = None
        self.rooms: Optional[pd.DataFrame] = None
        self.faculty: Optional[pd.DataFrame] = None
        self.enrollments: Optional[pd.DataFrame] = None
        self.sections: Optional[pd.DataFrame] = None
    
    def load_courses(self, df: pd.DataFrame):
        """Load courses data from DataFrame"""
        self.courses = df.copy()
        self._validate_courses_data()
    
    def load_rooms(self, df: pd.DataFrame):
        """Load rooms data from DataFrame"""
        self.rooms = df.copy()
        self._validate_rooms_data()
    
    def load_faculty(self, df: pd.DataFrame):
        """Load faculty data from DataFrame"""
        self.faculty = df.copy()
        self._validate_faculty_data()
    
    def load_enrollments(self, df: pd.DataFrame):
        """Load enrollments data from DataFrame"""
        self.enrollments = df.copy()
        self._validate_enrollments_data()
    
    def _validate_courses_data(self):
        """Validate courses data structure"""
        if self.courses is None:
            raise ValueError("Courses data is None")
        required_columns = [
            'course_code', 'course_title', 'program', 'year_level', 
            'term', 'course_type', 'units', 'hours_per_week'
        ]
        missing_columns = [col for col in required_columns if col not in self.courses.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns in courses data: {missing_columns}")
    
    def _validate_rooms_data(self):
        """Validate rooms data structure"""
        if self.rooms is None:
            raise ValueError("Rooms data is None")
        required_columns = [
            'room_name', 'room_type', 'capacity', 'available_days', 'start_time', 'end_time'
        ]
        missing_columns = [col for col in required_columns if col not in self.rooms.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns in rooms data: {missing_columns}")
    
    def _validate_faculty_data(self):
        """Validate faculty data structure"""
        if self.faculty is None:
            raise ValueError("Faculty data is None")
        required_columns = [
            'faculty_name'
        ]
        missing_columns = [col for col in required_columns if col not in self.faculty.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns in faculty data: {missing_columns}")
    
    def _validate_enrollments_data(self):
        """Validate enrollments data structure"""
        if self.enrollments is None:
            raise ValueError("Enrollments data is None")
        required_columns = ['program', 'year_level', 'term', 'total_students']
        missing_columns = [col for col in required_columns if col not in self.enrollments.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns in enrollments data: {missing_columns}")
    
    def load_default_courses(self):
        """Load default course data for all programs and years"""
        courses_data = [
            # BSCS Courses
            # Year 1
            {"course_code": "CCINCOMX", "course_title": "Introduction to Computing", "program": "BSCS", "year_level": 1, "term": 1, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            {"course_code": "CCINCOBL", "course_title": "Introduction to Computing Lab", "program": "BSCS", "year_level": 1, "term": 1, "course_type": "Lab", "units": 1, "hours_per_week": 3},
            {"course_code": "CCPRGG1X", "course_title": "Fundamentals of Programming", "program": "BSCS", "year_level": 1, "term": 1, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            {"course_code": "CCPRG1BL", "course_title": "Fundamentals of Programming Lab", "program": "BSCS", "year_level": 1, "term": 1, "course_type": "Lab", "units": 1, "hours_per_week": 3},
            {"course_code": "GEMATMW", "course_title": "Mathematics in the Modern World", "program": "BSCS", "year_level": 1, "term": 1, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            {"course_code": "GEUNDSE", "course_title": "Understanding the Self", "program": "BSCS", "year_level": 1, "term": 1, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            {"course_code": "NSTP1", "course_title": "National Service Training Program 1", "program": "BSCS", "year_level": 1, "term": 1, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            {"course_code": "PE1", "course_title": "Physical Education 1", "program": "BSCS", "year_level": 1, "term": 1, "course_type": "Lecture", "units": 2, "hours_per_week": 2},
            
            {"course_code": "CCDISTR1", "course_title": "Discrete Structures 1", "program": "BSCS", "year_level": 1, "term": 2, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            {"course_code": "CCPRGG2X", "course_title": "Intermediate Programming", "program": "BSCS", "year_level": 1, "term": 2, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            {"course_code": "CCPRG2BL", "course_title": "Intermediate Programming Lab", "program": "BSCS", "year_level": 1, "term": 2, "course_type": "Lab", "units": 1, "hours_per_week": 3},
            {"course_code": "GECYBER", "course_title": "Cybersecurity Fundamentals", "program": "BSCS", "year_level": 1, "term": 2, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            {"course_code": "GEPURCO", "course_title": "Purposive Communication", "program": "BSCS", "year_level": 1, "term": 2, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            {"course_code": "GERDHUM", "course_title": "Readings in Philippine History", "program": "BSCS", "year_level": 1, "term": 2, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            {"course_code": "NSTP2", "course_title": "National Service Training Program 2", "program": "BSCS", "year_level": 1, "term": 2, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            {"course_code": "PE2", "course_title": "Physical Education 2", "program": "BSCS", "year_level": 1, "term": 2, "course_type": "Lecture", "units": 2, "hours_per_week": 2},
            
            {"course_code": "CCDISTR2", "course_title": "Discrete Structures 2", "program": "BSCS", "year_level": 1, "term": 3, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            {"course_code": "CCOBJPGL", "course_title": "Object-Oriented Programming", "program": "BSCS", "year_level": 1, "term": 3, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            {"course_code": "CCOBJPGX", "course_title": "Object-Oriented Programming Lab", "program": "BSCS", "year_level": 1, "term": 3, "course_type": "Lab", "units": 1, "hours_per_week": 3},
            {"course_code": "GEARTAP", "course_title": "Art Appreciation", "program": "BSCS", "year_level": 1, "term": 3, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            {"course_code": "GESCITEC", "course_title": "Science, Technology and Society", "program": "BSCS", "year_level": 1, "term": 3, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            {"course_code": "PE3", "course_title": "Physical Education 3", "program": "BSCS", "year_level": 1, "term": 3, "course_type": "Lecture", "units": 2, "hours_per_week": 2},
            
            # Year 2
            {"course_code": "CCALCOML", "course_title": "Algorithms and Complexity", "program": "BSCS", "year_level": 2, "term": 1, "course_type": "Both", "units": 4, "hours_per_week": 6},
            {"course_code": "CCDATRCL", "course_title": "Data Structures and Algorithms", "program": "BSCS", "year_level": 2, "term": 1, "course_type": "Both", "units": 4, "hours_per_week": 6},
            {"course_code": "CCPROGRA", "course_title": "Advanced Programming", "program": "BSCS", "year_level": 2, "term": 1, "course_type": "Both", "units": 4, "hours_per_week": 6},
            {"course_code": "GEPHILO", "course_title": "Introduction to Philosophy", "program": "BSCS", "year_level": 2, "term": 1, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            {"course_code": "PE4", "course_title": "Physical Education 4", "program": "BSCS", "year_level": 2, "term": 1, "course_type": "Lecture", "units": 2, "hours_per_week": 2},
            
            {"course_code": "CCMACOML", "course_title": "Machine Learning", "program": "BSCS", "year_level": 2, "term": 2, "course_type": "Both", "units": 4, "hours_per_week": 6},
            {"course_code": "CCOPSYST", "course_title": "Operating Systems", "program": "BSCS", "year_level": 2, "term": 2, "course_type": "Both", "units": 4, "hours_per_week": 6},
            {"course_code": "CCNETPRG", "course_title": "Network Programming", "program": "BSCS", "year_level": 2, "term": 2, "course_type": "Both", "units": 4, "hours_per_week": 6},
            {"course_code": "GEETHICS", "course_title": "Ethics", "program": "BSCS", "year_level": 2, "term": 2, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            {"course_code": "GERESEL1", "course_title": "Research Methods", "program": "BSCS", "year_level": 2, "term": 2, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            
            {"course_code": "CCDATABA", "course_title": "Database Systems", "program": "BSCS", "year_level": 2, "term": 3, "course_type": "Both", "units": 4, "hours_per_week": 6},
            {"course_code": "CCWEBDEV", "course_title": "Web Development", "program": "BSCS", "year_level": 2, "term": 3, "course_type": "Both", "units": 4, "hours_per_week": 6},
            {"course_code": "CCSOFENG", "course_title": "Software Engineering", "program": "BSCS", "year_level": 2, "term": 3, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            {"course_code": "CCFORMAL", "course_title": "Formal Methods", "program": "BSCS", "year_level": 2, "term": 3, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            {"course_code": "GESTATS", "course_title": "Statistics and Probability", "program": "BSCS", "year_level": 2, "term": 3, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            
            # Year 3
            {"course_code": "CCARTINT", "course_title": "Artificial Intelligence", "program": "BSCS", "year_level": 3, "term": 1, "course_type": "Both", "units": 4, "hours_per_week": 6},
            {"course_code": "CCCOMPGR", "course_title": "Computer Graphics", "program": "BSCS", "year_level": 3, "term": 1, "course_type": "Both", "units": 4, "hours_per_week": 6},
            {"course_code": "CCNETWORK", "course_title": "Computer Networks", "program": "BSCS", "year_level": 3, "term": 1, "course_type": "Both", "units": 4, "hours_per_week": 6},
            {"course_code": "CCTHESIS1", "course_title": "Thesis Writing 1", "program": "BSCS", "year_level": 3, "term": 1, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            {"course_code": "GELITREV", "course_title": "Literature Review", "program": "BSCS", "year_level": 3, "term": 1, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            
            {"course_code": "CCCYBERS", "course_title": "Cybersecurity", "program": "BSCS", "year_level": 3, "term": 2, "course_type": "Both", "units": 4, "hours_per_week": 6},
            {"course_code": "CCMOBILE", "course_title": "Mobile Application Development", "program": "BSCS", "year_level": 3, "term": 2, "course_type": "Both", "units": 4, "hours_per_week": 6},
            {"course_code": "CCHUMCOM", "course_title": "Human Computer Interaction", "program": "BSCS", "year_level": 3, "term": 2, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            {"course_code": "CCTHESIS2", "course_title": "Thesis Writing 2", "program": "BSCS", "year_level": 3, "term": 2, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            {"course_code": "GERESEL2", "course_title": "Research Methodology", "program": "BSCS", "year_level": 3, "term": 2, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            
            {"course_code": "CCPRACTI", "course_title": "Practicum", "program": "BSCS", "year_level": 3, "term": 3, "course_type": "Lecture", "units": 6, "hours_per_week": 6},
            {"course_code": "CCELECT1", "course_title": "CS Elective 1", "program": "BSCS", "year_level": 3, "term": 3, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            {"course_code": "CCELECT2", "course_title": "CS Elective 2", "program": "BSCS", "year_level": 3, "term": 3, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            
            # Year 4
            {"course_code": "CCTHESIS3", "course_title": "Thesis Implementation", "program": "BSCS", "year_level": 4, "term": 1, "course_type": "Lecture", "units": 6, "hours_per_week": 6},
            {"course_code": "CCELECT3", "course_title": "CS Elective 3", "program": "BSCS", "year_level": 4, "term": 1, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            {"course_code": "CCELECT4", "course_title": "CS Elective 4", "program": "BSCS", "year_level": 4, "term": 1, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            {"course_code": "CCPRPSEM", "course_title": "Professional Seminar", "program": "BSCS", "year_level": 4, "term": 1, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            {"course_code": "GERESELM", "course_title": "Research Methodology in CS", "program": "BSCS", "year_level": 4, "term": 1, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            
            {"course_code": "CCTHESIS4", "course_title": "Thesis Defense", "program": "BSCS", "year_level": 4, "term": 2, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            {"course_code": "CCINTERN", "course_title": "Internship", "program": "BSCS", "year_level": 4, "term": 2, "course_type": "Lecture", "units": 6, "hours_per_week": 6},
            {"course_code": "CCELECT5", "course_title": "CS Elective 5", "program": "BSCS", "year_level": 4, "term": 2, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            {"course_code": "CCELECT6", "course_title": "CS Elective 6", "program": "BSCS", "year_level": 4, "term": 2, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            
            # BSIS Courses
            # Year 1
            {"course_code": "CCINCOMX", "course_title": "Introduction to Computing", "program": "BSIS", "year_level": 1, "term": 1, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            {"course_code": "CCINCOBL", "course_title": "Introduction to Computing Lab", "program": "BSIS", "year_level": 1, "term": 1, "course_type": "Lab", "units": 1, "hours_per_week": 3},
            {"course_code": "CCPRGG1X", "course_title": "Fundamentals of Programming", "program": "BSIS", "year_level": 1, "term": 1, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            {"course_code": "CCPRG1BL", "course_title": "Fundamentals of Programming Lab", "program": "BSIS", "year_level": 1, "term": 1, "course_type": "Lab", "units": 1, "hours_per_week": 3},
            {"course_code": "GEMATMW", "course_title": "Mathematics in the Modern World", "program": "BSIS", "year_level": 1, "term": 1, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            {"course_code": "GEUNDSE", "course_title": "Understanding the Self", "program": "BSIS", "year_level": 1, "term": 1, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            {"course_code": "NSTP1", "course_title": "National Service Training Program 1", "program": "BSIS", "year_level": 1, "term": 1, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            {"course_code": "PE1", "course_title": "Physical Education 1", "program": "BSIS", "year_level": 1, "term": 1, "course_type": "Lecture", "units": 2, "hours_per_week": 2},
            
            {"course_code": "CCFUINSY", "course_title": "Fundamentals of Information Systems", "program": "BSIS", "year_level": 1, "term": 2, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            {"course_code": "CCPRGG2X", "course_title": "Intermediate Programming", "program": "BSIS", "year_level": 1, "term": 2, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            {"course_code": "CCPRG2BL", "course_title": "Intermediate Programming Lab", "program": "BSIS", "year_level": 1, "term": 2, "course_type": "Lab", "units": 1, "hours_per_week": 3},
            {"course_code": "GECYBER", "course_title": "Cybersecurity Fundamentals", "program": "BSIS", "year_level": 1, "term": 2, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            {"course_code": "GEPURCO", "course_title": "Purposive Communication", "program": "BSIS", "year_level": 1, "term": 2, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            {"course_code": "GERDHUM", "course_title": "Readings in Philippine History", "program": "BSIS", "year_level": 1, "term": 2, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            {"course_code": "NSTP2", "course_title": "National Service Training Program 2", "program": "BSIS", "year_level": 1, "term": 2, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            {"course_code": "PE2", "course_title": "Physical Education 2", "program": "BSIS", "year_level": 1, "term": 2, "course_type": "Lecture", "units": 2, "hours_per_week": 2},
            
            {"course_code": "CCDATRCL", "course_title": "Data Structures and Algorithms", "program": "BSIS", "year_level": 1, "term": 3, "course_type": "Both", "units": 4, "hours_per_week": 6},
            {"course_code": "CCORMACO", "course_title": "Organization and Management Concepts", "program": "BSIS", "year_level": 1, "term": 3, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            {"course_code": "GEARTAP", "course_title": "Art Appreciation", "program": "BSIS", "year_level": 1, "term": 3, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            {"course_code": "GESCITEC", "course_title": "Science, Technology and Society", "program": "BSIS", "year_level": 1, "term": 3, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            {"course_code": "PE3", "course_title": "Physical Education 3", "program": "BSIS", "year_level": 1, "term": 3, "course_type": "Lecture", "units": 2, "hours_per_week": 2},
            
            # BSIS Year 2
            {"course_code": "CCDATABA", "course_title": "Database Management Systems", "program": "BSIS", "year_level": 2, "term": 1, "course_type": "Both", "units": 4, "hours_per_week": 6},
            {"course_code": "CCSYSANA", "course_title": "Systems Analysis and Design", "program": "BSIS", "year_level": 2, "term": 1, "course_type": "Both", "units": 4, "hours_per_week": 6},
            {"course_code": "CCWEBDEV", "course_title": "Web Development", "program": "BSIS", "year_level": 2, "term": 1, "course_type": "Both", "units": 4, "hours_per_week": 6},
            {"course_code": "GEPHILO", "course_title": "Introduction to Philosophy", "program": "BSIS", "year_level": 2, "term": 1, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            {"course_code": "PE4", "course_title": "Physical Education 4", "program": "BSIS", "year_level": 2, "term": 1, "course_type": "Lecture", "units": 2, "hours_per_week": 2},
            
            {"course_code": "CCBUSINT", "course_title": "Business Intelligence", "program": "BSIS", "year_level": 2, "term": 2, "course_type": "Both", "units": 4, "hours_per_week": 6},
            {"course_code": "CCNETWORK", "course_title": "Networking and Data Communications", "program": "BSIS", "year_level": 2, "term": 2, "course_type": "Both", "units": 4, "hours_per_week": 6},
            {"course_code": "CCPROMAN", "course_title": "Project Management", "program": "BSIS", "year_level": 2, "term": 2, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            {"course_code": "GEETHICS", "course_title": "Ethics", "program": "BSIS", "year_level": 2, "term": 2, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            {"course_code": "GERESEL1", "course_title": "Research Methods", "program": "BSIS", "year_level": 2, "term": 2, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            
            {"course_code": "CCSYSINT", "course_title": "Systems Integration", "program": "BSIS", "year_level": 2, "term": 3, "course_type": "Both", "units": 4, "hours_per_week": 6},
            {"course_code": "CCINFOSC", "course_title": "Information Security", "program": "BSIS", "year_level": 2, "term": 3, "course_type": "Both", "units": 4, "hours_per_week": 6},
            {"course_code": "CCQUALIT", "course_title": "Quality Assurance", "program": "BSIS", "year_level": 2, "term": 3, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            {"course_code": "GESTATS", "course_title": "Statistics and Probability", "program": "BSIS", "year_level": 2, "term": 3, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            
            # BSIS Year 3
            {"course_code": "CCENTSYS", "course_title": "Enterprise Systems", "program": "BSIS", "year_level": 3, "term": 1, "course_type": "Both", "units": 4, "hours_per_week": 6},
            {"course_code": "CCDATASC", "course_title": "Data Science and Analytics", "program": "BSIS", "year_level": 3, "term": 1, "course_type": "Both", "units": 4, "hours_per_week": 6},
            {"course_code": "CCBUSAPP", "course_title": "Business Applications Development", "program": "BSIS", "year_level": 3, "term": 1, "course_type": "Both", "units": 4, "hours_per_week": 6},
            {"course_code": "CCTHESIS1", "course_title": "Thesis Writing 1", "program": "BSIS", "year_level": 3, "term": 1, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            {"course_code": "GELITREV", "course_title": "Literature Review", "program": "BSIS", "year_level": 3, "term": 1, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            
            {"course_code": "CCINFMAN", "course_title": "Information Systems Management", "program": "BSIS", "year_level": 3, "term": 2, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            {"course_code": "CCITSRVC", "course_title": "IT Service Management", "program": "BSIS", "year_level": 3, "term": 2, "course_type": "Both", "units": 4, "hours_per_week": 6},
            {"course_code": "CCECOMRC", "course_title": "E-Commerce Systems", "program": "BSIS", "year_level": 3, "term": 2, "course_type": "Both", "units": 4, "hours_per_week": 6},
            {"course_code": "CCTHESIS2", "course_title": "Thesis Writing 2", "program": "BSIS", "year_level": 3, "term": 2, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            {"course_code": "GERESEL2", "course_title": "Research Methodology", "program": "BSIS", "year_level": 3, "term": 2, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            
            {"course_code": "CCPRACTI", "course_title": "Practicum", "program": "BSIS", "year_level": 3, "term": 3, "course_type": "Lecture", "units": 6, "hours_per_week": 6},
            {"course_code": "CCELECT1", "course_title": "IS Elective 1", "program": "BSIS", "year_level": 3, "term": 3, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            {"course_code": "CCELECT2", "course_title": "IS Elective 2", "program": "BSIS", "year_level": 3, "term": 3, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            
            # BSIS Year 4
            {"course_code": "CCTHESIS3", "course_title": "Thesis Implementation", "program": "BSIS", "year_level": 4, "term": 1, "course_type": "Lecture", "units": 6, "hours_per_week": 6},
            {"course_code": "CCELECT3", "course_title": "IS Elective 3", "program": "BSIS", "year_level": 4, "term": 1, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            {"course_code": "CCELECT4", "course_title": "IS Elective 4", "program": "BSIS", "year_level": 4, "term": 1, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            {"course_code": "CCPRPSEM", "course_title": "Professional Seminar", "program": "BSIS", "year_level": 4, "term": 1, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            {"course_code": "GERESELM", "course_title": "Research Methodology in IS", "program": "BSIS", "year_level": 4, "term": 1, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            
            {"course_code": "CCTHESIS4", "course_title": "Thesis Defense", "program": "BSIS", "year_level": 4, "term": 2, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            {"course_code": "CCINTERN", "course_title": "Internship", "program": "BSIS", "year_level": 4, "term": 2, "course_type": "Lecture", "units": 6, "hours_per_week": 6},
            {"course_code": "CCELECT5", "course_title": "IS Elective 5", "program": "BSIS", "year_level": 4, "term": 2, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            {"course_code": "CCELECT6", "course_title": "IS Elective 6", "program": "BSIS", "year_level": 4, "term": 2, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            
            # BSIT Courses
            # Year 1
            {"course_code": "INTCOMC", "course_title": "Introduction to Computing for CS/IT", "program": "BSIT", "year_level": 1, "term": 1, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            {"course_code": "PROGCON", "course_title": "Programming Concepts and Logic", "program": "BSIT", "year_level": 1, "term": 1, "course_type": "Both", "units": 4, "hours_per_week": 6},
            {"course_code": "COMPORG", "course_title": "Computer Organization & Architecture", "program": "BSIT", "year_level": 1, "term": 1, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            {"course_code": "GEMATMW", "course_title": "Mathematics in the Modern World", "program": "BSIT", "year_level": 1, "term": 1, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            {"course_code": "GEUNDSE", "course_title": "Understanding the Self", "program": "BSIT", "year_level": 1, "term": 1, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            {"course_code": "NSTP1", "course_title": "National Service Training Program 1", "program": "BSIT", "year_level": 1, "term": 1, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            {"course_code": "PE1", "course_title": "Physical Education 1", "program": "BSIT", "year_level": 1, "term": 1, "course_type": "Lecture", "units": 2, "hours_per_week": 2},
            
            {"course_code": "INPROLA", "course_title": "Introduction to Programming & Theories", "program": "BSIT", "year_level": 1, "term": 2, "course_type": "Both", "units": 4, "hours_per_week": 6},
            {"course_code": "MANPRIN", "course_title": "Management Principles", "program": "BSIT", "year_level": 1, "term": 2, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            {"course_code": "OPESYST", "course_title": "Operating Systems", "program": "BSIT", "year_level": 1, "term": 2, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            {"course_code": "GEPURCO", "course_title": "Purposive Communication", "program": "BSIT", "year_level": 1, "term": 2, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            {"course_code": "GERDHUM", "course_title": "Readings in Philippine History", "program": "BSIT", "year_level": 1, "term": 2, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            {"course_code": "NSTP2", "course_title": "National Service Training Program 2", "program": "BSIT", "year_level": 1, "term": 2, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            {"course_code": "PE2", "course_title": "Physical Education 2", "program": "BSIT", "year_level": 1, "term": 2, "course_type": "Lecture", "units": 2, "hours_per_week": 2},
            
            {"course_code": "DASTRUC", "course_title": "Data Structures", "program": "BSIT", "year_level": 1, "term": 3, "course_type": "Both", "units": 4, "hours_per_week": 6},
            {"course_code": "BUSPROS", "course_title": "Business Process", "program": "BSIT", "year_level": 1, "term": 3, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            {"course_code": "DNETCOM", "course_title": "Network Security, Storage & Data Communication", "program": "BSIT", "year_level": 1, "term": 3, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            {"course_code": "GEARTAP", "course_title": "Art Appreciation", "program": "BSIT", "year_level": 1, "term": 3, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            {"course_code": "GESCITEC", "course_title": "Science, Technology and Society", "program": "BSIT", "year_level": 1, "term": 3, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            {"course_code": "PE3", "course_title": "Physical Education 3", "program": "BSIT", "year_level": 1, "term": 3, "course_type": "Lecture", "units": 2, "hours_per_week": 2},
            
            # BSIT Year 2
            {"course_code": "CCWEBDEV", "course_title": "Web Development", "program": "BSIT", "year_level": 2, "term": 1, "course_type": "Both", "units": 4, "hours_per_week": 6},
            {"course_code": "CCDATABA", "course_title": "Database Systems", "program": "BSIT", "year_level": 2, "term": 1, "course_type": "Both", "units": 4, "hours_per_week": 6},
            {"course_code": "CCNETADM", "course_title": "Network Administration", "program": "BSIT", "year_level": 2, "term": 1, "course_type": "Both", "units": 4, "hours_per_week": 6},
            {"course_code": "GEPHILO", "course_title": "Introduction to Philosophy", "program": "BSIT", "year_level": 2, "term": 1, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            {"course_code": "PE4", "course_title": "Physical Education 4", "program": "BSIT", "year_level": 2, "term": 1, "course_type": "Lecture", "units": 2, "hours_per_week": 2},
            
            {"course_code": "CCMOBILE", "course_title": "Mobile Application Development", "program": "BSIT", "year_level": 2, "term": 2, "course_type": "Both", "units": 4, "hours_per_week": 6},
            {"course_code": "CCSYSADM", "course_title": "Systems Administration", "program": "BSIT", "year_level": 2, "term": 2, "course_type": "Both", "units": 4, "hours_per_week": 6},
            {"course_code": "CCINFOSEC", "course_title": "Information Security", "program": "BSIT", "year_level": 2, "term": 2, "course_type": "Both", "units": 4, "hours_per_week": 6},
            {"course_code": "GEETHICS", "course_title": "Ethics", "program": "BSIT", "year_level": 2, "term": 2, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            {"course_code": "GERESEL1", "course_title": "Research Methods", "program": "BSIT", "year_level": 2, "term": 2, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            
            {"course_code": "CCSERVMAN", "course_title": "Server Management", "program": "BSIT", "year_level": 2, "term": 3, "course_type": "Both", "units": 4, "hours_per_week": 6},
            {"course_code": "CCCLOUDCOM", "course_title": "Cloud Computing", "program": "BSIT", "year_level": 2, "term": 3, "course_type": "Both", "units": 4, "hours_per_week": 6},
            {"course_code": "CCPROMAN", "course_title": "Project Management", "program": "BSIT", "year_level": 2, "term": 3, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            {"course_code": "GESTATS", "course_title": "Statistics and Probability", "program": "BSIT", "year_level": 2, "term": 3, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            
            # BSIT Year 3
            {"course_code": "CCDEVOPS", "course_title": "DevOps and Automation", "program": "BSIT", "year_level": 3, "term": 1, "course_type": "Both", "units": 4, "hours_per_week": 6},
            {"course_code": "CCBIGDATA", "course_title": "Big Data Technologies", "program": "BSIT", "year_level": 3, "term": 1, "course_type": "Both", "units": 4, "hours_per_week": 6},
            {"course_code": "CCITMANAG", "course_title": "IT Management and Governance", "program": "BSIT", "year_level": 3, "term": 1, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            {"course_code": "CCTHESIS1", "course_title": "Thesis Writing 1", "program": "BSIT", "year_level": 3, "term": 1, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            {"course_code": "GELITREV", "course_title": "Literature Review", "program": "BSIT", "year_level": 3, "term": 1, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            
            {"course_code": "CCNETWORK", "course_title": "Advanced Networking", "program": "BSIT", "year_level": 3, "term": 2, "course_type": "Both", "units": 4, "hours_per_week": 6},
            {"course_code": "CCVIRTU", "course_title": "Virtualization Technologies", "program": "BSIT", "year_level": 3, "term": 2, "course_type": "Both", "units": 4, "hours_per_week": 6},
            {"course_code": "CCITSRVC", "course_title": "IT Service Management", "program": "BSIT", "year_level": 3, "term": 2, "course_type": "Both", "units": 4, "hours_per_week": 6},
            {"course_code": "CCTHESIS2", "course_title": "Thesis Writing 2", "program": "BSIT", "year_level": 3, "term": 2, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            {"course_code": "GERESEL2", "course_title": "Research Methodology", "program": "BSIT", "year_level": 3, "term": 2, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            
            {"course_code": "CCPRACTI", "course_title": "Practicum", "program": "BSIT", "year_level": 3, "term": 3, "course_type": "Lecture", "units": 6, "hours_per_week": 6},
            {"course_code": "CCELECT1", "course_title": "IT Elective 1", "program": "BSIT", "year_level": 3, "term": 3, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            {"course_code": "CCELECT2", "course_title": "IT Elective 2", "program": "BSIT", "year_level": 3, "term": 3, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            
            # BSIT Year 4
            {"course_code": "CCTHESIS3", "course_title": "Thesis Implementation", "program": "BSIT", "year_level": 4, "term": 1, "course_type": "Lecture", "units": 6, "hours_per_week": 6},
            {"course_code": "CCELECT3", "course_title": "IT Elective 3", "program": "BSIT", "year_level": 4, "term": 1, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            {"course_code": "CCELECT4", "course_title": "IT Elective 4", "program": "BSIT", "year_level": 4, "term": 1, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            {"course_code": "CCPRPSEM", "course_title": "Professional Seminar", "program": "BSIT", "year_level": 4, "term": 1, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            {"course_code": "GERESELM", "course_title": "Research Methodology in IT", "program": "BSIT", "year_level": 4, "term": 1, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            
            {"course_code": "CCTHESIS4", "course_title": "Thesis Defense", "program": "BSIT", "year_level": 4, "term": 2, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            {"course_code": "CCINTERN", "course_title": "Internship", "program": "BSIT", "year_level": 4, "term": 2, "course_type": "Lecture", "units": 6, "hours_per_week": 6},
            {"course_code": "CCELECT5", "course_title": "IT Elective 5", "program": "BSIT", "year_level": 4, "term": 2, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
            {"course_code": "CCELECT6", "course_title": "IT Elective 6", "program": "BSIT", "year_level": 4, "term": 2, "course_type": "Lecture", "units": 3, "hours_per_week": 3},
        ]
        
        self.courses = pd.DataFrame(courses_data)
    
    def load_default_rooms(self):
        """Load default room data"""
        rooms_data = [
            {"room_name": "Room101", "room_type": "Lecture", "capacity": 45, "available_days": "Monday,Tuesday,Wednesday,Thursday,Friday,Saturday", "start_time": "07:00", "end_time": "21:00"},
            {"room_name": "Room102", "room_type": "Lecture", "capacity": 45, "available_days": "Monday,Tuesday,Wednesday,Thursday,Friday,Saturday", "start_time": "07:00", "end_time": "21:00"},
            {"room_name": "Room103", "room_type": "Lecture", "capacity": 45, "available_days": "Monday,Tuesday,Wednesday,Thursday,Friday,Saturday", "start_time": "07:00", "end_time": "21:00"},
            {"room_name": "Room201", "room_type": "Lecture", "capacity": 50, "available_days": "Monday,Tuesday,Wednesday,Thursday,Friday,Saturday", "start_time": "07:00", "end_time": "21:00"},
            {"room_name": "Room202", "room_type": "Lecture", "capacity": 50, "available_days": "Monday,Tuesday,Wednesday,Thursday,Friday,Saturday", "start_time": "07:00", "end_time": "21:00"},
            {"room_name": "Room203", "room_type": "Lecture", "capacity": 50, "available_days": "Monday,Tuesday,Wednesday,Thursday,Friday,Saturday", "start_time": "07:00", "end_time": "21:00"},
            {"room_name": "ComLab1", "room_type": "Lab", "capacity": 40, "available_days": "Monday,Tuesday,Wednesday,Thursday,Friday,Saturday", "start_time": "07:00", "end_time": "21:00"},
            {"room_name": "ComLab2", "room_type": "Lab", "capacity": 40, "available_days": "Monday,Tuesday,Wednesday,Thursday,Friday,Saturday", "start_time": "07:00", "end_time": "21:00"},
            {"room_name": "ComLab3", "room_type": "Lab", "capacity": 40, "available_days": "Monday,Tuesday,Wednesday,Thursday,Friday,Saturday", "start_time": "07:00", "end_time": "21:00"},
            {"room_name": "ComLab4", "room_type": "Lab", "capacity": 35, "available_days": "Monday,Tuesday,Wednesday,Thursday,Friday,Saturday", "start_time": "07:00", "end_time": "21:00"},
            {"room_name": "ComLab5", "room_type": "Lab", "capacity": 35, "available_days": "Monday,Tuesday,Wednesday,Thursday,Friday,Saturday", "start_time": "07:00", "end_time": "21:00"},
            {"room_name": "ComLab6", "room_type": "Lab", "capacity": 35, "available_days": "Monday,Tuesday,Wednesday,Thursday,Friday,Saturday", "start_time": "07:00", "end_time": "21:00"},
        ]
        
        self.rooms = pd.DataFrame(rooms_data)
    
    def load_default_faculty(self):
        """Load default faculty data (constraints are now optional)"""
        faculty_data = [
            {"faculty_name": "Prof. John Smith"},
            {"faculty_name": "Prof. Maria Garcia"},
            {"faculty_name": "Prof. Robert Johnson"},
            {"faculty_name": "Prof. Lisa Brown"},
            {"faculty_name": "Prof. David Wilson"},
            {"faculty_name": "Prof. Sarah Davis"},
            {"faculty_name": "Prof. Michael Miller"},
            {"faculty_name": "Prof. Jennifer Taylor"},
            {"faculty_name": "Prof. Christopher Anderson"},
            {"faculty_name": "Prof. Amanda White"},
            {"faculty_name": "Prof. James Lee"},
            {"faculty_name": "Prof. Patricia Martinez"},
            {"faculty_name": "Prof. Thomas Rodriguez"},
            {"faculty_name": "Prof. Linda Hernandez"},
            {"faculty_name": "Prof. Richard Lopez"},
        ]
        
        self.faculty = pd.DataFrame(faculty_data)
    
    def load_default_enrollments(self):
        """Load default enrollment data"""
        enrollments_data = [
            # BSCS enrollments
            {"program": "BSCS", "year_level": 1, "term": 1, "total_students": 180},
            {"program": "BSCS", "year_level": 1, "term": 2, "total_students": 175},
            {"program": "BSCS", "year_level": 1, "term": 3, "total_students": 170},
            {"program": "BSCS", "year_level": 2, "term": 1, "total_students": 150},
            {"program": "BSCS", "year_level": 2, "term": 2, "total_students": 145},
            {"program": "BSCS", "year_level": 2, "term": 3, "total_students": 140},
            {"program": "BSCS", "year_level": 3, "term": 1, "total_students": 130},
            {"program": "BSCS", "year_level": 3, "term": 2, "total_students": 125},
            {"program": "BSCS", "year_level": 3, "term": 3, "total_students": 120},
            {"program": "BSCS", "year_level": 4, "term": 1, "total_students": 110},
            {"program": "BSCS", "year_level": 4, "term": 2, "total_students": 105},
            {"program": "BSCS", "year_level": 4, "term": 3, "total_students": 100},
            
            # BSIS enrollments
            {"program": "BSIS", "year_level": 1, "term": 1, "total_students": 160},
            {"program": "BSIS", "year_level": 1, "term": 2, "total_students": 155},
            {"program": "BSIS", "year_level": 1, "term": 3, "total_students": 150},
            {"program": "BSIS", "year_level": 2, "term": 1, "total_students": 135},
            {"program": "BSIS", "year_level": 2, "term": 2, "total_students": 130},
            {"program": "BSIS", "year_level": 2, "term": 3, "total_students": 125},
            {"program": "BSIS", "year_level": 3, "term": 1, "total_students": 115},
            {"program": "BSIS", "year_level": 3, "term": 2, "total_students": 110},
            {"program": "BSIS", "year_level": 3, "term": 3, "total_students": 105},
            {"program": "BSIS", "year_level": 4, "term": 1, "total_students": 95},
            {"program": "BSIS", "year_level": 4, "term": 2, "total_students": 90},
            {"program": "BSIS", "year_level": 4, "term": 3, "total_students": 85},
            
            # BSIT enrollments
            {"program": "BSIT", "year_level": 1, "term": 1, "total_students": 190},
            {"program": "BSIT", "year_level": 1, "term": 2, "total_students": 185},
            {"program": "BSIT", "year_level": 1, "term": 3, "total_students": 180},
            {"program": "BSIT", "year_level": 2, "term": 1, "total_students": 165},
            {"program": "BSIT", "year_level": 2, "term": 2, "total_students": 160},
            {"program": "BSIT", "year_level": 2, "term": 3, "total_students": 155},
            {"program": "BSIT", "year_level": 3, "term": 1, "total_students": 140},
            {"program": "BSIT", "year_level": 3, "term": 2, "total_students": 135},
            {"program": "BSIT", "year_level": 3, "term": 3, "total_students": 130},
            {"program": "BSIT", "year_level": 4, "term": 1, "total_students": 120},
            {"program": "BSIT", "year_level": 4, "term": 2, "total_students": 115},
            {"program": "BSIT", "year_level": 4, "term": 3, "total_students": 110},
        ]
        
        self.enrollments = pd.DataFrame(enrollments_data)
