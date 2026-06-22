"""Organize cards with a small CardDeck class."""
from dataclasses import dataclass, field


@dataclass
class CardDeck:
    name: str
    cards: list[str] = field(default_factory=list)

    def add(self, card: str) -> None:
        self.cards.append(card)

    def summary(self) -> str:
        return f"{self.name}: {len(self.cards)} 张卡片"


deck = CardDeck("第5章复习盒")
deck.add("类是图纸，对象是实例。")
deck.add("方法是对象能执行的动作。")
print(deck.summary())
