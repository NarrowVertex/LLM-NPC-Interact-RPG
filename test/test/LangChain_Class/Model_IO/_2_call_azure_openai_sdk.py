from dotenv import load_dotenv
import os

#pip install openai
from openai import AzureOpenAI

load_dotenv()

client = AzureOpenAI()

response = client.chat.completions.create(
  model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
  temperature=1.0,
  messages=[
    {"role": "system", "content":"You are a helpful assistant. Answer all questions to the best of your ability."}, 
    {"role": "user", "content": "Who won the World Cup in 2022?"}
  ]
)
print(response)
print("\n")
print(response.choices[0].message.content)

