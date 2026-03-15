import os
from openai import OpenAI
 
os.environ["OPENAI_API_KEY"] = 
 
client = OpenAI()
 
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": "Give me a short definition of DNN."}
    ]
)
 
print(response.choices[0].message.content)
 