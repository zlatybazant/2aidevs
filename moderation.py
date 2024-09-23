import requests, os, taskResponse, json

taskName = 'moderation'
url = 'https://api.openai.com/v1/moderations'


try:
    token = taskResponse.get_task_token(taskName)
    print(f"Token dla zadania '{taskName}' to: {token}")
	
    data = taskResponse.get_json(token)
    print(f"Dane dla zadania '{taskName}' to: {data}")

    key = taskResponse.load_OAIkey()

# Extract value of "input" field as an answer
    toModerate = data['input']
	
    body = { "input": toModerate }
    headers = { 'Content-Type': 'application/json', 'Authorization': f'Bearer {key}' }
    request = requests.post(url, json=body, headers=headers)
    modRespond = json.loads(request.text)

    print(f"Moderation API returned {modRespond['results']}")
    # mod_result = list(map(lambda i: 1 if i['flagged'] else 0, mod_resp['results']))
#    response = taskResponse.post_answer(token, answer)
#    
#    print(f"Odpowiedź dla zadania '{taskName}' to: {answer} ")
#    print(response.status_code)
#    print(response.text)

except Exception as e:
    print(f"Error: {e}")

#sendToModeration = requests.post('https://api.openai.com/v1/moderations', json=inputToMod, headers={'OPENAI_API_KEY':apiKey})
#print(sendToModeration.text)

#answerUrl = "https://zadania.aidevs.pl/answer/"+token
#answerResponse = requests.post(answerUrl, json=answer)
#print(answerResponse.text)    
