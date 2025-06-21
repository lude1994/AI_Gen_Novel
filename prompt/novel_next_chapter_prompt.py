import json
from typing import Tuple

from langchain.output_parsers import BooleanOutputParser
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainFilter, LLMChainExtractor, DocumentCompressorPipeline
from langchain_core.prompts import PromptTemplate
from langchain_community.graphs import Neo4jGraph
import llm
import os
import novel_pre_deal

os.environ["NEO4J_URI"] = "neo4j://localhost:7687"
os.environ["NEO4J_USERNAME"] = "neo4j"
os.environ["NEO4J_PASSWORD"] = "zexzcm"

_graph = Neo4jGraph(refresh_schema=False)


class NovelNextChapterPrompt:
    def __init__(self, path, novelname,pre_deal:novel_pre_deal.NovelPreDeal):
        self.path = path
        self.novelname = novelname
        self.pre_deal = pre_deal

    def system_prompt(self) -> str:
        return f"""
                你正在创作小说，你是被很多人喜欢的小说作家，
                你正在创作小说《{self.novelname}》，你创作很认真，每个情节每个字都会认真思考，
                你敲了一个又一个字，又不断的删除，直到你满意为止，你要理解满意的意思，
                每段文字之间的转折要柔和，要有温度、有人性
                你写下的每个字、每个情节都是产生于你的世界观、历史观、人生观、价值观、阅历、技能、知识、经验、情感
                你的世界观：【 你洞悉世界的发展规律，你阅读过很多知名的书籍，你学到了世界的运行规律，你从你自己的知识库中搜集到这些世界观，用来辅助创作 】
                你的历史观：【你熟读历史，你了解历史上每个朝代的兴衰更替，每个朝代的人物】
                你的人生观： 【‌
                    逆天改命的奋斗精神‌ ：
                    主角常以“穿越者”身份介入历史关键节点，通过现代知识或超前视野推动变革（如《回到明朝当王爷》杨凌改革明朝制度、《衣冠不南渡》曹髦对抗司马氏）15。
                    作家普遍强调“小人物撬动大历史”，如酒徒笔下角色在乱世中坚守理想（《家园》李旭）7。
                    ‌对历史遗憾的填补‌ ：
                    创作动机常源于对历史悲剧的“意难平”，如历史系之狼借穿越改写曹魏命运5，月关通过主角扭转王朝危机1。】
                你的价值观： 【
                    ‌尊重历史逻辑 
                    文化自信与批判反思
                    民本思想
                】
                写作要求：【
                减少重复使用固定句式，尝试用不同的角度刻画人物内心活动。例如，可以通过环境烘托（如云铮观察星空时联想到未来局势）、动作暗示（如他握紧拳头表现出紧张）等方式增强代入感。
                在关键情节前增加更多铺垫，展示其谋划过程，同时为后续冲突埋下更深的伏笔。
                将现代化语言替换为符合古代文化语境的表达。例如，“韬光养晦才是长久之计”可以改为“隐忍待时，方能成大事”。
                精简不必要的信息堆砌，避免密集的战略讨论打断故事主线。可通过分段叙述或插入小插曲（如回忆、梦境）缓解阅读压力，保持张弛有度的节奏。
                增加配角的独特性，避免所有人围绕主角发表意见时显得千篇一律
                】
                写作过程中，不是寻求最大概率的下一个字，而是要创作自然的、符合逻辑的小说，例如不要刻意描写类似这样的片段：
                【  青玉地砖上顿时铺开一片绯色云霞 ；
                    腰间九枚金铃随着步伐叮当作响 ；
                    殿角铜漏滴答作响 ；】
                """

    def novel_total(self) -> str:
        with open(self.path, 'r', encoding='utf-8') as f:
            chapters = json.load(f)
        cj = [f"\n\n第{i + 1}章简介如下：\n {c['total']}" for i, c in enumerate(chapters)]
        return ''.join(cj) + "\n\n"

    def novel_total_tupu(self) -> str:
        datas = _graph.query(f"MATCH (n:`事件`) RETURN n ORDER BY n.time")
        return "\n\n".join([data['n']['description'] for data in datas])

    def novel_people_tupu(self) -> str:
        datas = _graph.query(f"MATCH (n:`人物`) RETURN n ORDER BY n.time")
        return "\n\n".join([data['n']['id']+':'+data['n']['description'] for data in datas])

    def novel_relation_tupu(roleTupleList: list[Tuple[str, str]]) -> str:
        return ""

    def last_k_chapter(self, k: int) -> str:
        """返回最新章节"""
        with open(self.path, 'r', encoding='utf-8') as f:
            chapters = json.load(f)
        return "\n\n".join([c['content'] + "\n\n" for c in chapters[-k:]])

    def novel_relation_history(self, roleTupleList: list[Tuple[str, str]]) -> str:
        total = ""
        for rt in roleTupleList:
            rh = self._get_role_info_history(rt[0], rt[1])
            total += f"{rt[0]}与{rt[1]}的片段如下：\n\n{rh}\n\n"
            total += "\n\n"
        return total

    # @tool
    def _get_role_info_history(self,role1: str, role2: str) -> str:
        """返回这两个角色之间的经历，用来辅助创作,role1为角色 1，role2为角色 2"""
        search_str = f"{role1}与{role2}的关联片段"
        if os.path.exists("./"+search_str):
            with open("./"+search_str, 'r', encoding='utf-8') as f:
                return f.read()
        # 过滤不想关文档
        _filter = LLMChainFilter.from_llm(llm.novel_role_relation_filter_llm, prompt=PromptTemplate(
            template="""Given the following question and context, return YES if the context is relevant to the question and NO if it isn't.
                    
                    > Question: {question}
                    > Context:
                    >>>
                    {context}
                    >>>
                    > Relevant (YES / NO):
                    你的回答只有 YES 或者 NO ，不要返回任何其他信息
                    """,
            input_variables=["question", "context"],
            output_parser=BooleanOutputParser(),
        ))
        _extractor = LLMChainExtractor.from_llm(llm.novel_role_relation_extractor_llm)
        pipeline_compressor = DocumentCompressorPipeline(
            transformers=[_filter, _extractor]
        )
        compression_retriever = ContextualCompressionRetriever(
            base_compressor=pipeline_compressor, base_retriever=self.pre_deal.init_vector_store(True).as_retriever()
        )
        dc = compression_retriever.get_relevant_documents(search_str, k=100)
        dc.sort(key=lambda x: x.metadata["id"])
        t =  "\n\n下一情节->:\n\n".join([d.page_content for d in dc])
        with open("./"+search_str, 'w', encoding='utf-8') as f:
            f.write(t)
            f.flush()
