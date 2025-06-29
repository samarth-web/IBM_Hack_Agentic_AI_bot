from dotenv import load_dotenv
load_dotenv()
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


agent_goal = """
Analyze the provided meeting transcript. Generate:
1. A summary in bullet points
2. A list of tasks with owners and due dates
3. Ethics and tone analysis
4. Team culture score
5. Automatically create the extracted tasks in the most accessible platform (Google Calendar, Jira, Notion, or Teams — prioritize Google Calendar if available).
"""


transcript = transcipt
iam_token = os.environ["IAM_TOKEN"]
os.environ["IBM_API_KEY"] = os.environ["IBM_API_KEY"]

SLACK_WEBHOOK_URL = os.environ["SLACK_WEBHOOK_URL"]

API_KEY = os.environ["TRELLO_API_KEY"]
TOKEN = os.environ["TRELLO_TOKEN"]
BOARD_ID = os.environ["BOARD_ID"]
LIST_NAME = os.environ["LIST_NAME"]

SCOPES = [os.environ["GOOGLE_SCOPES"]]




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
        creds = Credentials.from_authorized_user_file('secrets/token.json', SCOPES)
    else:
        flow = InstalledAppFlow.from_client_secrets_file('secrets/credentials.json', SCOPES)
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
    "CultureScorer",
    "Rates team culture",
    (
        "You are an AI that ONLY returns valid JSON. No intro, no explanation.\n"
        "Read the meeting transcript and score the team on these 4 culture pillars: Inclusivity, Respect, Collaboration, Psychological_Safety.\n"
        "Each must be an integer from 1 to 5.\n"
        "Also add a short 'Verdict' string and a 'Recommendations' list with 2–3 practical actions.\n\n"
        "STRICT FORMAT:\n"
        "{\n"
        "  \"Inclusivity\": 2,\n"
        "  \"Respect\": 2,\n"
        "  \"Collaboration\": 2,\n"
        "  \"Psychological_Safety\": 1,\n"
        "  \"Verdict\": \"Short verdict sentence.\",\n"
        "  \"Recommendations\": [\n"
        "    \"Action 1.\",\n"
        "    \"Action 2.\",\n"
        "    \"Action 3.\"\n"
        "  ]\n"
        "}\n"
        "⚡ If you’re unsure, return: {} — do not explain anything."
    ),
    transcript,
    llm
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
    def extract_json_array(text):
       
        match = re.search(r'\[.*\]', text, re.DOTALL)
        if match:
            return match.group(0)
        else:
            return '[]'  
    def extract_json_object(text):
        print("\n=== RAW CULTURE OUTPUT ===")
        print(repr(text))

        # Replace smart quotes
        text = text.replace('“', '"').replace('”', '"').replace("‘", "'").replace("’", "'")

        # Remove code fences if they slip in
        text = text.strip().strip('`').strip('json').strip()

        # Extract JSON object
        match = re.search(r'\{[\s\S]*\}', text)
        if match:
            try:
                return json.loads(match.group(0))
            except json.JSONDecodeError as e:
                print("❌ JSON decoding failed:", e)
                return {}
        else:
            print("❌ No JSON object found. Returning empty dict.")
            return {}
 
    culture_data = extract_json_object(culture)
    print("\nParsed Culture JSON:", culture_data)
    categories = ["Inclusivity", "Respect", "Collaboration", "Psychological Safety"]
    categories = ["Inclusivity", "Respect", "Collaboration", "Psychological Safety"]
    scores = [
        culture_data.get("Inclusivity", 0),
        culture_data.get("Respect", 0),
        culture_data.get("Collaboration", 0),
        culture_data.get("Psychological_Safety", 0)
    ]

    # Close the loop on radar chart
    scores += [scores[0]]  # Radar needs first point repeated to close the shape
    categories += [categories[0]]

    # Build the radar chart
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=scores,
        theta=categories,
        fill='toself',
        name='Culture Scores',
        hovertemplate='%{theta}: %{r}/5'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5]
            )
        ),
        showlegend=False,
        title="Team Culture Score Radar Chart"
    )

    # Save the interactive HTML
    fig.write_html("culture_score.html")
    print("Interactive Culture Score saved: culture_score.html")

    # ✅ Optional: print recommendations for your site text
    print("\nVerdict:", culture_data.get("Verdict", ""))
    print("\nRecommendations:")
    for rec in culture_data.get("Recommendations", []):
        print("-", rec)

    
    try:
        tasks_json_str = extract_json_array(tasks)
        tasks_list = json.loads(tasks_json_str)
    except Exception as e:
        print("Could not parse tasks JSON:", e)
        tasks_list = []

   
    list_id = get_list_id(BOARD_ID, LIST_NAME)
    if list_id:
        for task in tasks_list:
            summary = task["task"]
            desc = f"Owner: {task['person']}, Due: {task['due_date']}"
            create_trello_card(list_id, summary, desc)
    else:
        print(" Could not find Trello list.")
    if tasks_list:
        slack_text = "*Tasks Extracted:*\n"
        for t in tasks_list:
            slack_text += f"- {t['task']} (Owner: {t['person']}, Due: {t['due_date']})\n"
    else:
        slack_text = " No tasks extracted."
    send_slack_message(slack_text)  
    
    for task in tasks_list:
        summary = f"{task['task']} — {task['person']}"
        due = task['due_date']
        create_event(summary, due)
    print("sentimental_chunks: ", sentiment_chunks)
    chunks = extract_sentiments(sentiment_chunks)
    scores_1 = [c["sentiment"] for c in chunks]
    ids = [c["chunk_id"] for c in chunks]
    person = [c["speaker"]for c in chunks]

    plt.plot(ids, scores_1, marker='o')
    plt.title("Meeting Sentiment Timeline")
    plt.xlabel("Chunk")
    plt.ylabel("Sentiment Score")
    plt.ylim(-1, 1)
    plt.grid(True)
    plt.savefig("sentiment_timeline.png")
    print("Sentiment timeline chart saved: sentiment_timeline.png")
    

    fig = go.Figure()
    hover_text = [
    f"Speaker: {c['speaker']}<br>Text: {c['text_excerpt']}<br>Sentiment: {c['sentiment']}"
    for c in chunks
]

    fig.add_trace(go.Scatter(
        x=ids,
        y=scores_1,
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

   

 
if __name__ == "__main__":
    asyncio.run(main())

