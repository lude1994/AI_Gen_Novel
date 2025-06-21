import json

from langchain_community.graphs import Neo4jGraph
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate

import ai_chapter_score
import gen_html_open
import llm
import novel_info
import novel_pre_deal
from prompt.novel_next_chapter_prompt import NovelNextChapterPrompt


class NextChapterInfo:
    def __init__(self, chapter_name, content, next_chapter_prompt, summary):
        self.chapter_name = chapter_name
        self.content = content
        self.next_chapter_prompt = next_chapter_prompt
        self.summary = summary

def gen_next_chapter(k, role_list, path, novel_name,suggests : list[str],aiChapter) -> NextChapterInfo:
    prompts = []
    npd = novel_pre_deal.NovelPreDeal("/users/zcm/Downloads/SoNovel-macOS_arm64/downloads/无敌六皇子(梁山老鬼).txt",
                                      "无敌六皇子", "./wudiliuhuangzi.chapter.total.txt")
    novel_prompt = NovelNextChapterPrompt(path, novel_name, npd)
    total = novel_prompt.novel_total()
    relation_history_prompt = novel_prompt.novel_relation_history(role_list)
    total_tupu_prompt = novel_prompt.novel_total_tupu()
    people_tupu_prompt = novel_prompt.novel_people_tupu()
    last_kchapter = novel_prompt.last_k_chapter(k=k)
    base_prompt = novel_prompt.system_prompt()
    prompts.append(("system", base_prompt + "\n\n" +
                    f"这是当前要创作的小说所有章节的简介:{total}" + "\n\n" +
                    f"这是当前要创作的小说事件发展线:{total_tupu_prompt}" + "\n\n" +
                    f"这是当前要创作的小说涉及的所有人物信息:{people_tupu_prompt}" + "\n\n" +
                    f"这是当前要创作小说的人物发展总结:{relation_history_prompt}" + "\n\n" +
                    f"这是当前要创作小说的最后{k}个章节:{last_kchapter}" + "\n\n"
                    ))
    if len(suggests) > 0:
        prompts.append(("user", f"你创作的最新章节如下：\n {aiChapter} , 请在已创作的章节基础上按照以下建议进行重写：\n{suggests}"))
    else:
        user_chapter_prompt = ("user", """你来创作最新章节，注意新章节要紧密续接已创作的最新章节内容，进行合理的续写,字数在2000以上""")
        # user_chapter_prompt = ("user", """参考给你的提示，构思第 21章的发展脉络 """)
        prompts.append(user_chapter_prompt)
    ####结束prompt
    cpt = ChatPromptTemplate.from_messages(prompts)
    messages = cpt.format_messages()
    resp = llm.chapter_gen_llm.invoke(messages)
    gen_html_open.gen_html_open(resp.content)
    name = resp.content.split("=====")[0]
    content = resp.content.split("=====")[0]
    # nci = NextChapterInfo(**map)
    return NextChapterInfo(name,content,"","")

suggests = []
aiChapter = ''
c = 0
while True:
    if c >= 1:
        break
    nci = gen_next_chapter(2, [("云峥", "沈落雁"), ("云峥", "文帝"), ("云峥", "三皇子")],
                     "./wudiliuhuangzi.chapter.total.txt","无敌六皇子",suggests,aiChapter)
    print(nci)
    # aiChapter = nci.content
    # suggests = ai_chapter_score.AiChapterScore(nci.chapter_name,nci.content,novel_info.NovelInfo("./wudiliuhuangzi.chapter.total.txt","无敌六皇子")).ai_chapter_score(k=2)
    c+=1