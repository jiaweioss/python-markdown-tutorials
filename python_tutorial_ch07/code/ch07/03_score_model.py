"""Score logic separated from pygame drawing."""
def update_score(score: int, correct: bool) -> int:
    return score + 10 if correct else max(0, score - 5)


score = 0
for result in [True, True, False, True]:
    score = update_score(score, result)
print("最终得分：", score)
