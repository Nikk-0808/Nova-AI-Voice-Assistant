from openai import OpenAI

# Initialize the OpenAI client with API key
client = OpenAI(api_key="your_openai_api_key_here")

# Generate a response from ChatGPT
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful virtual assistant named Nova."},
        {"role": "user", "content": "What is Python?"}
    ]
)

# Print the assistant's reply
print(response.choices[0].message.content)
