import itertools

steps = [
    0,
    [0, 1, 2],
    2
]


print()
print('Expected'.center(50, '='))

expected = [
    1 / 3,
    1 / 3 / 3,
    1 / 3 / 3,
    1 / 3 / 3,
    1 / 3,
]
print(*expected)
print(sum(expected))


print()
print('Actual'.center(50, '='))
def stage_progress(steps, weight = 1):
    steps_count = len(steps)
    for step in steps:
        if isinstance(step, int):
            yield weight / steps_count
        else:
            for val in stage_progress(step, weight / steps_count):
                yield val


print(*stage_progress(steps))
print(sum(stage_progress(steps)))
print(*itertools.accumulate(stage_progress(steps)))
print()


expected = [
    1 / 5,
    1 / 5,
    1 / 5 / 3,
    1 / 5 / 3,
    1 / 5 / 3,
    1 / 5 / 3,
    1 / 5 / 3,
    1 / 5 / 3 / 3,
    1 / 5 / 3 / 3,
    1 / 5 / 3 / 3,
    1 / 5
]
print('Expected'.center(50, '='))
print(*itertools.accumulate(expected))
print()

print('Actual'.center(50, '='))

print(*itertools.accumulate(stage_progress([
    1,
    1,
    [1, 2, 3],
    [1, 2, [
        1, 2, 3
    ]],
    1
])))
print()