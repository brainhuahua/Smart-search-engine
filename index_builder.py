import json
import string
from collections import defaultdict

def tokenize(text):
    text = text.lower()
    for p in string.punctuation:
        text = text.replace(p, " ")
    return [w for w in text.split() if w.isalpha()]

def build_and_save_index(jsonl_path, index_path):
    inverted_index = defaultdict(set)
    doc_store = {}

    with open(jsonl_path, encoding="utf-8") as f:
        for doc_id, line in enumerate(f):
            data = json.loads(line)
            tokens = tokenize(data.get("title", ""))
            doc_store[str(doc_id)] = data
            for token in tokens:
                inverted_index[token].add(str(doc_id))

    # 转换 set → list 以便序列化
    index_json = {word: list(ids) for word, ids in inverted_index.items()}
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump({"index": index_json, "docs": doc_store}, f, ensure_ascii=False, indent=2)

    print(f"索引保存成功，共索引词数：{len(index_json)}，文档数：{len(doc_store)}")

if __name__ == "__main__":
    build_and_save_index("books_extracted.jsonl", "inverted_index.json")
