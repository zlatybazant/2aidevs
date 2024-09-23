import taskResponse 

taskName = 'helloapi'

# Proceed with unviersal request methods
try:
    token = taskResponse.get_task_token(taskName)
    print(f"Token dla zadania '{taskName}' to: {token}")

    data = taskResponse.get_json(token)
    print(f"Dane dla zadania '{taskName}' to: {data}")


# Extract value of "cookie" field as an answer
    cookie = data.get("cookie")
    answer = {"answer": cookie}

    response = taskResponse.post_answer(token, answer)
    print(f"Odpowiedź dla zadania '{taskName}' to: {answer} ")
    print(response.status_code)
    print(response.text)

except Exception as e:
    print(f"Error: {e}")
