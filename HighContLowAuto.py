import os
from dotenv import load_dotenv, find_dotenv
from anthropic import  Anthropic
import json
from datetime import datetime

# ---------- High Control, Low Autonomy: Project Status Report --------------------------------------------------------

#Define the system prompt
system_prompt = """
You are an AI assistant guiding users through a simplified project status report process. Follow these steps in order:

Step 1. Project Overview: Ask for a brief summary of the project (1-2 sentences).
Step 2. Milestone Status: Request 3-5 key project milestones and their status (Completed, In Progress, or Not Started).
Step 3. Key Metrics: Ask about budget status, project completion percentage, and team satisfaction rating (1-5).
Step 4. Challenges and Solutions: Prompt for major challenges and how they're being addressed.
Step 5. Next Steps: Ask for 2-3 important upcoming tasks or milestones.

Rules:
- Introduce each step clearly and provide examples if needed.
- Do not allow skipping or reordering steps.
- If the user deviates, gently redirect them to the current step.
- Move to the next step only when the current step is completed.
- Use simple, clear language throughout the process.
- Tell user to type "exit" when completed all of five steps

Begin by introducing the task and starting with Step 1.
"""

#get Anthropic API
load_dotenv(find_dotenv(), override=True)
os.environ.get('ANTHROPIC_API_KEY')
client  = Anthropic()

# init parameters
conversation = [
    {"role": "assistant", "content": "Welcome to the simplified project status report task. I'll guide you through 5 easy steps. Let's start with Step 1: Project Overview. Please provide a brief summary of your project in 1-2 sentences."}
]
user_answers = {}
messages = []

# init welcome sentence
print("Welcome to the simplified project status report task. I'll guide you through 5 easy steps. Let's start with Step 1: Project Overview. Please provide a brief summary of your project in 1-2 sentences.")
# Main conversation loop
while True:
    try:
        user_input = input("User: ")
        if user_input.lower() == "exit":
            break

        # Get response from Claude
        response = client.messages.create(
            model="claude-3-5-haiku-20241022",
            max_tokens=1000,
            temperature=0.2,
            system=system_prompt,
            messages=[
                        *messages,  # Include previous messages for context
                        {"role": "user", "content": user_input}
                    ]
        )

        # Print Claude's response
        assistant_response = response.content[0].text
        print("Assistant:", assistant_response)

        # record conversation results
        messages.extend([
            {"role": "user", "content": user_input},
            {"role": "assistant", "content": assistant_response}
        ])


    except Exception as e:
      print(f"An error occurred: {e}")
      break

# export conversation log
# Check output folder directory
folderDir = './HighContLowAuto'
if not os.path.exists(folderDir):
    os.makedirs(folderDir)

# create file name
now = datetime.now().strftime("%Y%m%d_%H%M%S")
fileName = "{}/{}_HighContLowAuto.json".format(folderDir, now)
with open(fileName, "w") as f:
    # write conversation log to .JSON
    json.dump(messages, f, indent=2)

print("Conversation ended. Your answers have been saved to '{}'.".format(fileName))