# Novel-No-Social Skills

## 可用 Skills

### 1. novel-writer - 小说写作
- 选题搜索
- 大纲生成
- 正文写作

### 2. minimax-t2i - MiniMax 文生图
- 封面图生成
- 场景插图生成
- 角色形象图生成
- 图生图（风格参考）

## 使用方法

### 写作
```bash
python skills/novel-writer/novel_writer_skill.py topics -k 人工智能 量子计算
python skills/novel-writer/novel_writer_skill.py outline --meta novels/test/meta.md
python skills/novel-writer/novel_writer_skill.py write --meta novels/test/meta.md --chapter 1 --episode 1
```

### 生图
```bash
python skills/minimax-t2i/minimax_image_skill.py cover "科幻城市夜景"
python skills/minimax-t2i/minimax_image_skill.py scene "实验室场景"
python skills/minimax-t2i/minimax_image_skill.py character "男性科学家"
```
