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
# async def main():
#     llm = ChatModel.from_name(
#         "watsonx:ibm/granite-3-3-8b-instruct",
#         project_id="7a900cc3-a751-426f-881d-eb923da89638",
#         api_key=os.environ["IBM_API_KEY"]
#     )

#     workflow = AgentWorkflow(name="Meeting Transcript Analyzer")

#     workflow.add_agent(
#         name="Summarizer",
#         role="Summarizes meeting",
#         instructions="Summarize the transcript in 5 bullet points.",
#         llm=llm
#     )

#     workflow.add_agent(
#         name="TaskExtractor",
#         role="Extracts tasks",
#         instructions="""From the transcript, extract tasks in JSON format with task, person, due_date.""",
#         llm=llm
#     )

#     workflow.add_agent(
#         name="ToneAnalyzer",
#         role="Analyzes tone",
#         instructions="Evaluate tone and highlight inclusion, respect, or negativity.",
#         llm=llm
#     )

#     workflow.add_agent(
#         name="CultureScorer",
#         role="Rates team culture",
#         instructions="Score Inclusivity, Respect, Collaboration, Psychological Safety (1–5) with reasons and final verdict.",
#         llm=llm
#     )


#     input_text = f"{transcript}"
#     run = await workflow.run([AgentWorkflowInput(prompt=input_text)])

#     print(run.result)
#     print("######")
#     for agent_name, output in run.result:
#         print(f"\n📌 Agent: {agent_name}")
#         print("📝 Output:")
#         print(output)

# if __name__ == "__main__":
#     asyncio.run(main())
async def run_agent(agent_name, role, instructions, transcript, llm):
    workflow = AgentWorkflow(name=f"{agent_name} Workflow")
    workflow.add_agent(
        name=agent_name,
        role=role,
        instructions=instructions,
        llm=llm
    )
    result = await workflow.run([AgentWorkflowInput(prompt=transcript)])
    return result.result.final_answer  # safest for single-agent runs

# === MAIN ===
async def main():
    llm = ChatModel.from_name(
        "watsonx:ibm/granite-3-3-8b-instruct",
        project_id="7a900cc3-a751-426f-881d-eb923da89638",
        api_key=os.environ["IBM_API_KEY"]
    )

    # Run each agent one-by-one
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
        "Score Inclusivity, Respect, Collaboration, Psychological Safety (1–5) with reasons and final verdict.", transcript, llm
    )

    print("\n=== FINAL AGENT OUTPUTS ===")
    print("\n📌 Summary:\n", summary)
    print("\n📌 Tasks:\n", tasks)
    print("\n📌 Tone Analysis:\n", tone)
    print("\n📌 Culture Score:\n", culture)

    try:
     await llm.client.aclose()  # This explicitly closes the underlying HTTP session
    except Exception as e:
        print(f"Warning while closing session: {e}")
# === ENTRY POINT ===
if __name__ == "__main__":
    asyncio.run(main())

