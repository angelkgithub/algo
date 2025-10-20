# Overview

This is a class scheduling system built with Streamlit that automates the generation of academic schedules for university programs. The application takes enrollment data, course information, room availability, and faculty details to create conflict-free class schedules. It supports multiple degree programs (BSIT, BSCS, BSIS) and handles both lecture and laboratory courses with flexible time slot assignments.

# Recent Changes

**October 1, 2025**: Configured project for Replit environment and updated scheduling algorithm
- Set up Python 3.11 with dependencies (streamlit, pandas, numpy, openpyxl)
- Configured Streamlit to run on port 5000 with host 0.0.0.0 for Replit proxy compatibility
- Added .streamlit/config.toml with server settings to allow all hosts
- Created .gitignore for Python project structure
- Configured workflow to automatically run the Streamlit app on startup
- **Updated scheduling algorithm** to split classes across two specific days:
  - Lecture classes (3 hrs/week): Split into 1.5 hour sessions
  - Lab classes (2+ hrs/week): Split into balanced sessions
  - Day pairings: Monday-Thursday, Tuesday-Friday, or Wednesday-Saturday
  - Maintains conflict detection to avoid scheduling overlaps
- **Implemented even distribution mechanism**:
  - Added rotation system to distribute courses evenly across all three day pairs
  - Prevents clustering on specific day pairings (e.g., all courses on Monday-Thursday)
  - Maximizes room utilization throughout the entire week
  - Counter-based rotation ensures deterministic scheduling across runs

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