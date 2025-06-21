from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI, OpenAIEmbeddings


ALI_API_KEY = "test"
ALI_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"

_qwen_max_llm = ChatOpenAI(
    api_key=ALI_API_KEY,
    base_url=ALI_BASE_URL,
    model_name= "qwen-max-2025-01-25"
)
_deepseek_r1 = ChatOpenAI(
    api_key=ALI_API_KEY,
    base_url=ALI_BASE_URL,
    model_name= "deepseek-r1"
)
_deepseek_v3 = ChatOpenAI(
    api_key=ALI_API_KEY,
    base_url=ALI_BASE_URL,
    model_name= "deepseek-v3"
)
_abab6_5s_chat = ChatOpenAI(
    api_key=ALI_API_KEY,
    base_url=ALI_BASE_URL,
    model_name= "abab6.5s-chat"
)



chapter_gen_llm = _abab6_5s_chat
chapter_score_llm = _deepseek_r1
chapter_score_llm_2 = _qwen_max_llm
chapter_score_llm_3 = _deepseek_v3

# 角色关系过滤llm
novel_role_relation_filter_llm = _qwen_max_llm
# 角色关系压缩llm
novel_role_relation_extractor_llm = _qwen_max_llm

chapter_summary_llm = _deepseek_r1

em_text_embedding_v3 = OpenAIEmbeddings(
    api_key=ALI_API_KEY,
    base_url=ALI_BASE_URL,
    model="text-embedding-v3",
)
em_hfe_pmmlv2 = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"  # 多语言模型
    # 可选其他模型如 "GanymedeNil/text2vec-large-chinese"（需提前下载）
)
novel_em = em_hfe_pmmlv2

