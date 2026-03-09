#!/usr/bin/env python3
"""
AI Daily News - 新闻抓取脚本
从多个来源抓取AI科技新闻
"""

import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil import parser as date_parser
import feedparser
import time
import os

# 新闻源配置
NEWS_SOURCES = {
    "daheiai": {
        "type": "daheiai",
        "url": "https://news.daheiai.com/rss.php",
    }
}

def fetch_daheiai(source_name, config):
    """从大黑AI速报抓取新闻"""
    news_items = []
    try:
        # 使用 requests 获取 RSS 内容
        response = requests.get(config["url"], timeout=10)
        response.raise_for_status()
        
        # 用 feedparser 解析
        feed = feedparser.parse(response.content)
        
        # 只获取最新一期
        if feed.entries:
            entry = feed.entries[0]
            
            # 获取完整内容
            content = ""
            if 'content' in entry and entry.content:
                content = entry.content[0].value
            elif 'summary' in entry:
                content = entry.summary
            
            # 解析HTML内容，提取新闻列表
            soup = BeautifulSoup(content, 'html.parser')
            
            # 查找所有列表项
            items = soup.find_all('li')
            
            for item in items[:15]:  # 取前15条
                # 提取标题（在<strong>标签中）
                strong = item.find('strong')
                if strong:
                    title = strong.get_text(strip=True)
                    
                    # 提取分类（在方括号中）
                    category = ""
                    if title.startswith('['):
                        end_bracket = title.find(']')
                        if end_bracket > 0:
                            category = title[1:end_bracket]
                            title = title[end_bracket+1:].strip()
                    
                    # 提取链接
                    link_tag = item.find('a')
                    link = link_tag.get('href', '') if link_tag else entry.get('link', '')
                    
                    # 提取摘要（<br/>后的文本）
                    summary = ""
                    br = item.find('br')
                    if br and br.next_sibling:
                        summary_text = br.next_sibling
                        if hasattr(summary_text, 'get_text'):
                            summary = summary_text.get_text(strip=True)
                        else:
                            summary = str(summary_text).strip()
                    
                    news_items.append({
                        "title": title,
                        "link": link,
                        "source": "大黑AI速报",
                        "pub_date": entry.get("published", ""),
                        "summary": summary[:200],
                        "category": category
                    })
        
        print(f"✓ {source_name}: 抓取 {len(news_items)} 条新闻")
        
    except Exception as e:
        print(f"✗ {source_name}: 抓取失败 - {e}")
    
    return news_items

def fetch_rss(source_name, config):
    """从RSS源抓取新闻"""
    news_items = []
    try:
        feed = feedparser.parse(config["url"])
        keywords = config.get("keywords", [])
        
        for entry in feed.entries[:20]:  # 每个源取前20条
            title = entry.get("title", "")
            
            # 如果有关键词过滤，检查是否匹配
            if keywords:
                if not any(kw.lower() in title.lower() for kw in keywords):
                    continue
            
            # 解析发布时间
            pub_date = entry.get("published", entry.get("updated", ""))
            try:
                parsed_date = date_parser.parse(pub_date)
                pub_date = parsed_date.strftime("%Y-%m-%d %H:%M")
            except:
                pub_date = datetime.now().strftime("%Y-%m-%d %H:%M")
            
            news_items.append({
                "title": title,
                "link": entry.get("link", ""),
                "source": source_name,
                "pub_date": pub_date,
                "summary": entry.get("summary", "")[:200]
            })
        
        print(f"✓ {source_name}: 抓取 {len(news_items)} 条新闻")
        
    except Exception as e:
        print(f"✗ {source_name}: 抓取失败 - {e}")
    
    return news_items

def fetch_all_news():
    """抓取所有新闻源"""
    all_news = []
    
    for source_name, config in NEWS_SOURCES.items():
        if config["type"] == "daheiai":
            news = fetch_daheiai(source_name, config)
            all_news.extend(news)
        elif config["type"] == "rss":
            news = fetch_rss(source_name, config)
            all_news.extend(news)
        
        # 避免请求过快
        time.sleep(1)
    
    return all_news

def categorize_news(news_items):
    """对新闻进行分类"""
    categories = {
        "headline": [],      # 头条
        "product": [],       # 产品发布
        "funding": [],       # 融资
        "research": [],      # 研究/论文
        "industry": [],      # 行业动态
        "other": []          # 其他
    }
    
    # 分类映射（大黑AI速报的分类 -> 我们的分类）
    category_map = {
        "模型动态": "headline",
        "产品工具": "product",
        "技巧教程": "product",
        "硬件动态": "product",
        "行业资讯": "industry",
    }
    
    for item in news_items:
        # 如果新闻自带分类，使用映射
        if "category" in item and item["category"]:
            source_cat = item["category"]
            target_cat = category_map.get(source_cat, "other")
            categories[target_cat].append(item)
        else:
            # 否则使用关键词分类
            title = item["title"]
            categorized = False
            
            category_keywords = {
                "headline": ["GPT", "Claude", "Gemini", "大模型", "OpenAI", "Anthropic", "Google AI"],
                "product": ["发布", "推出", "上线", "更新", "新版", "功能"],
                "funding": ["融资", "投资", "估值", "上市", "融资轮"],
                "research": ["论文", "研究", "突破", "SOTA", "性能"],
                "industry": ["应用", "落地", "商业化", "合作", "签约"]
            }
            
            for category, keywords in category_keywords.items():
                if any(kw in title for kw in keywords):
                    categories[category].append(item)
                    categorized = True
                    break
            
            if not categorized:
                categories["other"].append(item)
    
    # 每个分类只保留前5条
    for cat in categories:
        categories[cat] = categories[cat][:5]
    
    return categories

def save_news(news_items, categories):
    """保存新闻数据"""
    output_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(output_dir, "..", "data")
    os.makedirs(data_dir, exist_ok=True)
    
    # 保存原始新闻
    raw_file = os.path.join(data_dir, f"raw_news_{datetime.now().strftime('%Y%m%d')}.json")
    with open(raw_file, "w", encoding="utf-8") as f:
        json.dump(news_items, f, ensure_ascii=False, indent=2)
    
    # 保存分类新闻
    cat_file = os.path.join(data_dir, "categorized_news.json")
    with open(cat_file, "w", encoding="utf-8") as f:
        json.dump(categories, f, ensure_ascii=False, indent=2)
    
    print(f"\n✓ 新闻数据已保存")
    print(f"  - 原始数据: {raw_file}")
    print(f"  - 分类数据: {cat_file}")

def get_demo_news():
    """获取示例新闻数据（当RSS抓取失败时使用）"""
    demo_news = [
        {
            "title": "OpenAI发布GPT-5：多模态能力大幅提升，推理速度提高3倍",
            "link": "https://openai.com/blog/gpt-5",
            "source": "OpenAI",
            "pub_date": "2026-03-08 20:30",
            "summary": "OpenAI今日发布GPT-5，在多模态理解和推理能力上取得重大突破"
        },
        {
            "title": "字节跳动豆包大模型3.0上线：性能对标GPT-4，免费开放",
            "link": "https://www.bytedance.com",
            "source": "36氪",
            "pub_date": "2026-03-08 19:45",
            "summary": "字节跳动发布最新大模型，中文能力领先"
        },
        {
            "title": "Anthropic推出Claude 4：上下文窗口扩展至200K tokens",
            "link": "https://anthropic.com",
            "source": "机器之心",
            "pub_date": "2026-03-08 18:20",
            "summary": "Claude 4在长文本处理能力上实现突破"
        },
        {
            "title": "月之暗面完成10亿美元B轮融资，估值突破150亿美元",
            "link": "https://moonshot.cn",
            "source": "量子位",
            "pub_date": "2026-03-08 17:00",
            "summary": "国内AI大模型公司融资创新高"
        },
        {
            "title": "Google Gemini 2.0正式开放API，多模态生成能力升级",
            "link": "https://google.com",
            "source": "InfoQ",
            "pub_date": "2026-03-08 16:30",
            "summary": "Google最新多模态模型全面开放"
        },
        {
            "title": "智谱AI获5亿美元融资，加速国产大模型研发",
            "link": "https://zhipuai.cn",
            "source": "36氪",
            "pub_date": "2026-03-08 15:00",
            "summary": "智谱AI完成新一轮融资"
        },
        {
            "title": "Meta发布Llama 4：开源大模型新里程碑",
            "link": "https://meta.com",
            "source": "TechCrunch",
            "pub_date": "2026-03-08 14:20",
            "summary": "Meta开源最新大模型，参数量达万亿级"
        },
        {
            "title": "阿里通义千问2.5发布：中文理解能力全球领先",
            "link": "https://aliyun.com",
            "source": "机器之心",
            "pub_date": "2026-03-08 13:00",
            "summary": "阿里发布最新大模型，多项评测超越GPT-4"
        },
        {
            "title": "AI编程助手Cursor完成2亿美元融资，估值达10亿美元",
            "link": "https://cursor.sh",
            "source": "InfoQ",
            "pub_date": "2026-03-08 11:30",
            "summary": "AI编程工具公司跻身独角兽"
        },
        {
            "title": "华为发布盘古大模型5.0：工业AI应用新突破",
            "link": "https://huawei.com",
            "source": "量子位",
            "pub_date": "2026-03-08 10:00",
            "summary": "华为工业大模型在制造、能源领域实现规模化应用"
        }
    ]
    return demo_news

def main():
    print("=" * 50)
    print("🤖 AI Daily News - 新闻抓取")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    print()
    
    # 抓取所有新闻
    all_news = fetch_all_news()
    print(f"\n总共抓取: {len(all_news)} 条新闻")
    
    # 如果没有抓取到新闻，使用示例数据
    if len(all_news) == 0:
        print("\n⚠️ RSS抓取失败，使用示例数据")
        all_news = get_demo_news()
    
    # 分类
    categories = categorize_news(all_news)
    
    # 打印分类统计
    print("\n分类统计:")
    for cat, items in categories.items():
        if items:
            print(f"  - {cat}: {len(items)} 条")
    
    # 保存
    save_news(all_news, categories)
    
    return categories

if __name__ == "__main__":
    main()
