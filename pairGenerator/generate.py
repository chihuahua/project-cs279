import random

# value to generate a random set of pairs for.
N = 502

pairs = []
for i in range(N):
  for j in range(i + 1, N):
    pair = [i, j]
    random.shuffle(pair)
    pairs.append(pair)

random.shuffle(pairs)
for pair in pairs:
  print `pair[0]` + "\t" + `pair[1]`

