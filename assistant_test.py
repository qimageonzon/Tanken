import os
import json
import requests
import time
from openai import AzureOpenAI

client = AzureOpenAI(
    azure_endpoint="https://giles-openai-test.openai.azure.com/",
    api_key="27e9399d48b64ce99400c08715dcec36",
    api_version="2024-05-01-preview",
)


# Create a thread
thread = client.beta.threads.create()


# Add a user question to the thread
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="assistant",
    content="Please introduce yourself and what you can offer to the user",
)

run = client.beta.threads.runs.create(
    thread_id=thread.id, assistant_id="asst_pgKaDAIfstrcEEPVSxelIKaO"
)

# Looping until the run completes or fails
while run.status in ["queued", "in_progress", "cancelling"]:
    time.sleep(1)
    run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

if run.status == "completed":

    thread_messages = client.beta.threads.messages.list(thread.id)
    thread_message_object = json.loads(thread_messages.model_dump_json(indent=2))
    print(thread_message_object["data"][0]["content"][0]["text"]["value"])

elif run.status == "requires_action":
    # the assistant requires calling some functions
    # and submit the tool outputs back to the run
    pass
else:
    print(run.status)

continue_condition = True

while continue_condition:

    continue_choice = str(input(f"Continue? (Y): "))

    if continue_choice.lower() == "y":

        user_prompt = str(input(f"\nUser Prompt: "))

        message = client.beta.threads.messages.create(
            thread_id=thread.id, role="user", content=user_prompt
        )

        run = client.beta.threads.runs.create(
            thread_id=thread.id, assistant_id="asst_pgKaDAIfstrcEEPVSxelIKaO"
        )

        while run.status in ["queued", "in_progress", "cancelling"]:
            time.sleep(1)
            run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

        if run.status == "completed":
            thread_messages = client.beta.threads.messages.list(thread.id)
            thread_message_object = json.loads(
                thread_messages.model_dump_json(indent=2)
            )
            print(thread_message_object["data"][0]["content"][0]["text"]["value"])

        elif run.status == "requires_action":
            # the assistant requires calling some functions
            # and submit the tool outputs back to the run
            pass
        else:
            print(run.status)

    else:
        continue_condition = False


thread_messages = client.beta.threads.messages.list(thread.id)
thread_message_object = json.loads(thread_messages.model_dump_json(indent=2))


for content in thread_message_object["data"]:
    print(content["content"][0]["text"]["value"])
