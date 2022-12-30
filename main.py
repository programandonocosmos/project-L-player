from compute_actions import compute, MemoizationStruct
from projectl import ProjectLGame
import random
import time
import matplotlib.pyplot as plt
import statistics


def run_game() -> None:
    game = ProjectLGame()
    mem = MemoizationStruct.new()
    running = True
    while running:
        possible_actions = compute(game, mem)
        if len(possible_actions) == 0:
            break
        random_action, _ = random.choice(possible_actions)
        _, __, running = game.step(random_action)


def get_game_time() -> float:
    initial_time = time.time()
    run_game()
    return time.time() - initial_time


def tap(x: float) -> float:
    print(x)
    return x


x = list(range(100))
y = [tap(get_game_time()) for _ in x]

m = statistics.fmean(y)
v = statistics.variance(y, m)

print(f"quantity of examples: {len(x)}")
print(f"mean: {m}")
print(f"variance: {v}")

plt.plot(x, y, color="r", label="times")
plt.plot(x, [m for _ in x], color="g", label="average")
plt.show()
