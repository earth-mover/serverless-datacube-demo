import random

import coiled


@coiled.function()
def estimate_pi(n: int) -> float:
    total = 0
    for _ in range(n):
        x = random.random()
        y = random.random()
        if x**2 + y**2 < 1:
            total += 1
    return total / n * 4


pi = estimate_pi(100_000)
print(pi)
