# 飞书机器人配置指南

## 1. 创建飞书群机器人

1. 打开飞书群聊
2. 点击群设置 → 群机器人 → 添加机器人
3. 选择"自定义机器人"
4. 机器人名称：`AI日报`
5. 复制 Webhook 地址

## 2. 配置 GitHub Secrets

1. 打开 GitHub 仓库
2. Settings → Secrets and variables → Actions
3. 点击 "New repository secret"
4. Name: `FEISHU_WEBHOOK`
5. Value: 粘贴 Webhook 地址
6. 点击 "Add secret"

## 3. 测试

手动触发 GitHub Actions：
1. Actions → AI Daily News - 每日更新
2. Run workflow → Run workflow
3. 查看运行日志

## Webhook 格式

```
https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxxxx
```

## 安全设置（可选）

如果启用了签名校验，需要在脚本中添加签名逻辑。
