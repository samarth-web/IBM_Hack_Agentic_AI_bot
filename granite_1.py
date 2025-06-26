import requests

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

iam_token = ""

agent_goal = """
Analyze the provided meeting transcript. Generate:
1. A summary in bullet points
2. A list of tasks with owners and due dates
3. Ethics and tone analysis
4. Team culture score
5. Automatically create the extracted tasks in the most accessible platform (Google Calendar, Jira, Notion, or Teams — prioritize Google Calendar if available).
"""

def summarizer():

    body = {
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"Summarize the following meeting transcript in bullet 5 points:{transcipt}"
                    }
                ]
            }
        ],
        "project_id": "7a900cc3-a751-426f-881d-eb923da89638",
        "model_id": "ibm/granite-3-3-8b-instruct",
        "frequency_penalty": 0,
        "max_tokens": 2000,
        "presence_penalty": 0,
        "temperature": 0,
        "top_p": 1
    }

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {iam_token}"
    }

    response = requests.post(
        url,
        headers=headers,
        json=body
    )

    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))

    data = response.json()
    return data

def task_allocation():
    body = {
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"""From the following meeting transcript, extract a list of tasks and who they are assigned to.
Return the output as a JSON with keys: "task", "person", and "due_date" (if any mentioned).

Transcript:
{transcipt}
"""
                    }
                ]
            }
        ],
        "project_id": "7a900cc3-a751-426f-881d-eb923da89638", 
        "model_id": "ibm/granite-3-3-8b-instruct",
        "frequency_penalty": 0,
        "max_tokens": 2000,
        "presence_penalty": 0,
        "temperature": 0,
        "top_p": 1
    }

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {iam_token}"
    }

    response = requests.post(
        url,
        headers=headers,
        json=body
    )

    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))

    return response.json()

def ethics():
    body = {
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"""Evaluate the tone and collaboration dynamics in the following meeting transcript. Highlight any moments that demonstrate inclusion, transparency, or respect, as well as any that indicate exclusion, opacity, or disrespect. Provide specific quotes with short explanations. Conclude with a brief summary of the overall team culture based on this interaction:

Transcript:
{transcipt}
"""
                    }
                ]
            }
        ],
        "project_id": "7a900cc3-a751-426f-881d-eb923da89638", 
        "model_id": "ibm/granite-3-3-8b-instruct",
        "frequency_penalty": 0,
        "max_tokens": 2000,
        "presence_penalty": 0,
        "temperature": 0,
        "top_p": 1
    }

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {iam_token}"
    }

    response = requests.post(
        url,
        headers=headers,
        json=body
    )

    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))

    return response.json()
    
def culture_compass():
    body = {
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"""From the following transcript, score the team’s culture on a scale of 1 to 5 for each of the following:

Inclusivity
Respect
Collaboration
Psychological Safety
Give a 1–2 line explanation per score.

Then, calculate a final culture score (average of the 4) and include a short verdict like:

Excellent culture
Good
Needs attention
Poor culture

Transcript:
{transcipt}
"""
                    }
                ]
            }
        ],
        "project_id": "7a900cc3-a751-426f-881d-eb923da89638", 
        "model_id": "ibm/granite-3-3-8b-instruct",
        "frequency_penalty": 0,
        "max_tokens": 2000,
        "presence_penalty": 0,
        "temperature": 0,
        "top_p": 1
    }

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {iam_token}"
    }

    response = requests.post(
        url,
        headers=headers,
        json=body
    )

    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))

    return response.json()


print(task_allocation())