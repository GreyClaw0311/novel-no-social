# novel-no-social

> 科幻/哲学/未来类小说账号自动化创作与发布系统

---

## 📋 项目概述

### 需求回顾

| 项目 | 要求 |
|------|------|
| **主题** | 科幻 + 哲学 + 未来 |
| **更新频率** | 每日 1-3 话 |
| **字数** | 每话约 3000 字 |
| **篇幅** | 一个故事 6-10 章，每章 4-8 话 |
| **配图** | 每话 1 张封面 + 多张场景插图 |
| **发布平台** | 小红书 + 知乎 + 微信公众号 |

---

## 🏗️ 系统架构

```
阶段一：创作准备（一次性）
┌─────────────────────────────────────┐
│ 1. 热点/选题收集 → AI搜索，老板敲定  │
│ 2. 设定讨论 → 人设/背景/风格/走向    │
│ 3. 写作风格 skill 提炼（从书中）     │
│ 4. 生成故事大纲 → 老板敲定           │
│ 5. 所有设定写入 <小说名>.md         │
│ 6. MiniMax 文生图 → 角色形象图      │
└─────────────────────────────────────┘
           ↓ 创建项目文件夹
阶段二：每日更新（循环）
┌─────────────────────────────────────┐
│ 1. 根据设定 + 大纲 + 上下文写每话    │
│ 2. MiniMax 图生图 → 封面 + 场景图   │
│ 3. 拼接图文                         │
│ 4. 发布到小红书 + 知乎              │
└─────────────────────────────────────┘
```

---

## 📂 数据结构

```
novel-no-social/
├── SPEC.md                          # 本文档
├── README.md                        # 项目说明
├── AGENTS.md                        # Agent 工作指南
├── skills/                          # Skills 模块
│   ├── salt-story/                  # 知乎盐选故事写作 skill（去AI味）
│   ├── zhihu-post/                   # 知乎发布 skill
│   ├── md2wechat/                   # 微信公众号发布 skill
│   ├── xhs-publisher/               # 小红书发布 skill
│   └── minimax-t2i/                 # MiniMax 文生图 skill
├── scripts/                         # 核心脚本
│   ├── topic_collector.py           # 热点/选题收集
│   ├── outline_generator.py         # 大纲生成
│   ├── content_writer.py            # 正文写作
│   ├── minimax_image.py             # MiniMax 生图
│   ├── publisher.py                 # 发布调度
│   └── scheduler.py                 # 定时任务
├── config/
│   └── config.yaml                  # 全局配置
└── novels/                          # 小说存档
    └── <小说题目>/
        ├── meta.md                  # 选题/人设/背景/风格/走向/大纲
        ├── characters/              # 角色形象图
        │   ├── protagonist.png
        │   └── supporting_1.png
        ├── chapter_01/
        │   ├── episode_01.md        # 第1话正文
        │   ├── episode_01_cover.png # 封面
        │   ├── episode_01_scene_1.png
        │   └── episode_01_scene_2.png
        └── chapter_02/
```

---

## 📖 小说创作流程

### Phase 1: 创作准备

#### Step 1: 选题收集
- **输入**: 老板指令 或 全网热点搜索（科幻/哲学/未来相关）
- **工具**: Tavily Search / 全网资讯搜索
- **输出**: 3-5 个备选选题清单
- **流程**:
  ```
  搜索热点 → 筛选相关主题 → 生成选题提案 → 老板敲定
  ```

#### Step 2: 设定讨论（可与 Agent 讨论，老板最终拍板）

| 设定项 | 说明 |
|--------|------|
| 角色人设 | 主角/配角的性格、外貌、背景 |
| 故事背景 | 世界观、时间线、地点 |
| 写作风格 | 从书籍中提炼 或 指定风格 |
| 故事走向 | 主线剧情、关键节点 |
| 故事大纲 | 章节规划、每章核心冲突 |

#### Step 3: 写作风格 Skill
- 如果老板给了参考书籍 → AI 提炼书中写作特点 → 生成专属 style guide
- 或直接指定风格（简洁/悬疑/意识流等）
- **参考**: `salt-story` skill 的去 AI 味机制

#### Step 4: 生成 meta.md
- 将所有设定写入 `<小说名>/meta.md`
- **后续每话创作必须读取此文件作为上下文**

#### Step 5: 角色形象图
- 调用 MiniMax image-01 文生图
- 为每个主要角色生成一张形象图

---

### Phase 2: 每日更新

#### Step 1: 正文生成
- 读取 `meta.md` + 上一话内容
- 根据设定 + 大纲 + 上下文生成每话
- 字数控制：约 3000 字/话

#### Step 2: 配图生成
| 图片类型 | 调用 | 说明 |
|----------|------|------|
| 每话封面 | MiniMax image-01 文生图 | 每话一张，根据内容生成 |
| 场景插图 | MiniMax image-01 图生图 | 每话 2-4 张，封面风格一致 |

**图生图风格统一**：
- 先生成一张满意的封面
- 后续场景图以此为参考图（image-01 图生图）
- 确保画风、角色一致

#### Step 3: 图文拼接
- 将正文 + 封面 + 场景图拼接
- 生成适合各平台发布的格式

#### Step 4: 发布
- **小红书**: 标题 + 正文 + 图片
- **知乎**: 专栏长文 + 图片
- **微信公众号**: Markdown → 公众号格式

---

## 🎨 MiniMax API

### Token 配置
- **Coding Plan Token**: `sk-cp-QBz9N5h2gLhd5skUQuakC9xl5MpmAfyXNo3MHDc8P3PocK-pv4NWnlJtn0P2YIMBxr4Hh3SzalTlW__DzzERV-KfrMQGKBwbOXk3_IuKEwyFq8dCRk8msWk`

### 支持功能
1. 文本生成 (text-post)
2. 同步语音合成 HTTP (speech-t2a-http)
3. 同步语音合成 WebSocket (speech-t2a-websocket)
4. 创建异步语音合成任务 (speech-t2a-async-create)
5. 音色查询 (voice-management-get)
6. 文生图 (image-generation-t2i)
7. 图生图 (image-generation-i2i)

### API 文档
https://platform.minimaxi.com/docs/api-reference/

---

## 📱 发布模块

### 小红书发布
- **方案**: browser 自动化（Chrome Browser Relay）
- **参考**: `xiaohongshu-automation` 项目
- **要求**: 必须有图片

### 知乎发布
- **方案**: Chrome Browser Relay
- **参考**: `zhihu-post` / `zhiforge` 项目
- **注意**: 需要去 AI 味处理

### 微信公众号
- **方案**: `md2wechat-skill` Go CLI
- **功能**: Markdown → 公众号格式 + 草稿箱

---

## ⏰ 定时任务

```
每日执行流程:
  08:00 检查是否有新话需要生成
  08:30 生成今日更新内容
  09:00 发布到小红书 + 知乎
  09:30 记录日志
```

---

## 🛠️ 技术栈

| 层级 | 技术 |
|------|------|
| **LLM（写作）** | Qwen3.5-plus（百炼 API）|
| **LLM（图生图）** | MiniMax image-01 |
| **搜索** | Tavily Search / 全网热点 |
| **小红书发布** | browser 自动化 |
| **知乎发布** | Chrome Browser Relay |
| **公众号发布** | md2wechat-skill |
| **存储** | 本地文件系统 + Git |

---

## 📅 开发计划

| 阶段 | 任务 | 周期 |
|------|------|------|
| **Phase 1** | 项目初始化 + 小说生成模块 | 3 天 |
| **Phase 2** | MiniMax 生图 skill 封装 | 1-2 天 |
| **Phase 3** | 小红书发布 skill | 1 天 |
| **Phase 4** | 知乎发布 skill | 1 天 |
| **Phase 5** | 微信公众号发布 skill | 1 天 |
| **Phase 6** | 定时任务 + 串联测试 | 2 天 |
| **Phase 7** | 试运行 + 优化 | 2 天 |

**总计：约 2 周**

---

## ⚠️ 关键注意事项

1. **知乎去 AI 味** - 必须使用 salt-story 的 anti-AI 机制
2. **小红书必须有图** - 不能纯文字发布
3. **上下文连贯** - 每话必须加载 meta.md + 上一话内容
4. **老板敲定** - 选题、大纲必须老板确认后才能继续

---

## 🔗 参考项目

| 项目 | 用途 | 地址 |
|------|------|------|
| salt-story | 知乎盐选故事写作 + 去AI味 | https://github.com/yfge/salt-story |
| zhiforge | 知乎文章自动发布 | https://github.com/yfge/zhiforge |
| zhihu-post | 知乎发帖 Chrome 自动化 | https://github.com/InuyashaYang/zhihu-post |
| md2wechat | Markdown 转公众号 | https://github.com/geekjourneyx/md2wechat-skill |
| multi-post | 多平台发布框架 | https://github.com/JeffChang2024/multi-post |
| xiaohongshu-automation | 小红书自动化 | https://github.com/hqrss/xiaohongshu-automation |

---

## 📝 变更日志

### v1.0.0 (2026-04-21)
- 初始版本
- 完成 SPEC.md 编写
- 确定技术方案
