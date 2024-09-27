import taskResponse, json 
from openai import OpenAI
from env import OPENAI_API_KEY

taskName = 'whisper'
client = OpenAI(api_key=OPENAI_API_KEY)

try:
    token = taskResponse.get_task_token(taskName)
    print(f"Token dla zadania '{taskName}' to: {token}")
	
    data = taskResponse.get_json(token)
    print(f"Dane dla zadania '{taskName}' to: {data}")

    audio_file = open("/backup/2aidev/mateusz.mp3", "rb")
    transcription = client.audio.transcriptions.create(
	model = "whisper-1",
	file = audio_file
    )
    print(transcription.text)
    answer={ 'answer': transcription.text }
    print(f"answer: {answer} ")
    response = taskResponse.post_answer(token, answer)
    print(response.status_code)
    print(response.text)

except Exception as e:
    print(f"Error: {e}")
