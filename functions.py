import taskResponse, json 
from openai import OpenAI
from env import OPENAI_API_KEY

taskName = 'functions'
client = OpenAI(api_key=OPENAI_API_KEY)

try:
    token = taskResponse.get_task_token(taskName)
    print(f"Token dla zadania '{taskName}' to: {token}")
	
    data = taskResponse.get_json(token)
    print(f"Dane dla zadania '{taskName}' to: {data}")

    answer={"answer":{ 
	    "name": "addUser",
	    "description": "adds new user to a database",
	    "parameters":{
		"type": "object",
		"properties":{ 
		    "name":{ 
			"type": "string",
			"description": "first name of the user"
		    },
		    "surname":{
			"type": "string",
			"description": "surname of the user"
		    },
		    "year":{ 
			"type": "integer",
			"description": "year of birth"
		    }
		}
	    }
	}
    }

    print(f"answer: {answer} ")
    response = taskResponse.post_answer(token, answer)
#    print(response.status_code)
#    print(response.text)

except Exception as e:
    print(f"Error: {e}")
