def get_multiplier(target_size):
    if target_size <= 5:
        return 2
    elif target_size >= 30:
        return 0.01
    else:
        return 2 - (target_size - 5) * (2 - 0.01) / (30 - 5)

x = list(range(35))
y = [get_multiplier(x) for x in x]

for i in range(35):
    print(x[i], y[i])