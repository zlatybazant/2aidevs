import requests
import json
import yaml 
import os.path

# Load API keys from file
def load_task_apikey():
    with open(os.path.expanduser('/backup/2aidev/.apikeys'), 'r') as file: #temporary path to fix
        task_apikey = yaml.safe_load(file)
    return task_apikey['TASK_APIKEY']
        
taskName = 'helloapi'
taskAPI = load_task_apikey()
url = 'https://zadania.aidevs.pl'+'/token/'+taskName

print(f'Getting {url}, sending {taskAPI}')



# Post API auth to receive TOKEN
#apiToSend = {"apikey": apiKey}
post_response = requests.post(url, json={"apikey": taskAPI})

response_data = json.loads(post_response.text)
token = response_data['token']
print(f'Token zadania:{token}')

# get json task
getUrl = "https://zadania.aidevs.pl/task/"+token
getResponse = requests.get(getUrl)
getResponseToJson = getResponse.json()
print(getResponseToJson)

# post 'answer' from getResponse json
cookie = getResponseToJson.get("cookie")
answer = {"answer": cookie}
answerUrl = "https://zadania.aidevs.pl/answer/"+token
answerResponse = requests.post(answerUrl, json=answer)
print(answerResponse.text)    
