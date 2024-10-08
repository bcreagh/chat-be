from openai import OpenAI

def callChatgpt(query: str) -> str:
    client = OpenAI()

    stream = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": query}],
        stream=True,
    )
    resp = ""
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            resp += chunk.choices[0].delta.content
    return resp