import openai

openai.api_key = "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"

try:
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="Hello, how are you?",
        max_tokens=5
    )
    print(response.choices[0].text.strip())
except Exception as e:
    print(f"Error: {e}")
