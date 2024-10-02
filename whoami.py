import taskResponse, json, requests
from openai import OpenAI
from env import OPENAI_API_KEY
import time

hints = []
client = OpenAI(api_key=OPENAI_API_KEY)
taskName = 'whoami'

def refresh_token(taskName):
    token = taskResponse.get_task_token(taskName)
    time.sleep(1.5)
    return token

token = refresh_token(taskName)
print(f"Token dla zadania '{taskName}': {token}")

def get_hint(token):
    data = None
    data = taskResponse.get_json(token)
    if 'hint' in data:
        hint = data['hint']
        hints.append(hint)
        return hint 
    return None

def analyze_hints_gpt():
    system = f"""
    Based on the following hints about a person, can you confidently identify this person?
    If yes, provide the person's full name. If not, say "I'm not sure".
    """
    user = f"""
    Hints:
    {'.'.join(hints)}

    Answer in the format:
    Confidence: [Yes/No]
    Person: [Full Name or "Unknown"]
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
        {"role": "system", "content":f"{system}"},
        {"role": "user", "content":f"{user}"}
        ]
    )

    answer = response.choices[0].message.content
    print(f"OAI response: {answer}")
    is_sure = answer.split('\n')[0].split(': ')[1].strip() == 'Yes'
    person = answer.split('\n')[1].split(': ')[1].strip()

    return is_sure, person if person != "Unknown" else None

def submit_answer(token, answer):
    response = taskResponse.post_answer(token, {"answer": answer})
    return response.status_code == 200

def main():
    token = refresh_token(taskName)
    print(f"Initial token: {token}")
    while True:
        hint = get_hint(token)
        if hint:
            print(f"New hint: {hint}")
            is_sure, guess = analyze_hints_gpt()
            if is_sure:
                if submit_answer(token, guess):
                    print(f"Answer '{guess}' was accepted!")
                    break
                else:
                    print("Answer was rejected. Continuing to collect hints.")
            else:
                print("GPT is not sure, collecting more hints.")
        else:
            print("Failed to get hint. Trying again.")
            token = refresh_token(taskName)
        time.sleep(1.5)

if __name__ == "__main__":
    main()
