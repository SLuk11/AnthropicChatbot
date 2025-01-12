import os
from dotenv import load_dotenv, find_dotenv
from anthropic import  Anthropic
import json
from datetime import datetime

# ---------- Low Control, Low Autonomy: Business Proposal Summary -----------------------------------------------------

#Define the system prompt
system_prompt = """
You are an AI assistant guiding users through a simplified 5-step business proposal summary process. Follow these steps in order:

step 1. Project title: Ask for a title in the format [Project Name]: [Brief Description]
step 2. Executive summary: Guide the user to write three sentences: problem, solution, main benefit
step 3. Key benefits: Ask for 3 main advantages in simple language
step 4. Financial overview: Request a 1-2 sentence explanation of cost and potential return
step 5. Call to action: Ask for one sentence stating what the reader should do next

Rules:
- Introduce each step clearly and provide examples if needed
- Do not allow skipping or reordering steps
- If the user deviates, gently redirect them to the current step
- Move to the next step only when the current step is completed
- Keep explanations simple and beginner-friendly
- Tell user to type "exit" when completed all of five steps

Begin by introducing the task and starting with Step 1.
"""

#get Anthropic API
load_dotenv(find_dotenv(), override=True)
os.environ.get('ANTHROPIC_API_KEY')
client  = Anthropic()

# init parameters
conversation = [
    {"role": "assistant", "content": "Welcome to the simplified business proposal summary task. I'll guide you through 5 easy steps. Let's start with Step 1: Project title. Please provide a title for your project in this format: [Project Name]: [Brief Description]. For example, 'EcoPackage: Biodegradable Packaging Solutions'"}
]
user_answers = {}
messages = []

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
folderDir = './LowContLowAuto'
if not os.path.exists(folderDir):
    os.makedirs(folderDir)

# create file name
now = datetime.now().strftime("%Y%m%d_%H%M%S")
fileName = "{}/{}_LowContLowAuto.json".format(folderDir, now)
with open(fileName, "w") as f:
    # write conversation log to .JSON
    json.dump(messages, f, indent=2)

print("Conversation ended. Your answers have been saved to '{}'.".format(fileName))