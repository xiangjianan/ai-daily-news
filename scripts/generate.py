#!/usr/bin/env python3
"""
AI Daily News - HTML生成脚本
将新闻数据生成HTML日报
"""

import json
import os
from datetime import datetime, timedelta
from jinja2 import Template

# HTML模板 - 报纸风格
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AI科技日报 | {{ date_str }}</title>
  <link rel="stylesheet" href="assets/style.css">
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>📰</text></svg>">
</head>
<body>
  <div class="container">
    <!-- 报纸头部 -->
    <header class="header">
      <div class="header-top">
        <div class="header-left">第 {{ issue_num }} 期</div>
        <div class="header-center">AI · ARTIFICIAL INTELLIGENCE · 人工智能</div>
        <div class="header-right">{{ date_str }}</div>
      </div>
      <h1>AI 科 技 日 报</h1>
      <div class="header-bottom">DAILY AI NEWS & TECHNOLOGY REPORT</div>
    </header>

    {% if categories.headline and categories.headline|length > 0 %}
    <!-- 头条区域 -->
    <article class="main-headline">
      <div class="headline-tag">◆ 头条 HEADLINE ◆</div>
      <h2 class="headline-title"><a href="{{ categories.headline[0].link }}" target="_blank">{{ categories.headline[0].title }}</a></h2>
      <div class="headline-meta">
        <span class="headline-source">{{ categories.headline[0].source }}</span>
        <span>{{ categories.headline[0].pub_date.split(' ')[1] }}</span>
      </div>
    </article>

    {% if categories.headline|length > 1 %}
    <!-- 副头条 -->
    <div class="sub-headlines">
      {% for item in categories.headline[1:3] %}
      <div class="sub-headline-item">
        <div class="news-title"><a href="{{ item.link }}" target="_blank">{{ item.title }}</a></div>
        <div class="news-meta"><span class="news-source">{{ item.source }}</span> | {{ item.pub_date.split(' ')[1] }}</div>
      </div>
      {% endfor %}
    </div>
    {% endif %}
    {% endif %}

    <div class="divider"></div>

    {% if categories.product %}
    <!-- 产品发布 -->
    <section class="section">
      <h3 class="section-title">产品发布 / PRODUCT</h3>
      <div class="news-grid">
        {% for item in categories.product %}
        <div class="news-item">
          <div class="news-title"><a href="{{ item.link }}" target="_blank">{{ item.title }}</a></div>
          <div class="news-meta"><span class="news-source">{{ item.source }}</span> | {{ item.pub_date.split(' ')[1] }}</div>
        </div>
        {% endfor %}
      </div>
    </section>
    {% endif %}

    {% if categories.funding %}
    <!-- 融资动态 -->
    <section class="section">
      <h3 class="section-title">融资动态 / FUNDING</h3>
      <div class="news-grid">
        {% for item in categories.funding %}
        <div class="news-item">
          <div class="news-title"><a href="{{ item.link }}" target="_blank">{{ item.title }}</a></div>
          <div class="news-meta"><span class="news-source">{{ item.source }}</span> | {{ item.pub_date.split(' ')[1] }}</div>
        </div>
        {% endfor %}
      </div>
    </section>
    {% endif %}

    {% if categories.research %}
    <!-- 研究突破 -->
    <section class="section">
      <h3 class="section-title">研究突破 / RESEARCH</h3>
      <div class="news-grid">
        {% for item in categories.research %}
        <div class="news-item">
          <div class="news-title"><a href="{{ item.link }}" target="_blank">{{ item.title }}</a></div>
          <div class="news-meta"><span class="news-source">{{ item.source }}</span> | {{ item.pub_date.split(' ')[1] }}</div>
        </div>
        {% endfor %}
      </div>
    </section>
    {% endif %}

    {% if categories.industry %}
    <!-- 行业动态 -->
    <section class="section">
      <h3 class="section-title">行业动态 / INDUSTRY</h3>
      <div class="news-grid">
        {% for item in categories.industry %}
        <div class="news-item">
          <div class="news-title"><a href="{{ item.link }}" target="_blank">{{ item.title }}</a></div>
          <div class="news-meta"><span class="news-source">{{ item.source }}</span> | {{ item.pub_date.split(' ')[1] }}</div>
        </div>
        {% endfor %}
      </div>
    </section>
    {% endif %}

    <!-- 今日金句 -->
    <section class="quote-section">
      <div class="quote">{{ quote }}</div>
      <div class="author">— {{ quote_author }}</div>
    </section>

    <!-- 页脚 -->
    <footer class="footer">
      <div class="footer-content">
        <span class="copyright">© 2026 AI Daily News</span>
        <span class="brand">AI 科 技 日 报</span>
        <span class="time">{{ gen_time }} 出版</span>
      </div>
    </footer>
  </div>
</body>
</html>
"""

# AI金句库
QUOTES = [
    ("AI不会取代你，会用AI的人会取代你。", "AI从业者共识"),
    ("人工智能是新时代的电力。", "吴恩达"),
    ("未来已来，只是分布不均。", "威廉·吉布森"),
    ("技术进步是社会进步的阶梯。", "AI先驱"),
    ("在AI时代，学习能力是最重要的能力。", "行业观察"),
    ("拥抱变化，是唯一的确定性。", "科技预言"),
    ("AI让每个人都有了超能力。", "Sam Altman"),
    ("机器学习是新时代的炼金术。", "研究者"),
]

def get_weekday_cn(date):
    """获取中文星期"""
    weekdays = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    return weekdays[date.weekday()]

def generate_html(categories):
    """生成HTML日报"""
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    date_display = f"{now.strftime('%Y年%m月%d日')} {get_weekday_cn(now)}"
    gen_time = now.strftime("%H:%M")
    
    # 计算期号（从2024-01-01开始）
    start_date = datetime(2024, 1, 1)
    issue_num = (now - start_date).days + 1
    
    # 随机选择金句
    import random
    quote, quote_author = random.choice(QUOTES)
    
    # 渲染模板
    template = Template(HTML_TEMPLATE)
    html = template.render(
        date_str=date_str,
        date_display=date_display,
        gen_time=gen_time,
        issue_num=issue_num,
        categories=categories,
        quote=quote,
        quote_author=quote_author
    )
    
    return html

def save_html(html, is_today=True):
    """保存HTML文件"""
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    if is_today:
        # 今日新闻 -> index.html
        output_file = os.path.join(project_dir, "index.html")
    else:
        # 历史新闻 -> archive/日期.html
        archive_dir = os.path.join(project_dir, "archive")
        os.makedirs(archive_dir, exist_ok=True)
        date_str = datetime.now().strftime("%Y%m%d")
        output_file = os.path.join(archive_dir, f"{date_str}.html")
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"✓ HTML已保存: {output_file}")
    return output_file

def archive_today():
    """将今天的index.html归档"""
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    index_file = os.path.join(project_dir, "index.html")
    
    if os.path.exists(index_file):
        # 读取index.html的日期
        with open(index_file, "r", encoding="utf-8") as f:
            content = f.read()
        
        # 提取日期 (从title标签)
        import re
        match = re.search(r'AI科技日报 \| (\d{4}-\d{2}-\d{2})', content)
        if match:
            date_str = match.group(1).replace("-", "")
            archive_dir = os.path.join(project_dir, "archive")
            os.makedirs(archive_dir, exist_ok=True)
            archive_file = os.path.join(archive_dir, f"{date_str}.html")
            
            # 如果归档文件不存在，创建它
            if not os.path.exists(archive_file):
                import shutil
                shutil.copy(index_file, archive_file)
                print(f"✓ 已归档: {archive_file}")

def main():
    print("=" * 50)
    print("🤖 AI Daily News - HTML生成")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    print()
    
    # 读取分类新闻
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    cat_file = os.path.join(project_dir, "data", "categorized_news.json")
    
    if not os.path.exists(cat_file):
        print("✗ 未找到新闻数据，请先运行 fetch_news.py")
        return
    
    with open(cat_file, "r", encoding="utf-8") as f:
        categories = json.load(f)
    
    # 归档今日新闻
    archive_today()
    
    # 生成新HTML
    html = generate_html(categories)
    save_html(html, is_today=True)
    
    print("\n✓ 日报生成完成!")

if __name__ == "__main__":
    main()
