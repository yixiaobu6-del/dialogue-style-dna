# 对话风格DNA提取器

从对话记录中提取语言风格特征，生成个人风格画像，并实现风格模仿写作。

## 项目简介

每个人的语言表达都有独特的风格"DNA"——包括句式偏好、用词习惯、修辞手法、语气特征等。本工具通过NLP技术系统性地提取这些特征，生成可量化的风格画像，并基于画像进行风格模仿写作。

## 核心功能

- **句式分析**：句长分布、句式结构、标点使用模式
- **高频词统计**：常用词汇、习惯表达、领域术语
- **修辞识别**：排比、比喻、反问、设问等修辞手法检测
- **语气分析**：正式/口语化程度，情感表达方式
- **风格画像**：多维度综合风格报告
- **风格模仿**：基于画像生成风格一致的文本

## 技术架构

```
对话风格DNA提取器/
├── extractor/
│   ├── analyzer.py    # 句式分析/高频词统计/修辞识别
│   ├── profile.py     # 风格画像生成
│   └── writer.py      # 风格模仿写作器
├── requirements.txt
└── README.md
```

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 提取风格DNA

```python
from extractor.analyzer import StyleAnalyzer
from extractor.profile import StyleProfiler

# 初始化分析器
analyzer = StyleAnalyzer()
analyzer.load_texts(["对话文本1", "对话文本2", ...])
analyzer.analyze()

# 生成风格画像
profiler = StyleProfiler(analyzer.results)
profile = profiler.generate()
profiler.save_report("style_profile.json")

print(profile)
```

### 风格模仿写作

```python
from extractor.writer import StyleWriter

writer = StyleWriter("style_profile.json")
output = writer.write("请简要说明你认为的好产品经理应该具备什么素质")
print(output)
```

## 分析维度

| 维度 | 子维度 | 说明 |
|------|--------|------|
| 句式结构 | 句长、从句数、并列结构 | 句子的长度和复杂度模式 |
| 词汇特征 | 高频词、独特词、术语 | 习惯使用的词汇集合 |
| 修辞手法 | 排比、比喻、反问、设问 | 常用的修辞表达模式 |
| 语气语调 | 正式度、情感强度、口语化程度 | 语言的情感色彩和正式程度 |
| 节奏韵律 | 停顿位置、语气词、感叹频率 | 语言的节奏和韵律特征 |

## 应用场景

- **个人写作助手**：模拟特定风格的写作输出
- **内容创作**：保持品牌声音的一致性
- **自媒体运营**：优化个人表达风格
- **沟通分析**：了解团队的沟通模式

## 许可证

MIT License