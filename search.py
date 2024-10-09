import taskResponse, json, requests, os, time, qdrant_client
from openai import OpenAI
from env import OPENAI_API_KEY
from requests.exceptions import RequestException
from docker_manager import ComposeManager
from qdrant_client.models import Distance, VectorParams, PointStruct
from concurrent.futures import ThreadPoolExecutor
from uuid import uuid4
import logging

taskName = 'search'
client = OpenAI(api_key=OPENAI_API_KEY)
file_remote = 'https://unknow.news/archiwum.json'
file_local = 'data/archiwum.json'
BATCH_SIZE = 10
PROGRESS_FILE = 'batch_progress.txt'
LIMIT_VECTORS = 2000
qclient = qdrant_client.QdrantClient(url='http://localhost:6333')
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def get_remote_file():
    if not os.path.exists(file_local):
        print(f'Downloading {file_remote} to {file_local}')
        os.makedirs(os.path.dirname(file_local), exist_ok=True)
        page = requests.get(file_remote)
        with open(file_local, 'wb') as f:
            f.write(page.content)
    else:
        print(f"File {file_local} already exists, skipping download")

def connect_qdrant_collection():
    
    try:
        collection = qclient.get_collection("new_collection")
        print("qdrant: Collection 'new_collection' exists, skipping creation")
        return collection
    except qdrant_client.http.exceptions.UnexpectedResponse:

        print("qdrant: Collection 'new_collection' does not exist, about to create it")
        collection = qclient.create_collection(
            collection_name="new_collection",
            vectors_config=VectorParams(size=1536, distance=Distance.COSINE))

def save_progress(count):
    with open(PROGRESS_FILE, 'w') as f:
        f.write(str(count))

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r') as f:
            return int(f.read())
    return 0

def get_embedding(text, model="text-embedding-ada-002"):
    text = text.replace("\n", " ")
    return client.embeddings.create(input=[text], model=model).data[0].embedding


def retry_logic(text, attemps=5, model="text-embedding-ada-002"):
    delay = 1

    for attempt in range(attemps):
        try:
            embedding = get_embedding(text, model=model)
            return embedding
        except Exception as e:
            print(f"Error: Retry {i+1}/{attempts} failed: {e}")
            time.sleep(delay)
            delay *= 2
    print("Max retries exceeded")
    return None

def get_openai_embeddings(items, model="text-embedding-ada-002"):
    embeddings = []
    for item in items:
        text = item['title'].replace("\n", " ")
        print(f"Getting embedding for item: {item['title']}")

        embedding = retry_logic(text, model=model)
        if embedding is None:
            print(f"Skipping item due to failure: {item['title']}")
            embeddings.appedn(None)
        else:
            embeddings.append(embedding)
    return embeddings


def main():

    compose_manager = ComposeManager()
    compose_manager.stop_services()
    compose_manager.start_services()
    compose_manager.status()

    try:
        token = taskResponse.get_task_token(taskName)
        print(f"Token dla zadania '{taskName}' to: {token}")
        task  = taskResponse.get_json(token)
        print(f"Dane dla zadania '{taskName}' to: {task}")

        get_remote_file()

        collection_info = connect_qdrant_collection()

        cnt = load_progress()

        if collection_info.vectors_count >= LIMIT_VECTORS:
            print(f"qdrant: Collection already has {LIMIT_VECTORS} vectors, no need to add more.")
            return

        with open(file_local, 'r') as f:
            data = json.load(f)


        print(f"Loaded {len(data)} items from {file_local}")

        data = data[collection_info.vectors_count:] if cnt < collection_info.vectors_count else data[cnt:]

        batch = []
        for idx, item in enumerate(data, start=cnt):
            batch.append(item)
            print(f"Adding item {idx} to batch: {item['title']}")

            if len(batch) == BATCH_SIZE:

                print(f"Processing batch of {BATCH_SIZE} items, starting at index {idx - BATCH_SIZE + 1}")

                embeddings_batch = get_openai_embeddings(batch)

                points = []
                for i, (item, embedding) in enumerate(zip(batch, embeddings_batch)):
                    if embedding is None:
                        logging.warning(f"Skipping item {idx - len(batch) + i + 1} due to missing embedding")
                        continue
                    item['uuid'] = str(uuid4())
                    points.append(PointStruct(id=idx - len(batch) + i + 1, vector=embedding, payload=item))
                if points:
                    result = qclient.upsert(collection_name="new_collection", points=points)
                    #logging.debug(f"qdrant: Inserted batch, Result: {result}")
        
                save_progress(idx + 1)
                batch = []

            if idx >= LIMIT_VECTORS:
                print(f"qdrant: Limit of {LIMIT_VECTORS} vectors being processed reached, stopping. Check qdrantDB total points value")
                break
            
        print(f"qdrant: Finished processing up to {LIMIT_VECTORS} vectors from data in given file.")

        
        question  = task.get('question').strip().lower()
        print(f"task question: {question}")
        search = get_embedding(question)

        finds = qclient.search(collection_name="new_collection", query_vector=search, limit=1)
        for find in finds:
            print(f"Found result: {find.payload}")
        print(f"qdrant: closest find: {finds[0].payload['title']}, url {finds[0].payload['url']}")
        url = finds[0].payload['url']
        
        answer={ 'answer': url }
        print(f"answer: {answer} ")
        response = taskResponse.post_answer(token, answer)
        print(response.status_code)
        print(response.text)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
