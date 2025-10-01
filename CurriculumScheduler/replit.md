# Overview

This is a class scheduling system built with Streamlit that automates the generation of academic schedules for university programs. The application takes enrollment data, course information, room availability, and faculty details to create conflict-free class schedules. It supports multiple degree programs (BSIT, BSCS, BSIS) and handles both lecture and laboratory courses with flexible time slot assignments.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture
- **Streamlit Web Interface**: Single-page application built with Streamlit for the user interface
- **Session State Management**: Uses Streamlit's session state to maintain data persistence across user interactions
- **CSV Data Loading**: Automatic loading of CSV files on application startup from the `data/` directory
- **Interactive Data Management**: Real-time data validation and display of courses, rooms, faculty, and enrollment information

## Backend Architecture
- **Model-Based Design**: Separation of concerns with dedicated model classes for scheduling logic and data management
- **DataManager Class**: Centralized data handling with validation for courses, rooms, faculty, and enrollment data
- **ClassScheduler Class**: Core scheduling algorithm implementation with support for different scheduling strategies
- **Utility Functions**: Helper functions for section generation, CSV validation, and conflict detection

## Data Processing
- **Section Generation Algorithm**: Automatically divides students into sections of 12-40 students with alphabetic naming (e.g., BSIT1A, BSIT1B)
- **Time Slot Management**: 30-minute interval scheduling from 7:00 AM to 9:00 PM, Monday through Saturday
- **Scheduling Rules Engine**: 
  - Pure lecture courses: 2 hours × 2 days or 4 hours once per week
  - Lecture+Lab courses: Separate scheduling for lecture and lab components
  - Faculty load constraints: Full-time (≥24 hrs/week), Part-time (≤18 hrs/week)

## Data Storage
- **CSV File-Based Storage**: Uses local CSV files for data persistence
- **In-Memory Processing**: DataFrame-based data manipulation using pandas
- **Data Validation**: Built-in validation for all CSV file formats and data integrity

# External Dependencies

## Core Libraries
- **Streamlit**: Web application framework for the user interface
- **Pandas**: Data manipulation and analysis for handling CSV data and scheduling operations
- **NumPy**: Numerical computing support for data processing algorithms

## Data Sources
- **CSV Files**: 
  - `data/courses.csv`: Course catalog with program, year, term, and hour requirements
  - `data/rooms.csv`: Room inventory with capacity, type, and availability
  - `data/faculty.csv`: Faculty information with employment type and availability
  - `data/enrollments.csv`: Student enrollment numbers by program and year

## File System
- **Local File Storage**: CSV files stored in the `data/` directory
- **Comment Filtering**: Automatic filtering of comment lines starting with '#' in CSV files
- **Error Handling**: Graceful handling of missing or corrupted CSV files