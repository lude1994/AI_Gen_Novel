

# AI小说生成工具

这是一个基于AI的小说生成与处理工具集合，可用于小说章节生成、内容评分、故事结构分析等功能。

## 主要功能

- AI章节生成：根据已有的小说内容生成下一章节的内容。
- 章节评分：评估AI生成章节与人工章节的相似度。
- 故事结构分析：提取小说中角色之间的关系和情节发展。
- Markdown转HTML：将Markdown格式的小说内容转换为HTML格式。

## 核心模块

- `ai_chapter_score.py` - AI章节评分模块，用于评估生成章节的质量。
- `gen_next_chapter.py` - 生成下一章节模块，结合已有内容进行AI续写。
- `novel_pre_deal.py` - 小说预处理模块，用于初始化向量存储和章节信息提取。
- `gen_html_open.py` - Markdown内容转换工具，支持生成HTML格式的小说阅读界面。
- `prompt/novel_next_chapter_prompt.py` - 提示词生成模块，用于构建AI生成小说章节所需的上下文提示。

## 使用方法

请参考各模块中的函数定义及实现，调用相关方法进行使用。例如：

- 生成下一章节：使用`gen_next_chapter.gen_next_chapter()`方法。
- 章节评分：使用`ai_chapter_score.AiChapterScore.ai_chapter_score()`方法。
- Markdown转HTML：调用`gen_html_open.gen_html_open()`函数。
- 小说结构分析：使用`novel_pre_deal.NovelPreDeal.gen_novel_tupu()`方法。

## 依赖项

- Python 3.x
- Git
- ChromaDB（用于向量存储）

## 许可证

本项目基于MIT许可证发布，请参阅项目中的许可证文件以获取详细信息。