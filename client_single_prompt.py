from openai import AzureOpenAI

client = AzureOpenAI(
    azure_endpoint="https://giles-openai-test.openai.azure.com/",
    api_key="27e9399d48b64ce99400c08715dcec36",
    api_version="2023-03-15-preview",
)

deployment_name = "giles-gpt-4o"

user_prompt = str(input("\n\n\nEnter Prompt: "))

messages = [
    {
        "role": "user",
        "content": user_prompt,
    }
]

response = client.chat.completions.create(
    model=deployment_name,
    messages=messages,
)

response_message = response.choices[0].message.content
print(f"Model's response: {response_message}\n\n\n")
