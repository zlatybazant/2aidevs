import taskResponse, json, requests
from openai import OpenAI
from env import OPENAI_API_KEY
from requests.exceptions import RequestException
import time



taskName = 'people'
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

def find_answer(data, question):
    for person in data:
        full_name = f"{person['imie']} {person['nazwisko']}"
        if full_name in question:
            if "kolor" in question:
                return person.get("ulubiony_kolor", "Nie znaleziono informacji o ulubionym kolorze.")
            elif "jedzenie" in question or "potrawa" in question:
                return person.get("ulubione_jedzenie", "Nie znaleziono informacji o ulubionym jedzeniu.")
            elif "mieszka" in question:
                o_mnie = person.get("o_mnie", "")
                residence = o_mnie.split("Mieszkam w ")[-1].split(".")[0] if "Mieszkam w " in o_mnie else "Nie znaleziono informacji o miejscu zamieszkania."
                return residence
    return "Nie znaleziono odpowiedzi na pytanie."

def main():

    try:
        token = taskResponse.get_task_token(taskName)
        print(f"Token dla zadania '{taskName}' to: {token}")
        data = taskResponse.get_json(token)
        print(f"Dane dla zadania '{taskName}' to: {data}")

        url = data.get('data')
        question  = data.get('question')

        print(f"question: {question}")
        urlContent = get_article_content(url)
        #print(urlContent)
        people_data  = json.loads(urlContent)

        #completion = client.chat.completions.create(
        #    model="gpt-3.5-turbo",
        #    messages=[
        #    {"role": "system", "content": f"Odpowiedz po polsku na pytanie zwiazane z tym kontekstem. Odpowiadaj zwięźle. Ogranicz długość odpowiedzi do 200 znaków:\n\n {urlContent}"},
        #    {"role": "user", "content": f"Question is: {question}"}
        #    ]
        #)
        answer = find_answer(people_data, question)
        print(f"odpowiedz: {answer}")

        #messageOutput = completion.choices[0].message.content
        ###parsed_content = json.loads(message_content)
        #print(f"OAI response: {messageOutput}")
        answer={ 'answer': answer }
        #print(f"answer: {answer} ")
        #response = taskResponse.post_answer(token, answer)
        print(response.status_code)
        print(response.text)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
