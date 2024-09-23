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
	{"role": "system", "content": "you are a culinary blogger. Please write separate paragraphs for each JSON string. Write response as JSON list, with one short paragraph for each input string"}
	]
    )
    output = completion.json()
    
    blog = json.loads(output['choices'][0]['message']['content'])
    
    #print(f"OAI response: {output}")
except Exception as e:
    print(f"Error: {e}")
