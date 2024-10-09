import taskResponse, json, requests
from openai import OpenAI
from env import OPENAI_API_KEY
from requests.exceptions import RequestException
import time, re, sys



taskName = 'knowledge'
client = OpenAI(api_key=OPENAI_API_KEY)

def get_article_content(url, max_retries=5, backoff_factor=1):
    headers = { 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0' }

    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            return response
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

        population = get_article_content(url='https://restcountries.com/v3.1/all?fields=name,population')
        currency = get_article_content(url='https://api.nbp.pl/api/exchangerates/tables/A/?format=json')

        rates = json.loads(currency.text)[0]['rates']
        rates_string = ''
        for c in rates:
            rates_string = rates_string + f"{c['currency']}/{c['code']} {c['mid']}, "
            print(rates_string)

        population = json.loads(population.text)
        print(f"retrieved info about {len(population)} countries.")
        population = ""
        for c in population:
            population = population + (f"{c['name']['common']} - {c['population']} people, ")

        question  = data.get('question')
        print(f"question: {question}")

        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"Odpowiedz krótko na pytanie używając Twojej wiedzy i informacji poniżej. Podaj dokładne liczby.  %% Aktualne kursy walut: {rates_string} %% Populacja krajów: {population}"},
                {"role": "user", "content": question}
            ]
        )
        answer = completion.choices[0].message.content
        print(f"OAI response: {answer}")
        answer={ 'answer': answer }
        print(answer)
        response = taskResponse.post_answer(token, answer)
        print(response.status_code)
        print(response.text)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
