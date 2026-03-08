#!/usr/bin/env python3
"""
AI Daily News - 飞书推送脚本
将日报推送到飞书群
"""

import os
import json
import requests
from datetime import datetime

def get_feishu_webhook():
    """获取飞书Webhook地址"""
    webhook = os.environ.get("FEISHU_WEBHOOK")
    if not webhook:
        print("⚠️ 未配置 FEISHU_WEBHOOK，跳过飞书推送")
        return None
    return webhook

def format_news_message(categories):
    """格式化飞书消息"""
    now = datetime.now()
    date_str = now.strftime("%Y年%m月%d日")
    
    # 构建消息卡片（简化版，不使用divider）
    elements = [
        {
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": f"**🤖 AI科技日报**\n📅 {date_str}\n今日AI科技新闻已更新"
            }
        }
    ]
    
    # 添加各分类新闻摘要
    category_emoji = {
        "headline": "📌",
        "product": "🚀", 
        "funding": "💰",
        "research": "🔬",
        "industry": "📊"
    }
    
    category_name = {
        "headline": "今日头条",
        "product": "产品发布",
        "funding": "融资动态",
        "research": "研究突破",
        "industry": "行业动态"
    }
    
    for cat, items in categories.items():
        if items and cat in category_emoji:
            # 构建新闻列表
            news_text = ""
            for item in items[:3]:  # 每个分类最多3条
                title = item["title"]
                if len(title) > 50:
                    title = title[:50] + "..."
                news_text += f"• {title}\n"
            
            elements.append({
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": f"**{category_emoji[cat]} {category_name[cat]}**\n{news_text}"
                }
            })
    
    # 添加查看链接
    elements.extend([
        {
            "tag": "action",
            "actions": [
                {
                    "tag": "button",
                    "text": {
                        "tag": "plain_text",
                        "content": "查看完整日报"
                    },
                    "url": "https://xiangjianan.github.io/ai-daily-news/",
                    "type": "primary"
                }
            ]
        },
        {
            "tag": "note",
            "elements": [
                {
                    "tag": "plain_text",
                    "content": f"生成时间: {now.strftime('%H:%M')}"
                }
            ]
        }
    ])
    
    message = {
        "msg_type": "interactive",
        "card": {
            "header": {
                "title": {
                    "tag": "plain_text",
                    "content": "AI科技日报"
                },
                "template": "blue"
            },
            "elements": elements
        }
    }
    
    return message

def send_to_feishu(webhook, message):
    """发送消息到飞书"""
    try:
        response = requests.post(
            webhook,
            json=message,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get("StatusCode") == 0:
                print("✓ 飞书推送成功")
                return True
            else:
                print(f"✗ 飞书推送失败: {result}")
        else:
            print(f"✗ 飞书推送失败: HTTP {response.status_code}")
    
    except Exception as e:
        print(f"✗ 飞书推送异常: {e}")
    
    return False

def main():
    print("=" * 50)
    print("🤖 AI Daily News - 飞书推送")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    print()
    
    # 获取Webhook
    webhook = get_feishu_webhook()
    if not webhook:
        return
    
    # 读取新闻数据
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    cat_file = os.path.join(project_dir, "data", "categorized_news.json")
    
    if not os.path.exists(cat_file):
        print("✗ 未找到新闻数据")
        return
    
    with open(cat_file, "r", encoding="utf-8") as f:
        categories = json.load(f)
    
    # 格式化消息
    message = format_news_message(categories)
    
    # 发送
    send_to_feishu(webhook, message)

if __name__ == "__main__":
    main()
