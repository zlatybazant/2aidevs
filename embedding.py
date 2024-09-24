import taskResponse, json 
from openai import OpenAI
from env import OPENAI_API_KEY

taskName = 'embedding'

def get_embedding(text, model="text-embedding-ada-002"):
    client = OpenAI(api_key=OPENAI_API_KEY)
    text = text.replace("\n", " ")
    return client.embeddings.create(input=[text], model=model).data[0].embedding

try:
    token = taskResponse.get_task_token(taskName)
    print(f"Token dla zadania '{taskName}' to: {token}")
	
    data = taskResponse.get_json(token)
    print(f"Dane dla zadania '{taskName}' to: {data}")


    print(f"type:{type(data)} ")

    sentence = 'Hawaiian pizza'
    
    answer={ 'answer': get_embedding(sentence) }
    print(f"answer: {answer} ")
    response = taskResponse.post_answer(token, answer)
    print(response.status_code)
    print(response.text)

except Exception as e:
    print(f"Error: {e}")
