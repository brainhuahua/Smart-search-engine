from __future__ import annotations

import os
import time
import random
import logging
import urllib.parse
from collections import deque

import requests
from bs4 import BeautifulSoup

# --------------------------------------------------------------------------- #
# 全局配置
# --------------------------------------------------------------------------- #
SEED_URL: str = "https://books.toscrape.com/index.html"
DOMAIN: str = "https://books.toscrape.com"
MAX_PAGES: int = 300                       # 抓取页面上限
DELAY_RANGE = (0.5, 1.5)                   # 请求间隔范围 (秒)
UA: str = "CSU-SE-SearchBot/0.1 (+https://github.com/your-team)"

SAVE_DIR: str = "data"                     # ==== 修改处：保存到 data/ ====
os.makedirs(SAVE_DIR, exist_ok=True)       # 若目录不存在则创建

# --------------------------------------------------------------------------- #
# 日志设置
# --------------------------------------------------------------------------- #
logging.basicConfig(
    format="%(levelname)s %(asctime)s %(message)s",
    level=logging.INFO,
    datefmt="%H:%M:%S",
)

# --------------------------------------------------------------------------- #
# 核心函数
# --------------------------------------------------------------------------- #
def fetch(url: str, timeout: int = 10) -> str | None:
    """下载单个 URL，返回 HTML，失败则返回 None。"""
    headers = {"User-Agent": UA, "Accept-Encoding": "gzip, deflate"}
    try:
        resp = requests.get(url, headers=headers, timeout=timeout)
        if resp.status_code == 200 and "text/html" in resp.headers.get("Content-Type", ""):
            return resp.text
        logging.warning("非 200 或非 HTML: %s (%s)", url, resp.status_code)
    except requests.RequestException as exc:
        logging.warning("请求失败: %s (%s)", url, exc)
    return None


def save_html(html: str, page_id: int) -> None:
    """将 HTML 保存到本地 data/{page_id}.html。"""
    filename = os.path.join(SAVE_DIR, f"{page_id}.html")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)


def extract_links(base_url: str, html: str) -> list[str]:
    """解析页面中的同域链接并返回绝对 URL 列表。"""
    soup = BeautifulSoup(html, "lxml")
    links: list[str] = []
    for a in soup.select("a[href]"):
        href = a["href"].strip()
        abs_url = urllib.parse.urljoin(base_url, href)
        if abs_url.startswith(DOMAIN) and "#" not in abs_url:
            links.append(abs_url.split("?")[0])  # 去掉查询参数
    return links


def crawl(seed: str = SEED_URL, max_pages: int = MAX_PAGES) -> None:
    """简单 BFS 爬虫主循环。"""
    frontier: deque[str] = deque([seed])
    visited: set[str] = set()

    while frontier and len(visited) < max_pages:
        url = frontier.popleft()
        if url in visited:
            continue

        logging.info("GET %s", url)
        html = fetch(url)
        if not html:
            continue

        visited.add(url)
        save_html(html, len(visited))
        logging.info("Saved page %d (%s)", len(visited), url)

        for link in extract_links(url, html):
            if link not in visited:
                frontier.append(link)

        time.sleep(random.uniform(*DELAY_RANGE))

    logging.info("任务完成！共抓取 %d 页，队列剩余 %d", len(visited), len(frontier))


# --------------------------------------------------------------------------- #
# 主入口
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    crawl()