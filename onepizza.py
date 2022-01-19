from itertools import combinations
from sys import argv, stdin


def get_input(input_file_name):
    lines = []

    with open(input_file_name) as f:
        for line in f:
            lines.append(line)

    c = int(lines[0])
    customers = []

    for x in range(1, 2*c, 2):
        likes = lines[x].split()[1:]
        dislikes = lines[x+1].split()[1:]

        customers.append((likes, dislikes))

    return c, customers


def get_all_ingredients(customers):
    all_ingredients = set()

    for like, dislike in customers:
        all_ingredients |= set(like)
        all_ingredients |= set(dislike)

    return list(all_ingredients)


def score_toppings(toppings, customers):
    return sum(all(like in toppings for like in likes) and not any(dislike in toppings for dislike in dislikes) for likes, dislikes in customers)


def solve_brute(c, customers):
    all_ingredients = get_all_ingredients(customers)
    best = (0, [])

    for topping_count in range(len(all_ingredients)+1):
        for toppings in combinations(all_ingredients, topping_count):
            score = score_toppings(toppings, customers)
            if score > best[0]:
                best = (score, toppings)

    return best[1]


def write_results(solution, file_name):
    with open(file_name, 'w') as f:
        f.write(f'{len(solution)} {" ".join(solution)}')

input_file_name = argv[1]
c, customers = get_input(input_file_name)
solution = solve_brute(c, customers)
output_file_name = '.'.join(map(lambda part: 'out' if part == 'in' else part, input_file_name.split('.')))

write_results(solution, output_file_name)