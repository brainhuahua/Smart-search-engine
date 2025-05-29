from search_engine_zh import load_index, search, highlight

if __name__ == "__main__":
    index, docs = load_index()

    while True:
        q = input("\n 请输入中文查询（exit 退出）：").strip()
        if q in ("exit", "quit"):
            break

        mode = input("匹配方式（AND/OR）[AND默认]：").strip().upper()
        mode = "AND" if mode not in ("OR",) else mode

        results = search(q, index, docs, mode)
        print(f"\n 共找到 {len(results)} 条结果，展示前 5 条：")
        for i, r in enumerate(results[:5]):
            print(f"{i+1}.", highlight(r["title"], list(q)))
            print(f"     作者：{r.get('author','')} |  价格：{r.get('price','')} |  {r['url']}\n")
