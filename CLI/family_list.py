def print_families():
    print('Here is a list of protein families\' names:\n')
    with open('families') as f:
        families = f.read().splitlines()
        print(*families, sep=', ')