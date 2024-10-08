import taskResponse, json, requests, os, time, qdrant_client
from openai import OpenAI
from env import OPENAI_API_KEY
from requests.exceptions import RequestException
from docker_manager import ComposeManager
from qdrant_client.models import Distance, VectorParams, PointStruct

#def get_article_content(url, max_retries=5, backoff_factor=1):
#    headers = { 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0' }
#
#    for attempt in range(max_retries):
#        try:
#            response = request.get(url, headers=headers, timeout=10)
#            response.raise_for_status()
#            return response.text
#        except RequestException as e:
#            print(f"Attempt {attempt + 1} failed: {e}")
#            if attempt + 1 == max_retries:
#                raise
#            time.sleep(backoff_factor * (2 ** attempt))


taskName = 'search'
client = OpenAI(api_key=OPENAI_API_KEY)
file_remote = 'https://unknow.news/archiwum.json'
file_local = 'data/archiwum.json'

def get_remote_file():
    if not os.path.exists(file_local):
        print(f'Downloading {file_remote} to {file_local}')
        os.makedirs(os.path.dirname(file_local), exist_ok=True)
        page = requests.get(file_remote)
        with open(file_local, 'wb') as f:
            f.write(page.content)
    else:
        print(f"File {file_local} already exists, skipping download")

def connect_qdrant_collection(url='http://localhost:6333'):
    
    client = qdrant_client.QdrantClient(url=url)
    try:
        collection = client.get_collection("unknown_search")
        print("qdrant: Collection 'unknown_search' exists, skipping creation")
    except qdrant_client.http.exceptions.UnexpectedResponse:

        print("qdrant: Collection 'unknown_search' does not exist, about to create it")
        collection = client.create_collection(
            collection_name="unknown_search",
            vectors_config=VectorParams(size=1536, distance=Distance.COSINE)
        )

def main():

    compose_manager.stop_services()
    #compose_manager = ComposeManager()
    compose_manager.start_services()
    compose_manager.status()

    try:
        token = taskResponse.get_task_token(taskName)
        print(f"Token dla zadania '{taskName}' to: {token}")
        data = taskResponse.get_json(token)
        print(f"Dane dla zadania '{taskName}' to: {data}")

        get_remote_file()

        connect_qdrant_collection()


        #print(articleLink)
        #print(question)

        #articleContent = requests.get(articleLink)
        #print("doc retreived")
	##body = json.loads(request.text)

        #completion = client.chat.completions.create(
	#    model="gpt-3.5-turbo",
	#    messages=[
	#    {"role": "system", "content": f"Odpowiedz po polsku na pytania zwiazane z tym kontekstem. Odpowiadaj zwięźle. Ogranicz długość odpowiedzi do 200 znaków:\n\n {articleContent}"},
	#    {"role": "user", "content": f"Question is: {question}"}
	#    ]
        #)

        #messageOutput = completion.choices[0].message.content
	###parsed_content = json.loads(message_content)
        #print(f"OAI response: {messageOutput}")
        #answer={ 'answer': messageOutput }
        #print(f"answer: {answer} ")
        #response = taskResponse.post_answer(token, answer)
        #print(response.status_code)
        #print(response.text)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()