import re

with open("/users/zcm/Downloads/SoNovel-macOS_arm64/downloads/无敌六皇子(梁山老鬼).txt", 'r', encoding='utf-8') as f:
    content = f.read()
# 匹配所有章节，包括标题和内容，直到下一个标题或文件结束
pattern = re.compile(r'第\d+章.*?(?=\s*第\d+章|\Z)', re.DOTALL)
chapters = pattern.findall(content)
# 去除每个章节的末尾空白
chapters = [chap.strip() for chap in chapters]
print(chapters)