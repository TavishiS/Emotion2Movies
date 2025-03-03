from openai import OpenAI
myKey="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"

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
    model="deepseek/deepseek-chat:free",
    messages=[
      {
        "role": "user",
        "content": f"prompt:'{prompt}' write only list of 3 movies based on this prompt. output formate should be single line with comma separated movie1, movie2, movie3. dont write anything else."
      }
    ]
  )
  output = completion.choices[0].message.content
  print(output)
  output=output.split(",")
  return output

if __name__ == "__main__":
  prompt="sleep fun jump wrong paper."
  output=give3movies(prompt=prompt)
  print(output)