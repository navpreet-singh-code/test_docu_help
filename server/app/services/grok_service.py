import os
from groq import Groq



def chat_with_grok(prompt: str):
    """
    Sends a prompt to the Grok API and returns the model's response.
    """
    try:
        # api_key = os.environ.get("GROQ_API_KEY")
        # if not api_key:
        #     raise ValueError("GROQ_API_KEY environment variable not set.")

        client = Groq(api_key="")

        
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="openai/gpt-oss-20b",
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        # Log the error or handle it as needed
        print(f"An error occur: {e}")
        return None
