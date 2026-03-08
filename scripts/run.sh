#!/bin/bash
# AI Daily News - 本地运行脚本

set -e

cd "$(dirname "$0")"

echo "========================================"
echo "🤖 AI Daily News - 本地运行"
echo "时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "========================================"
echo

# 检查依赖
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
fi

source venv/bin/activate

echo "安装依赖..."
pip install -q -r requirements.txt

echo
echo "1. 抓取新闻..."
python fetch_news.py

echo
echo "2. 生成HTML..."
python generate.py

echo
echo "3. 推送飞书..."
if [ -n "$FEISHU_WEBHOOK" ]; then
    python send_feishu.py
else
    echo "⚠️ 未设置 FEISHU_WEBHOOK 环境变量，跳过推送"
fi

echo
echo "========================================"
echo "✓ 完成!"
echo "========================================"
