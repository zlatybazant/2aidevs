import taskResponse, json, requests
from openai import OpenAI
from env import OPENAI_API_KEY
from requests.exceptions import RequestException
import time, sys



taskName = 'optimaldb'

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
def summarize_person_data(person_data,client):
    summaries = []
    for i in range(0, len(person_data), 10):
        batch = " ".join(person_data[i:i+10])
        try:
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Z każdego zdania, zwróć krótko tylko najważniejszą informacje. Wyniki nie mogą się powtarzać. Nie powielaj informacji. Może być użyta tylko raz . Nie wypisuj imienia."},
                    {"role": "user", "content": batch}
                ]
            )
            summaries.append(completion.choices[0].message.content)
        except Exception as e:
            print(f"Error during AI summarization: {e}")
            continue
    return " ".join(summaries)

def optimize_json_data(data, client):
    optimized_data = []
    for person, sentences in data.items():
        print(f"Optimizing for {person}...")
        optimized_summary = summarize_person_data(sentences, client)
        optimized_data.append(f'"{person}": "{optimized_summary}"')

        current_size = sys.getsizeof(", ".join(optimized_data))
        if current_size > 9000: 
            print(f"Warning: Optimized data exceeds 9kb limit. Current size: {current_size} bytes")
            break
    return ", ".join(optimized_data)

def main():

    client = OpenAI(api_key=OPENAI_API_KEY)
    try:
        token = taskResponse.get_task_token(taskName)
        print(f"Token dla zadania '{taskName}' to: {token}")
        data = taskResponse.get_json(token)
        print(f"Dane dla zadania '{taskName}' to: {data}")

        url = data.get('database')
        urlContent = get_article_content(url)

        urlContent = json.loads(urlContent)
        print(f"{type(urlContent)}, size: {sys.getsizeof(urlContent)}")
        #print(len(urlContent))

        optimized_data = optimize_json_data(urlContent, client)
        print(f"Optimized data size: {sys.getsizeof(json.dumps(optimized_data))} bytes")
        print(type(optimized_data),optimized_data)
        #with open('optimaldb.json','w') as f:
        #    f.write(urlContent)

        answer={ 'answer': optimized_data }
        print(answer)
        response = taskResponse.post_answer(token, answer)
        print(response.status_code)
        print(response.text)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
