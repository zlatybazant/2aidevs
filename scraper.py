import taskResponse, json, requests
from openai import OpenAI
from env import OPENAI_API_KEY
from requests.exceptions import RequestException
import time



def get_article_content(url, max_retries=5, backoff_factor=1):
    headers = { 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0' }

    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, timeout=100)
            response.raise_for_status()
            return response.text
        except RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt + 1 == max_retries:
                raise
            time.sleep(backoff_factor * (2 ** attempt))


def main():
    taskName = 'scraper'
    client = OpenAI(api_key=OPENAI_API_KEY)

    try:
        token = taskResponse.get_task_token(taskName)
        print(f"Token dla zadania '{taskName}' to: {token}")
        data = taskResponse.get_json(token)
        print(f"Dane dla zadania '{taskName}' to: {data}")

        articleLink = data.get('input')
        question  = data.get('question')

        print(articleLink)
        print(question)

        articleContent = get_article_content(articleLink)
        print("doc retreived")
	#body = json.loads(request.text)

        completion = client.chat.completions.create(
	    model="gpt-3.5-turbo",
	    messages=[
	    {"role": "system", "content": f"Odpowiedz po polsku na pytania zwiazane z tym kontekstem. Odpowiadaj zwięźle. Ogranicz długość odpowiedzi do 200 znaków:\n\n {articleContent}"},
	    {"role": "user", "content": f"Question is: {question}"}
	    ]
        )

        messageOutput = completion.choices[0].message.content
	##parsed_content = json.loads(message_content)
        print(f"OAI response: {messageOutput}")
        answer={ 'answer': messageOutput }
        print(f"answer: {answer} ")
        response = taskResponse.post_answer(token, answer)
        print(response.status_code)
        print(response.text)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
