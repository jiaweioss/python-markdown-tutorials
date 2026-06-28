"""
06_my_scraper.py - 一个完整的简单爬虫脚本
功能：请求网页 → 解析链接 → 保存 CSV → 打印摘要
"""

import csv
import time
import socket
from pathlib import Path
from html.parser import HTMLParser
from urllib.request import Request, urlopen
import urllib.error


# ===== 第一部分：HTML 解析器 =====

class LinkParser(HTMLParser):
    """自定义 HTML 解析器，只提取 <a href="..."> 中的链接地址"""

    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for attr_name, attr_value in attrs:
                if attr_name == "href":
                    self.links.append(attr_value)


# ===== 第二部分：请求网页 =====

def fetch_page(url, timeout=10):
    """向指定 URL 发送请求，返回 HTML 字符串"""
    headers = {
        "User-Agent": "MyScraper/1.0 (educational project)",
    }
    request = Request(url, headers=headers)

    try:
        response = urlopen(request, timeout=timeout)
        html_bytes = response.read()
        # 尝试用 UTF-8 解码，如果失败就用 replace 替换无法解码的字符
        html_str = html_bytes.decode("utf-8", errors="replace")
        print(f"请求成功：{response.status} {url}")
        return html_str
    except urllib.error.HTTPError as e:
        print(f"HTTP 错误：{e.code} - {e.reason}")
        return None
    except urllib.error.URLError as e:
        print(f"URL 错误：{e.reason}")
        return None
    except socket.timeout:
        print(f"请求超时：{url}")
        return None


# ===== 第三部分：保存到 CSV =====

def save_to_csv(links, filepath):
    """把链接列表写入 CSV 文件"""
    parent_dir = filepath.parent
    parent_dir.mkdir(exist_ok=True)  # 确保目录存在

    with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["序号", "链接地址"])  # 表头
        for i, link in enumerate(links, 1):
            writer.writerow([i, link])

    print(f"已保存 {len(links)} 条链接到 {filepath}")


# ===== 第四部分：主程序 =====

def main():
    # 目标 URL——你可以换成任何你想采集的页面
    target_url = "https://docs.python.org/3/"

    print(f"开始采集：{target_url}")
    print("-" * 40)

    # 步骤 1：请求网页
    html = fetch_page(target_url)
    if html is None:
        print("采集失败，程序退出。")
        return

    # 步骤 2：解析 HTML 提取链接
    parser = LinkParser()
    parser.feed(html)

    all_links = parser.links
    print(f"共找到 {len(all_links)} 条链接")

    # 步骤 3：只保留以 http 或 https 开头的完整链接（过滤掉 #、/ 等内部跳转）
    valid_links = [link for link in all_links if link.startswith("http")]
    print(f"其中有效链接 {len(valid_links)} 条，已过滤内部跳转")

    # 步骤 4：保存到 CSV
    output_path = Path("output") / "06_my_scraper_links.csv"
    save_to_csv(valid_links, output_path)

    # 步骤 5：打印摘要
    print("-" * 40)
    print(f"采集摘要")
    print(f"  目标网址：{target_url}")
    print(f"  找到链接：{len(all_links)} 条")
    print(f"  有效链接：{len(valid_links)} 条")
    print(f"  保存位置：{output_path}")
    print("采集完成！")


if __name__ == "__main__":
    main()
