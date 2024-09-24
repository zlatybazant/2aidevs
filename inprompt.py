import taskResponse, json 
from openai import OpenAI
from env import OPENAI_API_KEY

taskName = 'inprompt'
client = OpenAI(api_key=OPENAI_API_KEY)


try:
    token = taskResponse.get_task_token(taskName)
    print(f"Token dla zadania '{taskName}' to: {token}")
	
    data = taskResponse.get_json(token)
    print(f"Dane dla zadania '{taskName}' to: {data}")


    print(f"type:{type(data)} ")
    question = data.get('question')
    print(f"question: '{question}")

    completion = client.chat.completions.create(
	model="gpt-3.5-turbo",
	messages=[
		{"role": "system", "content": "Return name from question only. Short answer - name, add no punctuation marks. "},
		{"role": "user", "content": f"Question is: {question}."}
	]
    )
    name = completion.choices[0].message.content
    print(f"name: {name}")
    personDesc = ''
    for i in data['input']:
        if i.find(name) != -1:
            print(f"aidevs: useful info about {name} is {i}")
            personDesc = i
            break

    #Guard for correct answer
    if personDesc == '':
        print(f"{taskName}: ERROR: lack description about {name} found in the input")
        exit(1)

    completion = client.chat.completions.create(
	model="gpt-3.5-turbo",
	messages=[
		{"role": "system", "content": f"{personDesc}"},
		{"role": "user", "content": f"Question is: {question}."}
	]
    )
    completionOut = completion.choices[0].message.content
    print(f"AI :{completionOut}")

    answer={ 'answer': completionOut }
    print(f"answer: {answer} ")
    response = taskResponse.post_answer(token, answer)
    print(response.status_code)
    print(response.text)

except Exception as e:
    print(f"Error: {e}")
