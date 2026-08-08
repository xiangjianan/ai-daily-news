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
  <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
  <title>AI科技日报 | {{ date_str }}</title>
  <meta name="description" content="每日 AI 科技新闻日报，一报速览人工智能前沿动态。">
  <meta name="theme-color" content="#1a1a1a">
  <link rel="manifest" href="manifest.webmanifest">
  <link rel="stylesheet" href="assets/style.css">
  <!-- 图标 / PWA -->
  <link rel="icon" type="image/svg+xml" href="icons/icon.svg">
  <link rel="icon" type="image/png" sizes="32x32" href="icons/favicon-32.png">
  <link rel="apple-touch-icon" href="icons/apple-touch-icon.png">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="default">
  <meta name="apple-mobile-web-app-title" content="AI日报">
</head>
<body>
  <main id="reportStage">
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
  </main>

  <!-- 底部日报导航：上一期 / 历史回顾 / 下一期 -->
  <nav class="report-nav" id="reportNav" aria-label="日报导航">
    <button class="rn-btn" id="navPrev" aria-label="上一期">‹ 上一期</button>
    <button class="rn-btn rn-review" id="navReview" aria-label="历史回顾">📜 历史回顾</button>
    <button class="rn-btn" id="navNext" aria-label="下一期">下一期 ›</button>
    <button class="rn-btn rn-today" id="navToday" aria-label="返回今天">📰 今天</button>
  </nav>

  <div class="history-overlay" id="historyOverlay" role="dialog" aria-modal="true" aria-label="历史日报回顾">
    <div class="hpanel">
      <div class="hpanel-head">
        <div>
          <div class="hpanel-title">历史日报回顾</div>
          <div class="hpanel-sub" id="hmStats">加载中…</div>
        </div>
        <button class="hpanel-x" id="ovClose" aria-label="关闭">✕</button>
      </div>
      <div class="hpanel-scroll">
        <div class="hm">
          <div class="hm-weekdays"><span>一</span><span>二</span><span>三</span><span>四</span><span>五</span><span>六</span><span>日</span></div>
          <div class="hm-right">
            <div class="hm-months" id="hmMonths"></div>
            <div class="hm-weeks" id="hmWeeks"></div>
          </div>
        </div>
        <input class="tl-search" id="tlSearch" type="search" placeholder="🔍 搜索标题 / 来源…" autocomplete="off">
        <div id="tlList"></div>
      </div>
    </div>
  </div>

{% raw %}
  <script>
  (function () {
    "use strict";
    var BASE = location.pathname.indexOf("/archive/") !== -1 ? "../" : "./";
    var UNIT = 19, GAP = 4; // 与 CSS 一致：格子 15px + 间距 4px

    var manifest = null;
    var items = [];      // 按日期升序
    var dateIndex = {};  // date -> items 下标
    var curIdx = -1;
    var navEl = null, lastScrollY = 0, navHidden = false, scrollTicking = false;

    function $(id) { return document.getElementById(id); }
    function u(p) { return BASE + p; }
    function dash(d) { return d.slice(0, 4) + "-" + d.slice(4, 6) + "-" + d.slice(6, 8); }
    function md(d) { return d.slice(4, 6) + "·" + d.slice(6, 8); }
    function pad(n) { return n < 10 ? "0" + n : "" + n; }
    function ymd(dt) { return "" + dt.getFullYear() + pad(dt.getMonth() + 1) + pad(dt.getDate()); }

    function entryPath(date) {
      return date === manifest.meta.today ? u("index.html") : u("archive/" + date + ".html");
    }

    function ensure(cb) {
      if (manifest) { cb(manifest); return; }
      fetch(u("data/archive_manifest.json"), { cache: "no-cache" })
        .then(function (r) { return r.json(); })
        .then(function (m) {
          manifest = m;
          items = (m.items || []).slice().sort(function (a, b) {
            return a.date < b.date ? -1 : a.date > b.date ? 1 : 0;
          });
          dateIndex = {};
          items.forEach(function (it, i) { dateIndex[it.date] = i; });
          cb(m);
        })
        .catch(function (e) {
          console.error("[history] manifest load failed", e);
          var s = $("hmStats"); if (s) s.textContent = "清单加载失败，请刷新重试";
        });
    }

    function openOverlay() {
      var ov = $("historyOverlay");
      if (!ov) return;
      ov.classList.add("open");
      document.body.style.overflow = "hidden";
      ensure(function (m) {
        renderStats(m);
        renderHeatmap();
        renderTimeline("");
      });
    }

    function closeOverlay() {
      var ov = $("historyOverlay");
      if (ov) ov.classList.remove("open");
      document.body.style.overflow = "";
    }

    function renderStats(m) {
      var el = $("hmStats");
      if (!el || !m) return;
      var meta = m.meta || {};
      el.textContent = "📊 " + (meta.count || 0) + " 期 · " +
        (meta.first ? dash(meta.first) : "—") + " → " +
        (meta.last ? dash(meta.last) : "至今");
    }

    function renderHeatmap() {
      var weeksHost = $("hmWeeks"), monthsHost = $("hmMonths");
      if (!weeksHost || !monthsHost || !items.length) return;
      weeksHost.innerHTML = "";
      monthsHost.innerHTML = "";

      var byDate = {};
      items.forEach(function (it) { byDate[it.date] = it; });

      var first = items[0].date, last = items[items.length - 1].date;
      var start = new Date(+first.slice(0, 4), +first.slice(4, 6) - 1, +first.slice(6, 8));
      var end = new Date(+last.slice(0, 4), +last.slice(4, 6) - 1, +last.slice(6, 8));
      var dow = (start.getDay() + 6) % 7; // 0 = 周一
      start.setDate(start.getDate() - dow);

      var cols = [];
      var cur = new Date(start.getTime());
      while (cur <= end) {
        var cells = [];
        for (var r = 0; r < 7; r++) {
          var ds = ymd(cur);
          cells.push({ date: ds, item: byDate[ds] || null });
          cur.setDate(cur.getDate() + 1);
        }
        cols.push(cells);
      }

      // 月份标签：按每周首日的月份做 run-length，宽度按周列数对齐
      var months = [];
      cols.forEach(function (c, i) {
        var mk = c[0].date.slice(0, 6);
        if (i === 0 || mk !== cols[i - 1][0].date.slice(0, 6)) months.push({ mk: mk, count: 1 });
        else months[months.length - 1].count++;
      });
      months.forEach(function (mm) {
        var el = document.createElement("div");
        el.className = "hm-month";
        el.textContent = +mm.mk.slice(4, 6) + "月";
        el.style.width = (mm.count * UNIT - GAP) + "px";
        monthsHost.appendChild(el);
      });

      cols.forEach(function (c) {
        var col = document.createElement("div");
        col.className = "hm-col";
        c.forEach(function (cell) {
          var d = document.createElement("div");
          d.className = "hm-cell" + (cell.item ? " has" : "");
          if (cell.item) {
            d.title = dash(cell.date) + " · 第" + (cell.item.issue || "?") + "期" +
              (cell.item.title ? " · " + cell.item.title : "");
            d.addEventListener("click", function () { pickDate(cell.date); });
          }
          col.appendChild(d);
        });
        weeksHost.appendChild(col);
      });
    }

    function renderTimeline(q) {
      var host = $("tlList");
      if (!host) return;
      host.innerHTML = "";
      if (!items.length) return;
      var ql = (q || "").trim().toLowerCase();
      var desc = items.slice().reverse();
      var groups = {}, order = [];
      desc.forEach(function (it) {
        var mk = it.date.slice(0, 6);
        if (!groups[mk]) { groups[mk] = []; order.push(mk); }
        var hay = (it.title || "") + " " + (it.source || "");
        if (!ql || hay.toLowerCase().indexOf(ql) >= 0) groups[mk].push(it);
      });

      if (!order.some(function (mk) { return groups[mk].length; })) {
        var empty = document.createElement("div");
        empty.className = "tl-empty";
        empty.textContent = "没有匹配的日报";
        host.appendChild(empty);
        return;
      }

      order.forEach(function (mk) {
        var list = groups[mk];
        if (!list.length) return;
        var g = document.createElement("div");
        g.className = "tl-group";
        var h = document.createElement("div");
        h.className = "tl-month";
        h.textContent = mk.slice(0, 4) + "年" + (+mk.slice(4, 6)) + "月";
        g.appendChild(h);
        list.forEach(function (it) {
          var row = document.createElement("div");
          row.className = "tl-item";
          row.tabIndex = 0;
          var dEl = document.createElement("span"); dEl.className = "tl-date"; dEl.textContent = md(it.date); row.appendChild(dEl);
          var iEl = document.createElement("span"); iEl.className = "tl-issue"; iEl.textContent = "第" + (it.issue || "?") + "期"; row.appendChild(iEl);
          var tEl = document.createElement("span"); tEl.className = "tl-title"; tEl.textContent = it.title || "(无标题)"; row.appendChild(tEl);
          var aEl = document.createElement("span"); aEl.className = "tl-arrow"; aEl.textContent = "›"; row.appendChild(aEl);
          var open = function () { pickDate(it.date); };
          row.addEventListener("click", open);
          row.addEventListener("keydown", function (e) {
            if (e.key === "Enter" || e.key === " ") { e.preventDefault(); open(); }
          });
          g.appendChild(row);
        });
        host.appendChild(g);
      });
    }

    function updateNav() {
      var prev = $("navPrev"), next = $("navNext");
      if (prev) prev.disabled = curIdx <= 0;
      if (next) next.disabled = curIdx >= items.length - 1;
    }

    // 整屏切换到指定日期的日报
    function showReport(date) {
      var i = dateIndex[date];
      if (i == null) return;
      curIdx = i;
      var stage = $("reportStage");
      if (!stage) return;
      var loading = document.createElement("div");
      loading.className = "report-loading";
      loading.textContent = "加载中…";
      stage.innerHTML = "";
      stage.appendChild(loading);
      window.scrollTo(0, 0);
      showNav();
      lastScrollY = 0;
      fetch(entryPath(date), { cache: "no-cache" })
        .then(function (r) { return r.text(); })
        .then(function (html) {
          var doc = new DOMParser().parseFromString(html, "text/html");
          var c = doc.querySelector(".container");
          stage.innerHTML = "";
          if (c) stage.appendChild(c);
          else { var e = document.createElement("div"); e.className = "report-loading"; e.textContent = "无内容"; stage.appendChild(e); }
          document.title = "AI科技日报 | " + dash(date);
          updateNav();
        })
        .catch(function () {
          stage.innerHTML = "";
          var e = document.createElement("div");
          e.className = "report-loading";
          e.textContent = "加载失败";
          stage.appendChild(e);
        });
    }

    function navPrev() { ensure(function () { if (curIdx > 0) showReport(items[curIdx - 1].date); }); }
    function navNext() { ensure(function () { if (curIdx < items.length - 1) showReport(items[curIdx + 1].date); }); }

    // 返回并刷新到「今天」最新日报（entryPath(today) === index.html，no-cache 拉取最新）
    function navToday() {
      ensure(function (m) {
        var t = m.meta.today;
        if (dateIndex[t] != null) showReport(t);
      });
    }

    // 从回顾面板选择某天：关闭面板 + 整屏切到该日报
    function pickDate(date) {
      closeOverlay();
      ensure(function () { showReport(date); });
    }

    // 底栏滚动显隐：向下浏览(上滑)时隐藏，向回滑(下滑)时展开
    function showNav() { if (navEl) navEl.classList.remove("hidden"); navHidden = false; }
    function hideNav() { if (navEl) navEl.classList.add("hidden"); navHidden = true; }
    function onScroll() {
      if (scrollTicking) return;
      scrollTicking = true;
      requestAnimationFrame(function () {
        scrollTicking = false;
        var y = window.pageYOffset || document.documentElement.scrollTop;
        if (y < 8) { showNav(); lastScrollY = y; return; }
        if (y + window.innerHeight >= document.documentElement.scrollHeight - 8) { showNav(); lastScrollY = y; return; }
        if ($("historyOverlay").classList.contains("open")) { lastScrollY = y; return; }
        if (y > lastScrollY + 4 && !navHidden) hideNav();
        else if (y < lastScrollY - 4 && navHidden) showNav();
        lastScrollY = y;
      });
    }

    // PWA：按 BASE 规范化 manifest / 图标路径，并注册 Service Worker
    var manifestLink = document.querySelector('link[rel="manifest"]');
    if (manifestLink) manifestLink.href = u("manifest.webmanifest");
    var appleIcon = document.querySelector('link[rel="apple-touch-icon"]');
    if (appleIcon) appleIcon.href = u("icons/apple-touch-icon.png");
    if ("serviceWorker" in navigator) {
      window.addEventListener("load", function () {
        navigator.serviceWorker.register(u("sw.js")).catch(function () {});
      });
    }

    // 事件绑定
    $("navToday").addEventListener("click", navToday);
    $("navPrev").addEventListener("click", navPrev);
    $("navNext").addEventListener("click", navNext);
    $("navReview").addEventListener("click", openOverlay);
    $("ovClose").addEventListener("click", closeOverlay);
    $("historyOverlay").addEventListener("click", function (e) { if (e.target === this) closeOverlay(); });
    $("tlSearch").addEventListener("input", function (e) { renderTimeline(e.target.value); });
    navEl = $("reportNav");
    window.addEventListener("scroll", onScroll, { passive: true });

    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && $("historyOverlay").classList.contains("open")) closeOverlay();
    });

    // 启动：加载清单，定位到“今天”并更新底栏按钮状态
    ensure(function (m) {
      curIdx = dateIndex[m.meta.today];
      if (curIdx == null) curIdx = items.length - 1;
      updateNav();
    });
  })();
  </script>
{% endraw %}
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


def _parse_report_for_manifest(path: str, date_hint: str) -> dict | None:
    """解析单份日报 HTML，提取清单所需字段（缺失字段返回空串，不报错）。"""
    import re
    from bs4 import BeautifulSoup

    try:
        with open(path, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f.read(), "html.parser")
    except Exception:
        return None

    # 日期：优先取 <title> 里的 YYYY-MM-DD，回退用文件名提示
    date = date_hint
    title_tag = soup.find("title")
    if title_tag:
        m = re.search(r"(\d{4})-(\d{2})-(\d{2})", title_tag.get_text())
        if m:
            date = m.group(1) + m.group(2) + m.group(3)

    # 期号：.header-left “第 N 期”
    issue = ""
    left = soup.select_one(".header-left")
    if left:
        m = re.search(r"(\d+)", left.get_text())
        if m:
            issue = m.group(1)

    # 头条：标题/链接/来源
    title, link, source = "", "", ""
    a = soup.select_one(".main-headline .headline-title a")
    if a:
        title = a.get_text(strip=True)
        link = a.get("href", "") or ""
    src = soup.select_one(".main-headline .headline-source")
    if src:
        source = src.get_text(strip=True)

    # 兜底：旧版模板无 .main-headline，取首条新闻标题/来源
    if not title:
        first_a = soup.select_one(".news-item .news-title a")
        first_t = soup.select_one(".news-item .news-title")
        node = first_a or first_t
        if node:
            title = node.get_text(strip=True)
            if first_a:
                link = first_a.get("href", "") or ""
        first_src = soup.select_one(".news-item .news-source")
        if first_src and not source:
            source = first_src.get_text(strip=True)

    # 金句
    quote = ""
    q = soup.select_one(".quote-section .quote")
    if q:
        quote = q.get_text(strip=True)

    return {
        "date": date,
        "issue": issue,
        "title": title,
        "link": link,
        "source": source,
        "quote": quote,
    }


def generate_manifest() -> None:
    """扫描 index.html + archive/*.html，生成 data/archive_manifest.json。
    纯静态站无目录列举，前端历史回顾依赖此清单。每次运行都全量刷新。
    """
    import glob

    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    index_file = os.path.join(project_dir, "index.html")
    archive_dir = os.path.join(project_dir, "archive")
    data_dir = os.path.join(project_dir, "data")
    os.makedirs(data_dir, exist_ok=True)

    today = datetime.now().strftime("%Y%m%d")
    items: list[dict] = []

    # 今天（index.html）—— date_hint 用今天，标题里也会校准
    if os.path.exists(index_file):
        e = _parse_report_for_manifest(index_file, today)
        if e:
            items.append(e)

    # 历史归档（文件名即日期）
    for f in sorted(glob.glob(os.path.join(archive_dir, "*.html"))):
        date_hint = os.path.splitext(os.path.basename(f))[0]
        e = _parse_report_for_manifest(f, date_hint)
        if e:
            items.append(e)

    # 按日期去重（今天与归档可能同日）+ 升序
    seen: set[str] = set()
    deduped: list[dict] = []
    for it in items:
        if not it["date"] or it["date"] in seen:
            continue
        seen.add(it["date"])
        deduped.append(it)
    deduped.sort(key=lambda x: x["date"])

    manifest = {
        "meta": {
            "today": today,
            "count": len(deduped),
            "first": deduped[0]["date"] if deduped else "",
            "last": deduped[-1]["date"] if deduped else "",
            "generated": datetime.now().strftime("%Y-%m-%d %H:%M"),
        },
        "items": deduped,
    }

    out = os.path.join(data_dir, "archive_manifest.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False)
    print(f"✓ 历史清单已生成: {out} ({len(deduped)} 期)")


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
        try:
            generate_manifest()
        except Exception as exc:
            print(f"⚠️ 历史清单生成失败: {exc}")
        return
    
    with open(cat_file, "r", encoding="utf-8") as f:
        categories = json.load(f)
    
    # 归档今日新闻
    archive_today()
    
    # 生成新HTML
    html = generate_html(categories)
    save_html(html, is_today=True)

    # 刷新历史回顾清单（扫描 index.html + archive/）
    try:
        generate_manifest()
    except Exception as exc:
        print(f"⚠️ 历史清单生成失败: {exc}")

    print("\n✓ 日报生成完成!")

if __name__ == "__main__":
    main()
