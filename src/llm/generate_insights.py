from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

def generate_insights(summary_text):

    try:

        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {
                    "role": "system",
                    "content": "You are a retail analytics expert."
                },
                {
                    "role": "user",
                    "content": summary_text
                }
            ],
            temperature=0.3
        )

        return response.choices[0].message.content

    except Exception:

        return """AI insights are currently unavailable. Please verify LLM service credentials and account balance."""
        