import taskResponse, json 
from openai import OpenAI
from env import OPENAI_API_KEY

taskName = 'blogger'
client = OpenAI(api_key=OPENAI_API_KEY)

try:
    token = taskResponse.get_task_token(taskName)
    print(f"Token dla zadania '{taskName}' to: {token}")
	
    data = taskResponse.get_json(token)
    print(f"Dane dla zadania '{taskName}' to: {data}")

    completion = client.chat.completions.create(
	model="gpt-3.5-turbo",
	messages=[
	{"role": "system", "content": " Please write short paraghraph for each JSON chapter title. Output only written responses as a JSON list."},
        {"role": "user", "content": json.dumps(data)}
	]
    )
    message_content = completion.choices[0].message.content
    parsed_content = json.loads(message_content)
    print(f"OAI response: {message_content}")
    content_list = parsed_content['blog']

    final_output = {
	"answer": content_list
    }
    final_json = json.dumps(final_output, ensure_ascii=False)
    print(f"final content: {final_json}")

    response = taskResponse.post_answer(token, final_output)
    print(response.status_code)
    print(response.text)
except Exception as e:
    print(f"Error: {e}")
