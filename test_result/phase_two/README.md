# Phase 2 - MiniMax 生图 skill 封装

## 阶段目标
封装 MiniMax API 调用，提供便捷的生图功能

## 完成内容

### 1. Skill 模块
- `skills/minimax-t2i/` - MiniMax 文生图 skill
- `skills/novel-writer/` - 小说写作 skill
- `skills/SKILL.md` - Skill 索引

### 2. minimax-t2i 功能
- 封面图生成 (cover)
- 场景插图生成 (scene)
- 角色形象图生成 (character)
- 通用图片生成 (image)
- 图生图支持 (with reference)

### 3. novel-writer 功能
- 选题搜索 (topics)
- 大纲生成 (outline)
- 正文写作 (write)

## 测试结果

| 测试项 | 状态 |
|--------|------|
| minimax-t2i 生图 | ✅ 通过 |
| novel-writer 写作 | ✅ 通过 |

## 文件列表
- `01_skill_test.md` - Skill 功能测试报告
- `test_skill_cover.png` - 测试生成的封面图
