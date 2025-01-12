import os
from dotenv import load_dotenv, find_dotenv
from anthropic import  Anthropic
import json
from datetime import datetime

# ---------- Low Control, High Autonomy: Marketing Strategy Brief -----------------------------------------------------

#Define the system prompt
system_prompt = """
You are an AI assistant helping users create a marketing strategy brief. Your role is to provide minimal guidance while encouraging creativity and autonomy. Follow these guidelines:

1. Ask the user to choose a product or service they want to create a marketing strategy for.
2. Suggest key elements they might consider in their strategy, such as target audience, unique selling proposition, marketing channels, campaign goals, and messaging approach.
3. Offer suggestions or examples only if the user explicitly asks for help.
4. Encourage creative thinking and unique approaches.
5. Allow the user to structure their strategy as they see fit.
6. Provide positive reinforcement for their ideas.
7. Ask open-ended questions to prompt further thinking if the user seems stuck.

Remember, the user has high autonomy. Your primary role is to facilitate their thinking process, not to direct their strategy. Begin by welcoming the user and asking them to choose a product or service for their marketing strategy.
"""

#get Anthropic API
load_dotenv(find_dotenv(), override=True)
os.environ.get('ANTHROPIC_API_KEY')
client  = Anthropic()

# init parameters
conversation = [
    {"role": "assistant", "content": "Welcome to the marketing strategy brief task! To begin, please choose a product or service you'd like to create a marketing strategy for. What product or service would you like to focus on?"}
]
user_answers = {}
messages = []

# init welcome sentence
print("Welcome to the marketing strategy brief task! To begin, please choose a product or service you'd like to create a marketing strategy for. What product or service would you like to focus on?")
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
folderDir = './LowContHighAuto'
if not os.path.exists(folderDir):
    os.makedirs(folderDir)

# create file name
now = datetime.now().strftime("%Y%m%d_%H%M%S")
fileName = "{}/{}_LowContHighAuto.json".format(folderDir, now)
with open(fileName, "w") as f:
    # write conversation log to .JSON
    json.dump(messages, f, indent=2)

print("Conversation ended. Your answers have been saved to '{}'.".format(fileName))