from openai import OpenAI

shreeKey="shreekars API key"
#used by dhruv for testing
dhruvKey = "dhruvs API key"

def give5movies(prompt):
  client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=shreeKey,
  )
  completion = client.chat.completions.create(
  #   extra_headers={
  #     "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
  #     "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
  #   },
  #   extra_body={},
    model="deepseek/deepseek-chat:free",
    messages=[
      {
        "role": "user",
        "content": f"prompt:'{prompt}' write only list of 5 movies based on this prompt. output format should be single line with comma separated movie1, movie2, movie3, movie3, movie4, movie5. please don't write anything else."
      }
    ]
  )
  output = completion.choices[0].message.content
  #print(output)
  output=output.split(",")
  if len(output)>5:
    output=output[-5:]
  return output

if __name__ == "__main__":
  prompt="sleep fun jump wrong paper."
  output=give5movies(prompt=prompt)
  print(output)
