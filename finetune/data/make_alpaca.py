import json


if __name__ == '__main__':
    with open('./finetune/data/finetune_data.json', 'r', encoding='utf-8') as f:
        origin = json.loads(f.read())
    with open('../../prompt.md', 'r', encoding='utf-8') as f:
        template = f.read()
    with open('../../metadata.sql', 'r', encoding='utf-8') as f:
        metadata = f.read()
    alpaca_t2sql = []
    for i in origin:
        prompt = template.format(
            user_question=i["instruction"], table_metadata_string=metadata
        )
        alpaca_t2sql.append({
            "instruction": prompt,
            "input": "",
            "output": i["output"]
        })
    with open('./alpaca_t2sql.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(alpaca_t2sql, ensure_ascii=False, indent=1))
