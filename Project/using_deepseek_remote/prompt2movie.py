from openai import OpenAI
from myChatApi import myKey
def give3movies(prompt):
  client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=myKey,
  )
  completion = client.chat.completions.create(
  #   extra_headers={
  #     "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
  #     "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
  #   },
  #   extra_body={},
    model="deepseek/deepseek-r1-distill-llama-70b:free",
    messages=[
      {
        "role": "user",
        "content": f"prompt:'{prompt}' write only list of 3 movies based on this prompt. output formate should be single line with comma separated movie1, movie2, movie3. dont write anything else."
      }
    ]
  )
  output = completion.choices[0].message.content
  output=output.split(",")
  return output

if __name__ == "__main__":
  prompt="hindi movie funny scary."
  output=give3movies(prompt=prompt)
  print(output)