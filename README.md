# AI Daily News 🤖

每日AI科技新闻自动汇总系统

## 功能

- ✅ 自动抓取多个AI新闻源
- ✅ 生成精美HTML日报（适合截图发抖音）
- ✅ 部署到GitHub Pages
- ✅ 每晚9点自动更新
- ✅ 推送到飞书

## 访问地址

https://[你的GitHub用户名].github.io/ai-daily-news

## 项目结构

```
ai-daily-news/
├── index.html          # 今日日报（首页）
├── archive/            # 历史日报
│   ├── 20260307.html
│   └── ...
├── assets/             # 静态资源
│   ├── style.css
│   └── images/
├── scripts/            # 脚本
│   ├── fetch_news.py   # 新闻抓取
│   └── generate.py     # 生成HTML
├── .github/
│   └── workflows/
│       └── daily.yml   # 定时任务
└── README.md
```

## 新闻来源

- **大黑AI速报** (news.daheiai.com) - 每4小时更新的AI行业快讯，涵盖模型动态、产品工具、技巧教程、硬件动态、行业资讯

数据源RSS: https://news.daheiai.com/rss.php

## 使用

1. Fork 本仓库
2. 启用 GitHub Actions
3. 配置飞书机器人（可选）
4. 每晚9点自动更新

## License

MIT
