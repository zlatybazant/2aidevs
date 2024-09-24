import taskResponse, json 
from openai import OpenAI
from env import OPENAI_API_KEY

taskName = 'liar'
client = OpenAI(api_key=OPENAI_API_KEY)


try:
    token = taskResponse.get_task_token(taskName)
    print(f"Token dla zadania '{taskName}' to: {token}")
	
    data = taskResponse.get_json(token)
    print(f"Dane dla zadania '{taskName}' to: {data}")


    question = {"question": "What is capital city of Poland?"} 
    print (question)
    response = taskResponse.post_question(token,question)

    output = json.loads(response.text).get('answer')

    print(f"Output: {output}")

    completion = client.chat.completions.create(
	model="gpt-3.5-turbo",
	messages=[
		{"role": "system", "content": "You are judge for received answer. You role is to answer only YES when its corrent or NO when incorrect."},
		{"role": "user", "content": f"Question is: {question}. Received answer is: {output}."}
	]
    )

    ai_answer = completion.choices[0].message.content
    print("AI:", ai_answer)
	#Guard for correct answer
    guard = json.loads(response.text)['answer'].find("4") == -1

    answer={ 'answer': 'NO' if guard else 'YES' }
    print(f"answer: {answer} ")
    response = taskResponse.post_answer(token, answer)
    print(response.status_code)
    print(response.text)

except Exception as e:
    print(f"Error: {e}")
