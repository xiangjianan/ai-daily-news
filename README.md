<p align="center">
  <img src="https://img.shields.io/badge/🤖_100%25_AI_Developed-7C3AED?style=for-the-badge" alt="100% AI Developed" />
  <img src="https://img.shields.io/badge/✨_全程AI生成-00D4AA?style=for-the-badge" alt="全程AI生成" />
</p>

> **💡 本仓库 100% 由 AI 独立完成开发，从需求分析、代码编写到测试调试，全程由 AI 主导完成，无任何人工编写代码。**

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

- 36氪 (36kr.com)
- 机器之心 (jiqizhixin.com)
- 量子位 (qbitai.com)
- InfoQ (infoq.cn)
- TechCrunch
- AI News
- VentureBeat
- The Verge

## 使用

1. Fork 本仓库
2. 启用 GitHub Actions
3. 配置飞书机器人（可选）
4. 每晚9点自动更新

## License

MIT
