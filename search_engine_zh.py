import json
import jieba
from termcolor import colored

def tokenize_zh(text):
    return [w for w in jieba.cut(text) if len(w.strip()) > 1]

def load_index(index_path="inverted_index_zh.json"):
    with open(index_path, encoding="utf-8") as f:
        data = json.load(f)
    return data["index"], data["docs"]

def search(query, index, docs, mode="AND"):
    terms = tokenize_zh(query)
    if not terms:
        return []

    if mode == "AND":
        result = set(index.get(terms[0], []))
        for t in terms[1:]:
            result &= set(index.get(t, []))
    else:
        result = set()
        for t in terms:
            result |= set(index.get(t, []))

    scored = []
    for doc_id in result:
        title = docs[doc_id]["title"]
        score = sum(token in tokenize_zh(title) for token in terms)
        scored.append((score, doc_id))
    scored.sort(reverse=True)

    return [docs[doc_id] for score, doc_id in scored]

def highlight(text, keywords):
    for k in set(keywords):
        text = text.replace(k, colored(k, "red", attrs=["bold"]))
    return text
