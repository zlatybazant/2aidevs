import json

def convert_to_jsonl():
    with open("md2html.txt",'r') as f:
        body = f.read().strip()
    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        try:
            data = json.loads(f"[{body}]")
        except json.JSONDecodeError:
            print("Problematic JSON")
            raise

    with open('md2html_finetune.jsonl', 'w', encoding='utf-8') as json_file:
        for item in data:
            json.dump(item, json_file, ensure_ascii=False)
            json_file.write('\n')
    print("conv complete")

convert_to_jsonl()
