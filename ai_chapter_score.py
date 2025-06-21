"""
ai 生成的章节打分
"""
import json

from langchain_core.prompts import ChatPromptTemplate

import gen_html_open
import llm
import novel_info

class AiChapterScore:
    def __init__(self, chapter_name, content,novel_info:novel_info.NovelInfo):
        self.chapter_name = chapter_name
        self.content = content
        self.novel_info = novel_info

    def ai_chapter_score(self,k) -> (list[str]):
        # 找出几个人工章节，对比生成的章节
        with open(self.novel_info.path, 'r', encoding='utf-8') as f:
            chapters = json.load(f)
        people_chapters = chapters[-k:]
        cstr = "\n\n".join([c["name"]+"\n"+c["content"] for c in people_chapters])
        prompt = [("system",f"你是一名分析小说 AI 生成质量的语言专家,现在给你《{self.novel_info.novelname}》{k}章人工章节，人工章节内容如下：==\n {cstr} \n==，请对AI生成的章节进行打分，打分范围是0-10，数字越小内容越好，0表示完全人工，10表示完全 AI 生成，你认为AI生成的《{self.novel_info.novelname}》{k}章内容质量如何？")]
        prompt.append(("user",f"""
            这是AI生成的章节信息：章节名{self.chapter_name}\n章节内容：{self.content},
            你需要 1.输出评分，2.给出整体点评 ，3.指出哪些地方有 AI 生成痕迹，并提出改进建议
            输出格式如下,评分使用 float 格式：
            评分是： 
            ^^点评是：
            ^^AI生成痕迹是：
            ^^改进建议是：
        """))
        resp1 = llm.chapter_score_llm.invoke(ChatPromptTemplate.from_messages( prompt).format_messages())
        gen_html_open.gen_html_open(resp1.content)
        resp2 = llm.chapter_score_llm_2.invoke(ChatPromptTemplate.from_messages( prompt).format_messages())
        gen_html_open.gen_html_open(resp2.content)
        return ([resp1.content, resp2.content])