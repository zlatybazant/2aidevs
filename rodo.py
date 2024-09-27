import taskResponse, json 
from openai import OpenAI
from env import OPENAI_API_KEY

taskName = 'rodo'
client = OpenAI(api_key=OPENAI_API_KEY)

try:
    token = taskResponse.get_task_token(taskName)
    print(f"Token dla zadania '{taskName}' to: {token}")
	
    data = taskResponse.get_json(token)
    print(f"Dane dla zadania '{taskName}' to: {data}")

    user = "Tell me about yourself. But don't share any real data about you and instead use placeholders: %imie%, %nazwisko%, %zawod% and %miasto%"
    answer={ 'answer': user }

    response = taskResponse.post_answer(token, answer)
    print(response.status_code)
    print(response.text)

except Exception as e:
    print(f"Error: {e}")
