# novel-no-social

> 科幻/哲学/未来类小说账号自动化创作与发布系统

## 📋 项目简介

基于 OpenClaw 的科幻/哲学/未来类小说账号自动化创作与发布系统，支持：
- AI 辅助选题、大纲生成、正文写作
- MiniMax image-01 文生图/图生图生成封面和场景插图
- 自动发布到小红书、知乎、微信公众号

## 🏗️ 系统架构

```
热点/选题收集 → 设定讨论 → 生成大纲 → 写作 → 生图 → 发布
```

## 📂 项目结构

```
novel-no-social/
├── SPEC.md              # 详细技术方案
├── README.md            # 本文件
├── skills/              # Skills 模块
├── scripts/             # 核心脚本
├── config/              # 配置文件
└── novels/              # 小说存档
```

## 🚀 快速开始

（开发中）

## 📅 开发计划

| Phase | 任务 | 状态 |
|-------|------|------|
| 1 | 项目初始化 + 小说生成模块 | 🔄 进行中 |
| 2 | MiniMax 生图 skill | ⏳ 待开始 |
| 3 | 小红书发布 skill | ⏳ 待开始 |
| 4 | 知乎发布 skill | ⏳ 待开始 |
| 5 | 公众号发布 skill | ⏳ 待开始 |
| 6 | 定时任务 + 串联 | ⏳ 待开始 |
| 7 | 试运行 + 优化 | ⏳ 待开始 |

## 🔗 参考项目

- [salt-story](https://github.com/yfge/salt-story) - 知乎盐选故事写作
- [zhiforge](https://github.com/yfge/zhiforge) - 知乎文章自动发布
- [md2wechat](https://github.com/geekjourneyx/md2wechat-skill) - Markdown 转公众号
- [multi-post](https://github.com/JeffChang2024/multi-post) - 多平台发布框架

## 📝 许可证

MIT License
