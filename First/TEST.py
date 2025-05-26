from openai import OpenAI

YOUR_API_KEY = "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"

messages = [
    {
        "role": "system",
        "content": (
            "You are an artificial intelligence assistant and you need to "
            "engage in a helpful, detailed, polite conversation with a user."
        ),
    },
    {   
        "role": "user",
        "content": (
            "How many stars are in the universe?"
        ),
    },
]

client = OpenAI(api_key=YOUR_API_KEY, base_url="https://api.perplexity.ai")

# chat completion without streaming
response = client.chat.completions.create(
    model="sonar",
    messages=messages,
)
print(response)
