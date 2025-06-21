

# AI Novel Generation Tool

This is a collection of AI-based novel generation and processing tools that can be used for functions such as generating novel chapters, content scoring, and story structure analysis.

## Main Features

- **AI Chapter Generation:** Generate the content of the next chapter based on existing novel content.
- **Chapter Scoring:** Evaluate the similarity between AI-generated chapters and human-written chapters.
- **Story Structure Analysis:** Extract relationships between characters and plot development within the novel.
- **Markdown to HTML:** Convert novel content in Markdown format into HTML format.

## Core Modules

- `ai_chapter_score.py` - AI chapter scoring module, used to evaluate the quality of generated chapters.
- `gen_next_chapter.py` - Module for generating the next chapter, performing AI continuation based on existing content.
- `novel_pre_deal.py` - Novel preprocessing module, used for initializing vector storage and extracting chapter information.
- `gen_html_open.py` - Markdown content conversion tool, supports generating HTML reading interfaces for novels.
- `prompt/novel_next_chapter_prompt.py` - Prompt generation module, used to construct context prompts required for AI-generated novel chapters.

## Usage Instructions

Please refer to the function definitions and implementations within each module to invoke the relevant methods. For example:

- Generate next chapter: Use the `gen_next_chapter.gen_next_chapter()` method.
- Chapter scoring: Use the `ai_chapter_score.AiChapterScore.ai_chapter_score()` method.
- Markdown to HTML: Call the `gen_html_open.gen_html_open()` function.
- Novel structure analysis: Use the `novel_pre_deal.NovelPreDeal.gen_novel_tupu()` method.

## Dependencies

- Python 3.x
- Git
- ChromaDB (for vector storage)

## License

This project is released under the MIT License. Please refer to the license file in the project for more details.