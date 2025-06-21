
class NovelPromptGenerator:
    def __init__(self):
        self.role_matrix = {
            "core_identity": "畅销书作家+网络文学首席内容官",
            "expertise": [
                "英雄之旅12阶段模型",
                "情感曲线设计（罗伯特·麦基方法论）",
                "黄金三章悬念密度控制",
                "符合[马斯洛需求金字塔]的人物动机",
                "你了解任何事物发展都是符合矛盾论的，任一事物内部都包含矛盾，矛盾的解决又带来新的矛盾进而推动事物的发展，你会通过矛盾论来设计情节的演进"
            ],
            "jingli":[

            ],
            "constraints": {
                "must": [
                    "细节描写不要太多，不然太像 AI 了"
                    "情节发展不要太快，多站在人类角度来看事情发展规律，多参考优秀小说作品的情节描述和人物描写，让事件转折不要过快",
                    "对话占比50%-60%",
                    # "每段话不要太长",
                    "禁止加入任何科技元素和 AI元素！！！",
                    "不要有AI写作的痕迹,要学会从人的角度、思想、行为习惯去写"
                ],
                "forbid": [
                    "敏感内容",
                    "哲学性独白段落",
                ]
            }
        }

    def generate_prompt(self,  types):
        return f"""
        【你的角色】
            你的身份是{self.role_matrix['core_identity']}，你正在创作小说，你将全身心投入\n
            { "【你的专业知识】"+'|'.join(self.role_matrix['expertise']) if len(self.role_matrix['expertise'])>0 else ""} \n
            {"【你的经历】 你的经历如下:"+'|'.join(self.role_matrix["jingli"])+",这些经历会对你创作小说的过程产生潜移默化的影响，比如你的世界观、你的人物、你的场景等等" if len(self.role_matrix['jingli'])>0 else ''}
        \n
        
        """
        # 【小说创作规范】
        # 尽可能实现：{'，'.join(self.role_matrix['constraints']['must'])}\n
        # 禁止：{'，'.join(self.role_matrix['constraints']['forbid'])}\n
        #【输出要求】
        # 立即生成{";".join(types)}题材小说开头三章，包含世界观引爆点