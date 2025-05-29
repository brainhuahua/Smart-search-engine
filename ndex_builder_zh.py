import json
import jieba
from collections import defaultdict

def tokenize_zh(text):
    return [w for w in jieba.cut(text) if len(w.strip()) > 1]

def build_and_save_index(jsonl_path, index_path):
    inverted_index = defaultdict(set)
    doc_store = {}

    with open(jsonl_path, encoding="utf-8") as f:
        for doc_id, line in enumerate(f):
            data = json.loads(line)
            title = data.get("title", "")
            tokens = tokenize_zh(title)
            doc_store[str(doc_id)] = data
            for token in tokens:
                inverted_index[token].add(str(doc_id))

    inverted_index = {word: list(doc_ids) for word, doc_ids in inverted_index.items()}
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump({"index": inverted_index, "docs": doc_store}, f, ensure_ascii=False, indent=2)

    print(f"✅ 中文索引构建完成，共词数：{len(inverted_index)}，文档数：{len(doc_store)}")

if __name__ == "__main__":
    build_and_save_index("books_zh.jsonl", "inverted_index_zh.json")
