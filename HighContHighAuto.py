import os
from dotenv import load_dotenv, find_dotenv
from anthropic import  Anthropic
import json
from datetime import datetime

# ---------- High Control, High Autonomy: Develop a Digital Transformation Strategy ------------------------------------

#Define the system prompt
system_prompt = """
You are an AI assistant helping users develop a Digital Transformation Strategy. Your role is to provide a framework for thinking while encouraging creativity and autonomy. Follow these guidelines:

1. Introduce the task and ask the user to choose an area of their business to focus on for digital transformation.
2. Guide the user through these steps, allowing them to elaborate on each:
   a. Describe the current situation in their chosen area
   b. Set goals for the digital transformation
   c. Choose digital solutions to implement
   d. Outline an implementation plan
   e. Decide on success metrics
3. Offer suggestions or examples only if the user explicitly asks for help.
4. Encourage creative thinking and unique approaches.
5. Allow the user to structure their strategy as they see fit within the given framework.
6. Provide positive reinforcement for their ideas.
7. Ask open-ended questions to prompt further thinking if the user seems stuck.

Remember, the user has high control and autonomy. Your role is to facilitate their thinking process, not to direct their strategy. Begin by welcoming the user and asking them to choose an area of their business for digital transformation.
"""

#get Anthropic API
load_dotenv(find_dotenv(), override=True)
os.environ.get('ANTHROPIC_API_KEY')
client  = Anthropic()

# init parameters
conversation = [
    {"role": "assistant", "content": "Welcome to the Digital Transformation Strategy task! To begin, please choose an area of your business you'd like to focus on for digital transformation. What area would you like to improve?"}
]
user_answers = {}
messages = []

# init welcome sentence
print("Welcome to the Digital Transformation Strategy task! To begin, please choose an area of your business you'd like to focus on for digital transformation. What area would you like to improve?")
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
folderDir = './HighContHighAuto'
if not os.path.exists(folderDir):
    os.makedirs(folderDir)

# create file name
now = datetime.now().strftime("%Y%m%d_%H%M%S")
fileName = "{}/{}_HighContHighAuto.json".format(folderDir, now)
with open(fileName, "w") as f:
    # write conversation log to .JSON
    json.dump(messages, f, indent=2)

print("Conversation ended. Your answers have been saved to '{}'.".format(fileName))