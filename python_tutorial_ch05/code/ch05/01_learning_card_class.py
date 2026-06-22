"""Define and use a LearningCard class."""
from dataclasses import dataclass


@dataclass
class LearningCard:
    topic: str
    question: str
    answer: str
    tags: list[str]

    def preview(self) -> str:
        return f"[{self.topic}] {self.question} -> {self.answer[:20]}..."


card = LearningCard("Python", "变量是什么？", "变量像贴在数据上的标签。", ["基础", "比喻"])
print(card.preview())
