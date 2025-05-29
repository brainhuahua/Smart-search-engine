import json
from googletrans import Translator

input_file = "books_extracted.jsonl"
output_file = "books_zh.jsonl"

translator = Translator()

with open(input_file, "r", encoding="utf-8") as infile, \
     open(output_file, "w", encoding="utf-8") as outfile:

    for line in infile:
        try:
            data = json.loads(line)
            original_title = data.get("title", "")
            translation = translator.translate(original_title, src="en", dest="zh-cn")
            data["title"] = translation.text  # 替换为翻译后的中文标题
            outfile.write(json.dumps(data, ensure_ascii=False) + "\n")
            print(f"正在翻译")
        except Exception as e:
            print(f" 翻译失败: {original_title} ({e})")
