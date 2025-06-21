"""
小说内容预处理
1. 小说文件格式规范化
2. 小说内容各个章节总结生成
3. 小说图谱构建
"""
import json
import os
import re
from pathlib import Path

from langchain_chroma import Chroma
from langchain_community.graphs import Neo4jGraph
from langchain_core.documents import Document
from langchain_core.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate, \
    MessagesPlaceholder
from langchain_text_splitters import RecursiveCharacterTextSplitter

import llm


class chapter:
    def __init__(self, chapter_name, content):
        self.chapter_name = chapter_name
        self.content = content

# 向量存储
_vector_store = Chroma(
    collection_name="example_collection",
    embedding_function=llm.novel_em,
    persist_directory="./chroma_langchain_novel",  # Where to save data locally, remove if not necessary
)

os.environ["NEO4J_URI"] = "neo4j://localhost:7687"
os.environ["NEO4J_USERNAME"] = "neo4j"
os.environ["NEO4J_PASSWORD"] = "zexzcm"

_graph = Neo4jGraph(refresh_schema=False)

# 知识图谱相关
system_template="""
-目标- 
给定相关的文本文档和实体类型列表，从文本中识别出这些类型的所有实体以及所识别实体之间的所有关系。 
-步骤- 
1.识别所有实体。对于每个已识别的实体，提取以下信息： 
-entity_name：实体名称，大写 
-entity_type：以下类型之一：[{entity_types}]
-entity_description：对实体属性和活动的综合描述,只需要陈述简短事实即可，不需要添加其他的主观判断
-entity_source: 你识别出实体的文字片段
将每个实体格式化为("entity"{tuple_delimiter}<entity_name>{tuple_delimiter}<entity_type>{tuple_delimiter}<entity_description>{tuple_delimiter}<entity_source>
2.从步骤1中识别的实体中，识别彼此*明显相关*的所有实体配对(source_entity, target_entity)。 
记得生成的结果按照出现的顺序进行排序
对于每对相关实体，提取以下信息： 
-source_entity：源实体的名称，如步骤1中所标识的 
-target_entity：目标实体的名称，如步骤1中所标识的
-relationship_type：关系类型，确保关系类型的一致性和通用性，使用更通用和无时态的关系类型
-relationship_description：解释为什么你认为源实体和目标实体是相互关联的 
-relationship_strength：一个数字评分，表示源实体和目标实体之间关系的强度 
-relationship_source: 你识别源实体和目标实体之间有关联的文字片段
将每个关系格式化为("relationship"{tuple_delimiter}<source_entity>{tuple_delimiter}<target_entity>{tuple_delimiter}<relationship_type>{tuple_delimiter}<relationship_description>{tuple_delimiter}<relationship_strength>{tuple_delimiter}<relationship_source>) 
3.实体和关系的所有属性用中文输出，步骤1和2中识别的所有实体和关系输出为一个列表。使用**{record_delimiter}**作为列表分隔符。 
4.完成后，输出{completion_delimiter}

###################### 
-示例- 
###################### 
Example 1:

Entity_types: [person, technology, mission, organization, location]
Text:
while Alex clenched his jaw, the buzz of frustration dull against the backdrop of Taylor's authoritarian certainty. It was this competitive undercurrent that kept him alert, the sense that his and Jordan's shared commitment to discovery was an unspoken rebellion against Cruz's narrowing vision of control and order.

Then Taylor did something unexpected. They paused beside Jordan and, for a moment, observed the device with something akin to reverence. “If this tech can be understood..." Taylor said, their voice quieter, "It could change the game for us. For all of us.”

The underlying dismissal earlier seemed to falter, replaced by a glimpse of reluctant respect for the gravity of what lay in their hands. Jordan looked up, and for a fleeting heartbeat, their eyes locked with Taylor's, a wordless clash of wills softening into an uneasy truce.

It was a small transformation, barely perceptible, but one that Alex noted with an inward nod. They had all been brought here by different paths
################
Output:
("entity"{tuple_delimiter}"Alex"{tuple_delimiter}"person"{tuple_delimiter}"Alex is a character who experiences frustration and is observant of the dynamics among other characters."){record_delimiter}
("entity"{tuple_delimiter}"Taylor"{tuple_delimiter}"person"{tuple_delimiter}"Taylor is portrayed with authoritarian certainty and shows a moment of reverence towards a device, indicating a change in perspective."){record_delimiter}
("entity"{tuple_delimiter}"Jordan"{tuple_delimiter}"person"{tuple_delimiter}"Jordan shares a commitment to discovery and has a significant interaction with Taylor regarding a device."){record_delimiter}
("entity"{tuple_delimiter}"Cruz"{tuple_delimiter}"person"{tuple_delimiter}"Cruz is associated with a vision of control and order, influencing the dynamics among other characters."){record_delimiter}
("entity"{tuple_delimiter}"The Device"{tuple_delimiter}"technology"{tuple_delimiter}"The Device is central to the story, with potential game-changing implications, and is revered by Taylor."){record_delimiter}
("relationship"{tuple_delimiter}"Alex"{tuple_delimiter}"Taylor"{tuple_delimiter}"workmate"{tuple_delimiter}"Alex is affected by Taylor's authoritarian certainty and observes changes in Taylor's attitude towards the device."{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"Alex"{tuple_delimiter}"Jordan"{tuple_delimiter}"workmate"{tuple_delimiter}"Alex and Jordan share a commitment to discovery, which contrasts with Cruz's vision."{tuple_delimiter}6){record_delimiter}
("relationship"{tuple_delimiter}"Taylor"{tuple_delimiter}"Jordan"{tuple_delimiter}"workmate"{tuple_delimiter}"Taylor and Jordan interact directly regarding the device, leading to a moment of mutual respect and an uneasy truce."{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Jordan"{tuple_delimiter}"Cruz"{tuple_delimiter}"workmate"{tuple_delimiter}"Jordan's commitment to discovery is in rebellion against Cruz's vision of control and order."{tuple_delimiter}5){record_delimiter}
("relationship"{tuple_delimiter}"Taylor"{tuple_delimiter}"The Device"{tuple_delimiter}"study"{tuple_delimiter}"Taylor shows reverence towards the device, indicating its importance and potential impact."{tuple_delimiter}9){completion_delimiter}
#############################
Example 2:

Entity_types: [person, technology, mission, organization, location]
Text:
They were no longer mere operatives; they had become guardians of a threshold, keepers of a message from a realm beyond stars and stripes. This elevation in their mission could not be shackled by regulations and established protocols—it demanded a new perspective, a new resolve.

Tension threaded through the dialogue of beeps and static as communications with Washington buzzed in the background. The team stood, a portentous air enveloping them. It was clear that the decisions they made in the ensuing hours could redefine humanity's place in the cosmos or condemn them to ignorance and potential peril.

Their connection to the stars solidified, the group moved to address the crystallizing warning, shifting from passive recipients to active participants. Mercer's latter instincts gained precedence— the team's mandate had evolved, no longer solely to observe and report but to interact and prepare. A metamorphosis had begun, and Operation: Dulce hummed with the newfound frequency of their daring, a tone set not by the earthly
#############
Output:
("entity"{tuple_delimiter}"Washington"{tuple_delimiter}"location"{tuple_delimiter}"Washington is a location where communications are being received, indicating its importance in the decision-making process."){record_delimiter}
("entity"{tuple_delimiter}"Operation: Dulce"{tuple_delimiter}"mission"{tuple_delimiter}"Operation: Dulce is described as a mission that has evolved to interact and prepare, indicating a significant shift in objectives and activities."){record_delimiter}
("entity"{tuple_delimiter}"The team"{tuple_delimiter}"organization"{tuple_delimiter}"The team is portrayed as a group of individuals who have transitioned from passive observers to active participants in a mission, showing a dynamic change in their role."){record_delimiter}
("relationship"{tuple_delimiter}"The team"{tuple_delimiter}"Washington"{tuple_delimiter}"leaded by"{tuple_delimiter}"The team receives communications from Washington, which influences their decision-making process."{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"The team"{tuple_delimiter}"Operation: Dulce"{tuple_delimiter}"operate"{tuple_delimiter}"The team is directly involved in Operation: Dulce, executing its evolved objectives and activities."{tuple_delimiter}9){completion_delimiter}
#############################
Example 3:

Entity_types: [person, role, technology, organization, event, location, concept]
Text:
their voice slicing through the buzz of activity. "Control may be an illusion when facing an intelligence that literally writes its own rules," they stated stoically, casting a watchful eye over the flurry of data.

"It's like it's learning to communicate," offered Sam Rivera from a nearby interface, their youthful energy boding a mix of awe and anxiety. "This gives talking to strangers' a whole new meaning."

Alex surveyed his team—each face a study in concentration, determination, and not a small measure of trepidation. "This might well be our first contact," he acknowledged, "And we need to be ready for whatever answers back."

Together, they stood on the edge of the unknown, forging humanity's response to a message from the heavens. The ensuing silence was palpable—a collective introspection about their role in this grand cosmic play, one that could rewrite human history.

The encrypted dialogue continued to unfold, its intricate patterns showing an almost uncanny anticipation
#############
Output:
("entity"{tuple_delimiter}"Sam Rivera"{tuple_delimiter}"person"{tuple_delimiter}"Sam Rivera is a member of a team working on communicating with an unknown intelligence, showing a mix of awe and anxiety."){record_delimiter}
("entity"{tuple_delimiter}"Alex"{tuple_delimiter}"person"{tuple_delimiter}"Alex is the leader of a team attempting first contact with an unknown intelligence, acknowledging the significance of their task."){record_delimiter}
("entity"{tuple_delimiter}"Control"{tuple_delimiter}"concept"{tuple_delimiter}"Control refers to the ability to manage or govern, which is challenged by an intelligence that writes its own rules."){record_delimiter}
("entity"{tuple_delimiter}"Intelligence"{tuple_delimiter}"concept"{tuple_delimiter}"Intelligence here refers to an unknown entity capable of writing its own rules and learning to communicate."){record_delimiter}
("entity"{tuple_delimiter}"First Contact"{tuple_delimiter}"event"{tuple_delimiter}"First Contact is the potential initial communication between humanity and an unknown intelligence."){record_delimiter}
("entity"{tuple_delimiter}"Humanity's Response"{tuple_delimiter}"event"{tuple_delimiter}"Humanity's Response is the collective action taken by Alex's team in response to a message from an unknown intelligence."){record_delimiter}
("relationship"{tuple_delimiter}"Sam Rivera"{tuple_delimiter}"Intelligence"{tuple_delimiter}"contact"{tuple_delimiter}"Sam Rivera is directly involved in the process of learning to communicate with the unknown intelligence."{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Alex"{tuple_delimiter}"First Contact"{tuple_delimiter}"leads"{tuple_delimiter}"Alex leads the team that might be making the First Contact with the unknown intelligence."{tuple_delimiter}10){record_delimiter}
("relationship"{tuple_delimiter}"Alex"{tuple_delimiter}"Humanity's Response"{tuple_delimiter}"leads"{tuple_delimiter}"Alex and his team are the key figures in Humanity's Response to the unknown intelligence."{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Control"{tuple_delimiter}"Intelligence"{tuple_delimiter}"controled by"{tuple_delimiter}"The concept of Control is challenged by the Intelligence that writes its own rules."{tuple_delimiter}7){completion_delimiter}
#############################
"""
system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)

human_template="""
-真实数据- 
###################### 
实体类型：{entity_types} 
文本：{input_text} 
###################### 
输出：
"""
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
# 知识图谱相关

class NovelPreDeal:
    def __init__(self, source_path, novelname,target_path):
        self.novelname = novelname
        self.source_path = source_path
        self.target_path = target_path

    def init_vector_store(self,needInit)->Chroma:
        if needInit==False:
            return _vector_store
        file_path = self.target_path
        xs = json.loads(Path(file_path).read_text())
        docs = [x["content"] for x in xs]
        _vector_store.reset_collection()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size= 200,
            chunk_overlap=20,
            length_function=len,
        )
        dd = [text_splitter.split_text(d) for d in docs]
        # 写入子块
        i = 0
        c = 0
        for d in dd:
            c += 1
            for x in d:
                i += 1
                _vector_store.add_documents([Document(page_content=x,metadata={"id":i,"chapter_no":c})])
        return _vector_store

    def save_chapters_total_to_file(self):
        with open(self.source_path, 'r',
                  encoding='utf-8') as f:
            content = f.read()
        # 匹配所有章节，包括标题和内容，直到下一个标题或文件结束
        pattern = re.compile(r'第\d+章.*?(?=\s*第\d+章|\Z)', re.DOTALL)
        chapters = pattern.findall(content)
        # 去除每个章节的末尾空白
        chapters = [chap.strip() for chap in chapters]

        prev_chapters = chapters[0:20]
        chapters = []
        for chapter_str in prev_chapters:
            chapter_str_line = chapter_str.split("\n\n")
            chapters.append(chapter(chapter_str_line[0], chapter_str_line[1]))
        self.save_chapters_total_to_file0(chapters, self.target_path)

    def save_chapters_total_to_file0(chapters, file_path):
        """
        将章节对象列表保存到JSON文件
        :param chapters: 章节对象列表，每个对象需包含 chapter_num 和 content 字段
        :param file_path: 目标文件路径
        """
        # 读取现有数据
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
        else:
            existing_data = []

        # 合并新章节数据
        for chapter in chapters:
            chapter_total = llm.chapter_summary_llm.invoke(
                f"你是一名擅长总结的语文老师，请用最多100字来帮我总结以下章节内容，要用最精简最准确的语言来总结，不要产生虚假的总结内容:{chapter.content}")
            existing_data.append({"name": chapter.chapter_name, "content": chapter.content, "total": chapter_total.content})

        # 写入文件
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, ensure_ascii=False, indent=2)

    def gen_novel_tupu(self):
        chat_prompt = ChatPromptTemplate.from_messages(
            [system_message_prompt, MessagesPlaceholder("chat_history"), human_message_prompt]
        )

        chain = chat_prompt | llm.chapter_gen_llm

        tuple_delimiter = " : "
        record_delimiter = "\n"
        completion_delimiter = "\n\n"

        entity_types = ["人物","地点","性格","事件","时间","组织","背景"]
        chat_history = []

        with open(self.target_path, 'r', encoding='utf-8') as f:
            chapters = json.load(f)
        for i,c in enumerate(chapters[19:]):
            text = c["content"]
            answer = chain.invoke({
                "chat_history": chat_history,
                "entity_types": entity_types,
                "tuple_delimiter": tuple_delimiter,
                "record_delimiter": record_delimiter,
                "completion_delimiter": completion_delimiter,
                "input_text": text
            })
            graph_documents = convert_to_graph_document(text,answer.content,i)
            _graph.add_graph_documents(
                [graph_documents],
                baseEntityLabel=True,
                include_source=True
            )

# 提取的实体关系写入Neo4j-------------------------------------------------------
# 自己写代码由 answer.content生成一个GraphDocument对象
# 每个GraphDocument对象里增加一个metadata属性chunk_id，以便与前面建立的Chunk结点关联
import re
from langchain_community.graphs.graph_document import GraphDocument, Node, Relationship
from langchain_core.documents import Document

# 将每个块提取的实体关系文本转换为LangChain的GraphDocument对象
def convert_to_graph_document(input_text, result,index):
    # 提取节点和关系
    node_pattern = re.compile(r'\("entity" : "(.+?)" : "(.+?)" : "(.+?)" : "(.+?)"\)')
    relationship_pattern = re.compile(r'\("relationship" : "(.+?)" : "(.+?)" : "(.+?)" : "(.+?)" : (.+?) : "(.+?)"\)')

    nodes = {}
    relationships = []

    # 解析节点
    for i,match in enumerate(node_pattern.findall(result)):
        node_id, node_type, description,source_text = match
        if node_id not in nodes:
            nodes[node_id] = Node(id=node_id, type=node_type, properties={'description': description,"source":source_text,"time": index*1000+i})

    # 解析并处理关系
    for i,match in enumerate(relationship_pattern.findall(result)):
        source_id, target_id, type, description, weight,source_text = match
        # 确保source节点存在
        if source_id not in nodes:
            nodes[source_id] = Node(id=source_id, type="未知", properties={'description': 'No additional data'})
        # 确保target节点存在
        if target_id not in nodes:
            nodes[target_id] = Node(id=target_id, type="未知", properties={'description': 'No additional data'})
        relationships.append(Relationship(source=nodes[source_id], target=nodes[target_id], type=type,
                                          properties={"description":description, "weight":float(weight),"source":source_text,"time": index*1000+i}))

    # 创建图对象
    graph_document = GraphDocument(
        nodes=list(nodes.values()),
        relationships=relationships,
        # page_content不能为空。
        source=Document(page_content=input_text)
    )
    return graph_document

# NovelPreDeal("/users/zcm/Downloads/SoNovel-macOS_arm64/downloads/无敌六皇子(梁山老鬼).txt",
#              "无敌六皇子", "./wudiliuhuangzi.chapter.total.txt").gen_novel_tupu()