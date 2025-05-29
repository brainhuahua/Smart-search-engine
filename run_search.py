from search_engine import load_index, search, highlight

if __name__ == "__main__":
    index, docs = load_index()

    while True:
        query = input("\n 输入查询（exit 退出）：").strip()
        if query.lower() in ("exit", "quit"):
            break

        mode = input("匹配方式（AND/OR）[AND默认]：").strip().upper()
        mode = "AND" if mode not in ("OR",) else mode

        results = search(query, index, docs, mode=mode)
        print(f"\n 共找到 {len(results)} 条结果，展示前 5 条：")

        for i, r in enumerate(results[:5]):
            print(f"{i+1}.", highlight(r["title"], query.lower().split()))
            print(f"     价格：{r['price']} |  库存：{r['availability']} |  {r['url']}\n")
