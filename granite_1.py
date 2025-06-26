import requests
import os
import asyncio
#from beeai.agents import ReActAgent
from beeai_framework.backend.chat import ChatModel
from datetime import datetime
from beeai_framework.workflows.agent import AgentWorkflow, AgentWorkflowInput


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

iam_token = "eyJraWQiOiIyMDE5MDcyNCIsImFsZyI6IlJTMjU2In0.eyJpYW1faWQiOiJJQk1pZC02OTMwMDBaQjU2IiwiaWQiOiJJQk1pZC02OTMwMDBaQjU2IiwicmVhbG1pZCI6IklCTWlkIiwianRpIjoiNmQ0ZDZiMGYtN2I3Yi00YjEyLWJhMjctNzExNTI0MzNhMDJjIiwiaWRlbnRpZmllciI6IjY5MzAwMFpCNTYiLCJnaXZlbl9uYW1lIjoiU2FtYXJ0aCIsImZhbWlseV9uYW1lIjoiSmFpbiIsIm5hbWUiOiJTYW1hcnRoIEphaW4iLCJlbWFpbCI6InNhbWFydGhqMjA0QGdtYWlsLmNvbSIsInN1YiI6InNhbWFydGhqMjA0QGdtYWlsLmNvbSIsImF1dGhuIjp7InN1YiI6InNhbWFydGhqMjA0QGdtYWlsLmNvbSIsImlhbV9pZCI6IklCTWlkLTY5MzAwMFpCNTYiLCJuYW1lIjoiU2FtYXJ0aCBKYWluIiwiZ2l2ZW5fbmFtZSI6IlNhbWFydGgiLCJmYW1pbHlfbmFtZSI6IkphaW4iLCJlbWFpbCI6InNhbWFydGhqMjA0QGdtYWlsLmNvbSJ9LCJhY2NvdW50Ijp7InZhbGlkIjp0cnVlLCJic3MiOiJlOTUzZDEwYzg1Yzk0MjIyOGMyYTMyNDQ0ZDkyZjAxNyIsImltc191c2VyX2lkIjoiMTM4OTkxNzciLCJmcm96ZW4iOnRydWUsImltcyI6IjI5OTg2NzQifSwibWZhIjp7ImltcyI6dHJ1ZX0sImlhdCI6MTc1MDk2NTE5MiwiZXhwIjoxNzUwOTY4NzkyLCJpc3MiOiJodHRwczovL2lhbS5jbG91ZC5pYm0uY29tL2lkZW50aXR5IiwiZ3JhbnRfdHlwZSI6InVybjppYm06cGFyYW1zOm9hdXRoOmdyYW50LXR5cGU6YXBpa2V5Iiwic2NvcGUiOiJpYm0gb3BlbmlkIiwiY2xpZW50X2lkIjoiZGVmYXVsdCIsImFjciI6MSwiYW1yIjpbInB3ZCJdfQ.j9UKwqel9PDl4QKSZoZKy8koCYAfH7LYv6cQhzI_wq6uyEDwDk11Vt40HURL9G_JUgAR4qEQ8HZCAEjNHoXf5S-I1Z8ov_KtkiyBoD_N3to_PU7YEqPOSrk8CagDInkwoY9RBWYfpIvf8ZBLnMu0sZJkI2Ku1Ow6MmVC--M_N5uxWz_WUeZ5qpQMpE3u6o8dlm8HTBXZYRXR6uR7gGAgsjzeflByvLV5sFFxJVkPRSV5rhIT7UlwdCO0X6JyM7PrAfcwQkyp-zhbpfqXsSFrRUwDwgLkIz_wZfWIX5KWtqsNztSthbuEWoO2TGOH0x1hlnuWk98D-ejRtGU2IV6THA"
os.environ["IBM_API_KEY"] = iam_token
agent_goal = """
Analyze the provided meeting transcript. Generate:
1. A summary in bullet points
2. A list of tasks with owners and due dates
3. Ethics and tone analysis
4. Team culture score
5. Automatically create the extracted tasks in the most accessible platform (Google Calendar, Jira, Notion, or Teams — prioritize Google Calendar if available).
"""

# def summarizer():

#     body = {
#         "messages": [
#             {
#                 "role": "user",
#                 "content": [
#                     {
#                         "type": "text",
#                         "text": f"Summarize the following meeting transcript in bullet 5 points:{transcipt}"
#                     }
#                 ]
#             }
#         ],
#         "project_id": "7a900cc3-a751-426f-881d-eb923da89638",
#         "model_id": "ibm/granite-3-3-8b-instruct",
#         "frequency_penalty": 0,
#         "max_tokens": 2000,
#         "presence_penalty": 0,
#         "temperature": 0,
#         "top_p": 1
#     }

#     headers = {
#         "Accept": "application/json",
#         "Content-Type": "application/json",
#         "Authorization": f"Bearer {iam_token}"
#     }

#     response = requests.post(
#         url,
#         headers=headers,
#         json=body
#     )

#     if response.status_code != 200:
#         raise Exception("Non-200 response: " + str(response.text))

#     data = response.json()
#     return data

# def task_allocation():
#     body = {
#         "messages": [
#             {
#                 "role": "user",
#                 "content": [
#                     {
#                         "type": "text",
#                         "text": f"""From the following meeting transcript, extract a list of tasks and who they are assigned to.
# Return the output as a JSON with keys: "task", "person", and "due_date" (if any mentioned).

# Transcript:
# {transcipt}
# """
#                     }
#                 ]
#             }
#         ],
#         "project_id": "7a900cc3-a751-426f-881d-eb923da89638", 
#         "model_id": "ibm/granite-3-3-8b-instruct",
#         "frequency_penalty": 0,
#         "max_tokens": 2000,
#         "presence_penalty": 0,
#         "temperature": 0,
#         "top_p": 1
#     }

#     headers = {
#         "Accept": "application/json",
#         "Content-Type": "application/json",
#         "Authorization": f"Bearer {iam_token}"
#     }

#     response = requests.post(
#         url,
#         headers=headers,
#         json=body
#     )

#     if response.status_code != 200:
#         raise Exception("Non-200 response: " + str(response.text))

#     return response.json()

# def ethics():
#     body = {
#         "messages": [
#             {
#                 "role": "user",
#                 "content": [
#                     {
#                         "type": "text",
#                         "text": f"""Evaluate the tone and collaboration dynamics in the following meeting transcript. Highlight any moments that demonstrate inclusion, transparency, or respect, as well as any that indicate exclusion, opacity, or disrespect. Provide specific quotes with short explanations. Conclude with a brief summary of the overall team culture based on this interaction:

# Transcript:
# {transcipt}
# """
#                     }
#                 ]
#             }
#         ],
#         "project_id": "7a900cc3-a751-426f-881d-eb923da89638", 
#         "model_id": "ibm/granite-3-3-8b-instruct",
#         "frequency_penalty": 0,
#         "max_tokens": 2000,
#         "presence_penalty": 0,
#         "temperature": 0,
#         "top_p": 1
#     }

#     headers = {
#         "Accept": "application/json",
#         "Content-Type": "application/json",
#         "Authorization": f"Bearer {iam_token}"
#     }

#     response = requests.post(
#         url,
#         headers=headers,
#         json=body
#     )

#     if response.status_code != 200:
#         raise Exception("Non-200 response: " + str(response.text))

#     return response.json()
    
# def culture_compass():
#     body = {
#         "messages": [
#             {
#                 "role": "user",
#                 "content": [
#                     {
#                         "type": "text",
#                         "text": f"""From the following transcript, score the team’s culture on a scale of 1 to 5 for each of the following:

# Inclusivity
# Respect
# Collaboration
# Psychological Safety
# Give a 1–2 line explanation per score.

# Then, calculate a final culture score (average of the 4) and include a short verdict like:

# Excellent culture
# Good
# Needs attention
# Poor culture

# Transcript:
# {transcipt}
# """
#                     }
#                 ]
#             }
#         ],
#         "project_id": "7a900cc3-a751-426f-881d-eb923da89638", 
#         "model_id": "ibm/granite-3-3-8b-instruct",
#         "frequency_penalty": 0,
#         "max_tokens": 2000,
#         "presence_penalty": 0,
#         "temperature": 0,
#         "top_p": 1
#     }

#     headers = {
#         "Accept": "application/json",
#         "Content-Type": "application/json",
#         "Authorization": f"Bearer {iam_token}"
#     }

#     response = requests.post(
#         url,
#         headers=headers,
#         json=body
#     )

#     if response.status_code != 200:
#         raise Exception("Non-200 response: " + str(response.text))

#     return response.json()
llm = ChatModel.from_name("watsonx:ibm/granite-3-3-8b-instruct",
                          project_id="7a900cc3-a751-426f-881d-eb923da89638", 
                          api_key=iam_token )




workflow = AgentWorkflow(name="Meeting Transcript Analyzer")
workflow.add_agent(
    name="Summarizer",
    role="A concise summarizer.",
    instructions="Summarize the transcript in 5 clear bullet points.",
    llm=llm
)


workflow.add_agent(
    name="TaskExtractor",
    role="Task extraction agent.",
    instructions=""""
From the transcript, extract tasks in JSON format:
[
  {"task": "...", "person": "...", "due_date": "..."},
  ...
]
""",
    
    llm=llm
)


workflow.add_agent(
    name="ToneAnalyzer",
    role="Ethics and tone evaluator.",
    instructions="""
        Evaluate tone and collaboration dynamics. Highlight inclusion, transparency, respect.
        Also identify exclusion, opacity, or disrespect with quotes and short explanations.
    """,
    llm=llm
)


workflow.add_agent(
    name="CultureScorer",
    role="Culture rating assistant.",
    instructions="""
        Score the team on: Inclusivity, Respect, Collaboration, Psychological Safety (1-5).
        Give short explanations and an overall verdict.
    """,
    llm=llm
)


# workflow.add_agent(
#     name="TaskScheduler",
#     role="Calendar automation assistant.",
#     instructions="""
#         Take the previously extracted tasks and create events in Google Calendar (if due dates present).
#         If not possible, suggest fallback like Jira or Notion.
#     """,
#     tools=[GoogleCalendarTool()],
#     llm=llm
# )
transcript = transcipt
inputs = [
    AgentWorkflowInput(prompt=f"Summarize this transcript:\n{transcript}"),
    AgentWorkflowInput(prompt=f"Extract tasks from this transcript:\n{transcript}"),
    AgentWorkflowInput(prompt=f"Analyze tone and collaboration in this transcript:\n{transcript}"),
    AgentWorkflowInput(prompt=f"Score team culture based on this transcript:\n{transcript}"),
    #AgentWorkflowInput(prompt="Use the extracted tasks to schedule calendar events.")
]

response = workflow.run(inputs).on(
    "success", lambda data, event: print(f"\n✅ Step '{data.step}' completed.\n{data.state.final_answer}")
)
first_task = response._tasks[0]
print("=== Final Result ===")
print(first_task)
