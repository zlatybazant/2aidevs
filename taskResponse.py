import requests 
import yaml
import os.path


#Load API keys from file
def load_apikeys(apikey_file='/backup/2aidev/.apikeys'):
    with open(os.path.expanduser(apikey_file), 'r') as file:
        apikey = yaml.safe_load(file)
    return apikey['TASK_APIKEY']

#Load OpenAI Api key
def load_OAIkey(apikey_file='/backup/2aidev/.apikeys'):
    with open(os.path.expanduser(apikey_file), 'r') as file:
        apikey = yaml.safe_load(file)
    return apikey['OAI_APIKEY']

# Function to get the token for a given task name
def get_task_token(taskName, base_url='https://zadania.aidevs.pl', apikey_file='/backup/2aidev/.apikeys'):
    task_api = load_apikeys(apikey_file)
    url = f"{base_url}/token/{taskName}"

    response = requests.post(url, json={"apikey": task_api})
    
    if response.status_code == 200:
        return response.json()['token']
    else:
        raise Exception(f"Failed to get token: {response.status_code}, {response.text}")

#Function to get JSON data for taskName
def get_json(token, task_url='https://zadania.aidevs.pl/task'):
    get_url = f"{task_url}/{token}"

    response = requests.get(get_url)
      
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to get JSON data: {response.status_code}, {response.text}")
           
# Function to post JSON answer 
def post_answer(token, answer, answer_url='https://zadania.aidevs.pl/answer'):
    post_url = f"{answer_url}/{token}"
    
    response = requests.post(post_url, json=answer)
    if response.status_code == 200:
        return response
    else:
        raise Exception(f"Failed to post JSON data: {response.status_code}, {response.text}")
