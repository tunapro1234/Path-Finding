nodes = [3, 2, 1]

for i in range(len(nodes) - 1):
    for j in range(len(nodes) - i):
        if len(nodes) > j + 1 and nodes[j] > nodes[j + 1]:
            nodes[j], nodes[j + 1] = nodes[j + 1], nodes[j]

print(nodes)