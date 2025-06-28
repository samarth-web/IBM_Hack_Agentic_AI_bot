import json
import re
import requests
import os
import asyncio
#from beeai.agents import ReActAgent
from beeai_framework.backend.chat import ChatModel
from datetime import datetime
from beeai_framework.workflows.agent import AgentWorkflow, AgentWorkflowInput
import json
import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os
import matplotlib.pyplot as plt
import plotly.graph_objects as go



url = "https://us-south.ml.cloud.ibm.com/ml/v1/text/chat?version=2023-05-29"
transcipt = """Meeting Transcript: Product Launch Timeline Finalization


Tom (Project Manager):
Alright folks, let’s jump in. Our goal today is to finalize the product launch timeline. First update – Engineering flagged a delay due to integration issues.

Emily (Engineering Lead):
Yes, we underestimated the complexity of the backend connector. We’ll need one more sprint.

Tom:
That’s frustrating, but okay. Can you ensure the fix doesn’t affect the launch?

Emily:
We’ll do our best, but it depends on QA’s bandwidth.

Ravi (QA):
We’re already behind on regression testing. We can try, but I’ll need Priya full-time on this.

Tom:
Yeah… let’s prioritize. Emily, please loop Priya in. We don’t need everyone chasing edge cases.

Priya (QA):
Sorry, but I don’t think we should cut corners. This affects security.

Tom:
Noted, but let’s be practical.

Amir (Marketing):
From our side, the assets are 90% ready. I just need Engineering to give me the final list of supported integrations by Friday.

Tom:
Emily?

Emily:
We’ll get it to you by Thursday EOD.

Tom:
Great. Amir, please also update the sales enablement documents by Monday.

Amir:
Sure.

Tom:
Alright, unless someone has blockers, I think we’re done.

Emily:
One quick thing — I think we should include Customer Success in next week’s meeting.

Tom:
I don’t think it’s necessary. They’ll get the docs.

Ravi:
They raised issues last week that weren’t captured.

Tom:
Okay, fine. Invite one rep. Let’s not overcomplicate this."""

iam_token = "eyJraWQiOiIyMDE5MDcyNCIsImFsZyI6IlJTMjU2In0.eyJpYW1faWQiOiJJQk1pZC02OTMwMDBaQjU2IiwiaWQiOiJJQk1pZC02OTMwMDBaQjU2IiwicmVhbG1pZCI6IklCTWlkIiwianRpIjoiMGU3YzJjMmQtNTdlMy00MjBiLTlkODUtMzA1M2IyZWQ5Mzg3IiwiaWRlbnRpZmllciI6IjY5MzAwMFpCNTYiLCJnaXZlbl9uYW1lIjoiU2FtYXJ0aCIsImZhbWlseV9uYW1lIjoiSmFpbiIsIm5hbWUiOiJTYW1hcnRoIEphaW4iLCJlbWFpbCI6InNhbWFydGhqMjA0QGdtYWlsLmNvbSIsInN1YiI6InNhbWFydGhqMjA0QGdtYWlsLmNvbSIsImF1dGhuIjp7InN1YiI6InNhbWFydGhqMjA0QGdtYWlsLmNvbSIsImlhbV9pZCI6IklCTWlkLTY5MzAwMFpCNTYiLCJuYW1lIjoiU2FtYXJ0aCBKYWluIiwiZ2l2ZW5fbmFtZSI6IlNhbWFydGgiLCJmYW1pbHlfbmFtZSI6IkphaW4iLCJlbWFpbCI6InNhbWFydGhqMjA0QGdtYWlsLmNvbSJ9LCJhY2NvdW50Ijp7InZhbGlkIjp0cnVlLCJic3MiOiJlOTUzZDEwYzg1Yzk0MjIyOGMyYTMyNDQ0ZDkyZjAxNyIsImltc191c2VyX2lkIjoiMTM4OTkxNzciLCJmcm96ZW4iOnRydWUsImltcyI6IjI5OTg2NzQifSwibWZhIjp7ImltcyI6dHJ1ZX0sImlhdCI6MTc1MTA0Mjc1OSwiZXhwIjoxNzUxMDQ2MzU5LCJpc3MiOiJodHRwczovL2lhbS5jbG91ZC5pYm0uY29tL2lkZW50aXR5IiwiZ3JhbnRfdHlwZSI6InVybjppYm06cGFyYW1zOm9hdXRoOmdyYW50LXR5cGU6YXBpa2V5Iiwic2NvcGUiOiJpYm0gb3BlbmlkIiwiY2xpZW50X2lkIjoiZGVmYXVsdCIsImFjciI6MSwiYW1yIjpbInB3ZCJdfQ.Q69Sw3E-quoTKGYpKkSPzPVRNqk-U3G6NSzPXkKAky6k5RPzZiFKSZaQuTUeCOXfs_tkmG80SjqefDdPqbe9WeyT98BZMwedh9767m795B8feCBJp5RR_tZQcZVz-3lhq_RDTHCc615Pq__-QwLoVJPTDq69dk77kJ5rRM8kDfdGIGhwJbxbCDppdAU3YLGw_Df9d_xE7ci7suTDmyo_y07_qFEGls4gCl9E7IW7q7lNol4h-qVbulcNZuHpGji8ZnGnUJoRbMnEtguXsr3sAxl4fTChIxiI3zJrgZfOMTCLzFPo8F1bwHHQ4JFpsXQTepyGbcDbtlmhEU_Xu3MvJg"
os.environ["IBM_API_KEY"] = "tj2HifWLSjTPrAyxgL8SLh5m4QKC2Tm6qk1xbLDHgw0L"
agent_goal = """
Analyze the provided meeting transcript. Generate:
1. A summary in bullet points
2. A list of tasks with owners and due dates
3. Ethics and tone analysis
4. Team culture score
5. Automatically create the extracted tasks in the most accessible platform (Google Calendar, Jira, Notion, or Teams — prioritize Google Calendar if available).
"""


transcript = transcipt

SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/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"

API_KEY = "98ba5fac32841e02dc31ce69994ceefb"
TOKEN = "ATTA3de43fcdffa9256748f9cb858565555175358f99eeebfd2312e56796866467fd79DAD6BF"
BOARD_ID = "HU04NoGx"
LIST_NAME = "To Do"
SCOPES = ['https://www.googleapis.com/auth/calendar.events']


def extract_sentiments(json_str):
    try:
        match = re.search(r'\[.*\]', json_str, re.DOTALL)
        if match:
            json_str = match.group(0)
            return json.loads(json_str)
        else:
            print("No JSON array found. Using empty list.")
            return []
    except Exception as e:
        print("JSON parse error:", e)
        return []

def create_event(summary, due_date_str):
    
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

  
    today = datetime.date.today()
    date_lower = due_date_str.lower()

   
    if "thursday" in date_lower:
        days_ahead = (3 - today.weekday()) % 7  
    elif "monday" in date_lower:
        days_ahead = (0 - today.weekday()) % 7  
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
    print(f" Created event: {created_event.get('htmlLink')}")





def get_list_id(board_id, list_name):
    url = f"https://api.trello.com/1/boards/{board_id}/lists"
    params = {"key": API_KEY, "token": TOKEN}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        for lst in response.json():
            if lst['name'].lower() == list_name.lower():
                return lst['id']
        print(" List not found.")
    else:
        print("Failed to fetch lists:", response.text)
    return None

def create_trello_card(list_id, name, desc):
    url = "https://api.trello.com/1/cards"
    query = {
        'key': API_KEY,
        'token': TOKEN,
        'idList': list_id,
        'name': name,
        'desc': desc
    }
    response = requests.post(url, params=query)
    if response.status_code == 200:
        print(" Card created:", response.json()["url"])
    else:
        print("Failed to create card:", response.text)




def send_slack_message(text):
    payload = {
        "text": text
    }
    response = requests.post(SLACK_WEBHOOK_URL, json=payload)

    if response.status_code == 200:
        print("Sent Slack message")
    else:
        print(f" Slack error: {response.status_code} {response.text}")



async def run_agent(agent_name, role, instructions, transcript, llm):
    workflow = AgentWorkflow(name=f"{agent_name} Workflow")
    workflow.add_agent(
        name=agent_name,
        role=role,
        instructions=instructions,
        llm=llm
    )
    result = await workflow.run([AgentWorkflowInput(prompt=transcript)])
    return result.result.final_answer  


async def main():
    llm = ChatModel.from_name(
        "watsonx:ibm/granite-3-3-8b-instruct",
        project_id="7a900cc3-a751-426f-881d-eb923da89638",
        api_key=os.environ["IBM_API_KEY"]
    )

    
    summary = await run_agent(
        "Summarizer", "Summarizes meeting", 
        "Summarize the transcript in 5 bullet points.", transcript, llm
    )
    
    tasks = await run_agent(
        "TaskExtractor", "Extracts tasks", 
        "From the transcript, extract tasks in JSON format with task, person, due_date.", transcript, llm
        
    )
    
    tone = await run_agent(
        "ToneAnalyzer", "Analyzes tone",
        "Evaluate tone and highlight inclusion, respect, or negativity.", transcript, llm
    )
    
    culture = await run_agent(
        "CultureScorer", "Rates team culture",
        "Score Inclusivity, Respect, Collaboration, Psychological Safety (1–5) with reasons and final verdict." "Provide 2-3 specific, practical recommendations for how the team could improve its weakest areas.", transcript, llm
    )

    ethics = await run_agent(
        "EthicsChecker",
        "Flags risky language",
    (
            "Scan the transcript for any non-inclusive, offensive, or risky language. "
            "Highlight specific phrases, give context, and classify severity (Low/Medium/High). "
            "Provide an overall ethics compliance verdict."
    ),
    transcript,
    llm
    )
    sentiment_chunks = await run_agent(
       
        "SentimentChunker",
        "Chunk-level sentiment analyzer",
        (
            "Split the transcript into meaningful chunks (like paragraphs or speaker turns). "
            "For each chunk, analyze sentiment and output ONLY a valid JSON array like this:\n\n"
            "[\n"
            "  {\n"
            "    \"chunk_id\": 1,\n"
            "    \"text_excerpt\": \"short excerpt text\",\n"
            "    \"speaker\": \"Tom\",\n"
            "    \"sentiment\": 0.2\n"
            "  },\n"
            "  ...\n"
            "]\n\n"
            "Sentiment should be a float between -1 (very negative) and 1 (very positive). "
            "DO NOT add any commentary or explanation — return ONLY the JSON array."
        ),
        transcript,
        llm
    )

  

   

    print("\n=== FINAL AGENT OUTPUTS ===")
    print("\n Summary:\n", summary)
    print("\n Tasks:\n", tasks)
    print("\n Tone Analysis:\n", tone)
    print("\n Culture Score:\n", culture)
    print("\n=== Ethics Check ===\n", ethics)
    culture_data = json.loads(culture)

    def extract_json_array(text):
       
        match = re.search(r'\[.*\]', text, re.DOTALL)
        if match:
            return match.group(0)
        else:
            return '[]'  
    try:
        tasks_json_str = extract_json_array(tasks)
        tasks_list = json.loads(tasks_json_str)
    except Exception as e:
        print("Could not parse tasks JSON:", e)
        tasks_list = []

   
    # list_id = get_list_id(BOARD_ID, LIST_NAME)
    # if list_id:
    #     for task in tasks_list:
    #         summary = task["task"]
    #         desc = f"Owner: {task['person']}, Due: {task['due_date']}"
    #         create_trello_card(list_id, summary, desc)
    # else:
    #     print(" Could not find Trello list.")
    # if tasks_list:
    #     slack_text = "*Tasks Extracted:*\n"
    #     for t in tasks_list:
    #         slack_text += f"- {t['task']} (Owner: {t['person']}, Due: {t['due_date']})\n"
    # else:
    #     slack_text = " No tasks extracted."
    # send_slack_message(slack_text)  
    
    # for task in tasks_list:
    #     summary = f"{task['task']} — {task['person']}"
    #     due = task['due_date']
    #     create_event(summary, due)
    #print("sentimental_chunks: ", sentiment_chunks)
    chunks = extract_sentiments(sentiment_chunks)
    scores = [c["sentiment"] for c in chunks]
    ids = [c["chunk_id"] for c in chunks]
    person = [c["speaker"]for c in chunks]

    # plt.plot(ids, scores, marker='o')
    # plt.title("Meeting Sentiment Timeline")
    # plt.xlabel("Chunk")
    # plt.ylabel("Sentiment Score")
    # plt.ylim(-1, 1)
    # plt.grid(True)
    # plt.savefig("sentiment_timeline.png")
    # print("Sentiment timeline chart saved: sentiment_timeline.png")
    

    fig = go.Figure()
    hover_text = [
    f"Speaker: {c['speaker']}<br>Text: {c['text_excerpt']}<br>Sentiment: {c['sentiment']}"
    for c in chunks
]

    fig.add_trace(go.Scatter(
        x=ids,
        y=scores,
        mode='lines+markers',
        marker=dict(size=10),
        text=hover_text, 

        hoverinfo='text+y',
    ))

    fig.update_layout(
        title="Meeting Sentiment Timeline",
        xaxis_title="Chunk",
        yaxis_title="Sentiment Score",
        yaxis=dict(range=[-1, 1]),
    )

    
    fig.write_html("sentiment_timeline.html")
    print("Interactive chart saved as sentiment_timeline.html")

    try:
     await llm.client.aclose()  
    except Exception as e:
        print(f"Warning while closing session: {e}")
    

# === ENTRY POINT ===
if __name__ == "__main__":
    asyncio.run(main())

