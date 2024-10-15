import taskResponse, json, requests
from openai import OpenAI
from env import OPENAI_API_KEY
from requests.exceptions import RequestException
import time, re, sys



taskName = 'ownapipro'
client = OpenAI(api_key=OPENAI_API_KEY)

def get_article_content(url, max_retries=5, backoff_factor=1):
    headers = { 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0' }

    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            return response.text
        except RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt + 1 == max_retries:
                raise
            time.sleep(backoff_factor * (2 ** attempt))


def main():

    try:
        token = taskResponse.get_task_token(taskName)
        print(f"Token dla zadania '{taskName}' to: {token}")
        data = taskResponse.get_json(token)
        print(f"Dane dla zadania '{taskName}' to: {data}")

        #url = data.get('data')
        #question  = data.get('question')

        #print(f"question: {question}")
        #urlContent = get_article_content(url)

        #urlContent = json.loads(urlContent)

        #completion = client.chat.completions.create(
        #    model="gpt-3.5-turbo",
        #    messages=[
        #        {"role": "system", "content": "Z otrzymanego pytania musisz zwrócić tylko imię i nazwisko w mianowniku. Nie przekazuj formy zdrobniałej. Gdy otrzymasz zdrobnienie imienia, musisz podać je  w formie podstawowej. Przekaż tylko dwa wyrazy - imię nazwisko. Nie odpowiadaj na pytanie."},
        #        {"role": "user", "content": question}
        #    ]
        #)
        #firstNameAI, lastNameAI = completion.choices[0].message.content.split()
        #
        #print(f"AI names: {firstNameAI}, {lastNameAI} ") 

        #firstName = []
        #lastName = []
        #personInfo = []

        #for person in urlContent:
        #    firstName = person['imie']
        #    lastName = person['nazwisko']

        #    if firstNameAI == firstName and lastNameAI == lastName:
        #        print(f"Found record: {personInfo}")
        #        print("found match: ", firstName, lastName)
        #        personInfo = person
        #        break
        #
        #if personInfo == []:
        #    print(f"No person data received, names don't match: {firstName} {lastName} ")
        #    sys.exit(1)
        #                 

        #completion = client.chat.completions.create(
        #    model="gpt-3.5-turbo",
        #    messages=[
        #        {"role": "system", "content": f"Dane szukanej osoby: {personInfo}, krótko odpowiedz na zadane pytanie."},
        #        {"role": "user", "content": f"Pytanie: {question}"}
        #    ]
        #)

        answer = 'https://2aidevs.bieda.it/v1/ownapi/ask'
        answer={ 'answer': answer }
        response = taskResponse.post_answer(token, answer)
        print(response.status_code)
        print(response.text)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
