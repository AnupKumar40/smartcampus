"""
timetable_data.py - Smart Campus Timetable Data & Helper Functions
Defines the weekly academic timetable and helper methods to query classes by day.
"""

from datetime import datetime

WEEKLY_TIMETABLE = {
    "Monday": [
        {
            "time": "09:15 - 10:10",
            "start": "09:15",
            "end": "10:10",
            "subject": "Software Engineering",
            "teacher": "Mrs Deepti Saxena",
            "room": "CR - 21",
            "type": "Lecture"
        },
        {
            "time": "10:15 - 11:10",
            "start": "10:15",
            "end": "11:10",
            "subject": "Computer Architecture",
            "teacher": "Mr Amit Chaurasia",
            "room": "LT-21-B",
            "type": "Lecture"
        },
        {
            "time": "11:15 - 12:10",
            "start": "11:15",
            "end": "12:10",
            "subject": "Java Programming",
            "teacher": "Dr Sanjay Jain",
            "room": "CR - 24",
            "type": "Lecture"
        },
        {
            "time": "12:15 - 12:55",
            "start": "12:15",
            "end": "12:55",
            "subject": "Communication Skills-III",
            "teacher": "Ms Padmakshi Sharma",
            "room": "CR - 15",
            "type": "Lecture"
        },
        {
            "time": "14:00 - 14:55",
            "start": "14:00",
            "end": "14:55",
            "subject": "Open Elective (Biodiversity and Law)",
            "teacher": "Dr Suman Paliwal",
            "room": "LT-10",
            "type": "Elective"
        },
        {
            "time": "15:00 - 15:55",
            "start": "15:00",
            "end": "15:55",
            "subject": "German",
            "teacher": "Dr Raksha Gusain",
            "room": "CR - 12",
            "type": "Language"
        }
    ],
    "Tuesday": [
        {
            "time": "09:15 - 10:10",
            "start": "09:15",
            "end": "10:10",
            "subject": "Java Programming",
            "teacher": "Dr Sanjay Jain",
            "room": "CR - 24",
            "type": "Lecture"
        },
        {
            "time": "10:15 - 12:10",
            "start": "10:15",
            "end": "12:10",
            "subject": "Python Programming Lab",
            "teacher": "Dr Taranpreet Singh Ruprah",
            "room": "Lab - 3",
            "type": "Lab"
        },
        {
            "time": "13:00 - 13:55",
            "start": "13:00",
            "end": "13:55",
            "subject": "German",
            "teacher": "Dr Raksha Gusain",
            "room": "CR - 12",
            "type": "Language"
        },
        {
            "time": "14:00 - 14:55",
            "start": "14:00",
            "end": "14:55",
            "subject": "Software Engineering",
            "teacher": "Mrs Deepti Saxena",
            "room": "CR - 21",
            "type": "Lecture"
        },
        {
            "time": "15:00 - 15:55",
            "start": "15:00",
            "end": "15:55",
            "subject": "Open Elective (Biodiversity and Law)",
            "teacher": "Dr Suman Paliwal",
            "room": "LT-10",
            "type": "Elective"
        }
    ],
    "Wednesday": [
        {
            "time": "09:15 - 10:10",
            "start": "09:15",
            "end": "10:10",
            "subject": "Behavioural Science-V",
            "teacher": "Dr Neha Gupta",
            "room": "CR - 18",
            "type": "Value Added"
        },
        {
            "time": "11:15 - 12:10",
            "start": "11:15",
            "end": "12:10",
            "subject": "Computer Architecture",
            "teacher": "Mr Amit Chaurasia",
            "room": "LT-21-B",
            "type": "Lecture"
        },
        {
            "time": "13:00 - 13:55",
            "start": "13:00",
            "end": "13:55",
            "subject": "Python Programming",
            "teacher": "Dr Taranpreet Singh Ruprah",
            "room": "LT-22-B",
            "type": "Lecture"
        },
        {
            "time": "14:00 - 14:55",
            "start": "14:00",
            "end": "14:55",
            "subject": "Java Programming",
            "teacher": "Dr Sanjay Jain",
            "room": "CR - 24",
            "type": "Lecture"
        },
        {
            "time": "15:00 - 15:55",
            "start": "15:00",
            "end": "15:55",
            "subject": "Java Programming Lab",
            "teacher": "Dr Sanjay Jain",
            "room": "Lab - 1",
            "type": "Lab"
        },
        {
            "time": "16:00 - 16:55",
            "start": "16:00",
            "end": "16:55",
            "subject": "Computer Architecture Lab",
            "teacher": "Mr Amit Chaurasia",
            "room": "Lab - 2",
            "type": "Lab"
        }
    ],
    "Thursday": [
        {
            "time": "09:15 - 11:10",
            "start": "09:15",
            "end": "11:10",
            "subject": "Python Programming Lab",
            "teacher": "Dr Taranpreet Singh Ruprah",
            "room": "Lab - 3",
            "type": "Lab"
        },
        {
            "time": "11:15 - 12:10",
            "start": "11:15",
            "end": "12:10",
            "subject": "Software Engineering",
            "teacher": "Mrs Deepti Saxena",
            "room": "CR - 21",
            "type": "Lecture"
        },
        {
            "time": "13:00 - 13:55",
            "start": "13:00",
            "end": "13:55",
            "subject": "Open Elective (Biodiversity and Law)",
            "teacher": "Dr Suman Paliwal",
            "room": "LT-10",
            "type": "Elective"
        },
        {
            "time": "14:00 - 14:55",
            "start": "14:00",
            "end": "14:55",
            "subject": "Open Elective (Biodiversity and Law)",
            "teacher": "Dr Suman Paliwal",
            "room": "LT-10",
            "type": "Elective"
        },
        {
            "time": "15:00 - 15:55",
            "start": "15:00",
            "end": "15:55",
            "subject": "Computer Architecture Lab",
            "teacher": "Mr Amit Chaurasia",
            "room": "Lab - 2",
            "type": "Lab"
        },
        {
            "time": "16:00 - 16:55",
            "start": "16:00",
            "end": "16:55",
            "subject": "Software Engineering Lab",
            "teacher": "Mrs Deepti Saxena",
            "room": "Lab - 4",
            "type": "Lab"
        }
    ],
    "Friday": [
        {
            "time": "09:15 - 10:10",
            "start": "09:15",
            "end": "10:10",
            "subject": "Java Programming Lab",
            "teacher": "Dr Sanjay Jain",
            "room": "CR - 24",
            "type": "Lab"
        },
        {
            "time": "10:15 - 11:10",
            "start": "10:15",
            "end": "11:10",
            "subject": "Java Programming",
            "teacher": "Dr Sanjay Jain",
            "room": "CR - 24",
            "type": "Lecture"
        },
        {
            "time": "11:15 - 12:10",
            "start": "11:15",
            "end": "12:10",
            "subject": "Computer Architecture",
            "teacher": "Mr Amit Chaurasia",
            "room": "LT-21-B",
            "type": "Lecture"
        },
        {
            "time": "13:00 - 13:55",
            "start": "13:00",
            "end": "13:55",
            "subject": "Python Programming",
            "teacher": "Dr Taranpreet Singh Ruprah",
            "room": "LT-22-B",
            "type": "Lecture"
        }
    ],
    "Saturday": [],
    "Sunday": []
}

def get_class_status(start_time_str, end_time_str, is_today=True):
    """
    Returns the real-time status of a class:
    - 'ongoing' (Live Now)
    - 'completed' (Done)
    - 'upcoming' (Scheduled)
    """
    if not is_today:
        return "scheduled"
    
    now = datetime.now()
    cur_hm = now.strftime("%H:%M")
    
    if cur_hm < start_time_str:
        return "upcoming"
    elif start_time_str <= cur_hm <= end_time_str:
        return "ongoing"
    else:
        return "completed"

def get_dashboard_timetable_data():
    """
    Returns today's timetable info and all days timetable for the dashboard.
    """
    now = datetime.now()
    today_day = now.strftime("%A")  # 'Monday', 'Tuesday', etc.
    today_formatted = now.strftime("%A, %d %b %Y")
    
    is_weekend = today_day in ["Saturday", "Sunday"]
    
    # Enrich classes for today with real-time status
    today_classes = []
    raw_today = WEEKLY_TIMETABLE.get(today_day, [])
    for cls in raw_today:
        status = get_class_status(cls["start"], cls["end"], is_today=True)
        enriched = dict(cls)
        enriched["status"] = status
        today_classes.append(enriched)

    # Active day to show initially: if weekend, show Monday's schedule by default for preview, else today
    default_active_day = today_day if not is_weekend else "Monday"
    
    return {
        "today_day": today_day,
        "today_formatted": today_formatted,
        "is_weekend": is_weekend,
        "default_active_day": default_active_day,
        "today_classes": today_classes,
        "weekly_timetable": WEEKLY_TIMETABLE
    }
