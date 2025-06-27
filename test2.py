import json
import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os

SCOPES = ['https://www.googleapis.com/auth/calendar.events']

def create_event(summary, due_date_str):
    # Auth
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    # Attempt to interpret due_date_str
    today = datetime.date.today()
    date_lower = due_date_str.lower()

    # Handle vague strings
    if "thursday" in date_lower:
        days_ahead = (3 - today.weekday()) % 7  # 3 = Thursday
    elif "monday" in date_lower:
        days_ahead = (0 - today.weekday()) % 7  # 0 = Monday
    elif "next week" in date_lower:
        days_ahead = 7
    elif "immediate" in date_lower or "now" in date_lower:
        days_ahead = 0
    else:
        days_ahead = 2  # Default fallback

    due_date = today + datetime.timedelta(days=days_ahead)
    event_time = datetime.datetime.combine(due_date, datetime.time(10, 0)).isoformat()

    event = {
    'summary': summary,
    'start': {'date': due_date.isoformat(), 'timeZone': 'Europe/London'},
    'end': {'date': (due_date + datetime.timedelta(days=1)).isoformat(), 'timeZone': 'Europe/London'},
}


    created_event = service.events().insert(calendarId='primary', body=event).execute()
    print(f"✅ Created event: {created_event.get('htmlLink')}")

# === MAIN TEST ===
tasks_json = '''
[
  {
    "task": "Finalize product launch timeline",
    "person": "Tom (Project Manager)",
    "due_date": "Not explicitly mentioned, but implied to be completed during the meeting"
  },
  {
    "task": "Address integration issues in Engineering",
    "person": "Emily (Engineering Lead)",
    "due_date": "End of the next sprint"
  },
  {
    "task": "Ensure QA does not compromise on security during regression testing",
    "person": "Ravi (QA)",
    "due_date": "Immediately"
  },
  {
    "task": "Provide final list of supported integrations to Marketing",
    "person": "Emily (Engineering Lead)",
    "due_date": "Thursday EOD"
  },
  {
    "task": "Update sales enablement documents",
    "person": "Amir (Marketing)",
    "due_date": "Monday"
  },
  {
    "task": "Include Customer Success in next week’s meeting",
    "person": "Tom (Project Manager)",
    "due_date": "Next week"
  }
]
'''

task_list = json.loads(tasks_json)

for task in task_list:
    summary = f"{task['task']} — {task['person']}"
    due = task['due_date']
    create_event(summary, due)
