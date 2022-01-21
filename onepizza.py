from itertools import combinations
from sys import argv, setrecursionlimit

setrecursionlimit(11000)


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


def write_results(solution, file_name):
    with open(file_name, 'w') as f:
        f.write(f'{len(solution)} {" ".join(solution)}')


def get_all_ingredients(customers):
    all_ingredients = set()

    for like, dislike in customers:
        all_ingredients |= set(like)
        all_ingredients |= set(dislike)

    return list(all_ingredients)


def score_toppings(toppings, customers):
    return sum(all(like in toppings for like in likes) and not any(dislike in toppings for dislike in dislikes) for likes, dislikes in customers)


def solve_brute(customers):
    all_ingredients = get_all_ingredients(customers)
    best = (0, [])

    for topping_count in range(len(all_ingredients)+1):
        for toppings in combinations(all_ingredients, topping_count):
            score = score_toppings(toppings, customers)
            if score > best[0]:
                best = (score, toppings)

    return best[1]


def solve_smarter(customers, output_file_name):
    best = 0
    frontier = [(0, set(), 0)]
    print(f'Working with {len(customers)} customers.')

    for fed, used, pos in frontier:
        if fed > best:
            print(f'Found a {fed} at position {pos}')
            best = fed
            write_results(list(used), output_file_name)
        
        if pos == len(customers):
            continue

        if not any(dislike in used for dislike in customers[pos][1]):
            frontier.append((fed+1, used | set(customers[pos][0]), pos+1))
        frontier.append((fed, set(used), pos+1))


def solve_smarter_and_slicker(customers, output_file_name):
    best = 0
    customers.sort(lambda customer: len(customer[0]) + len(customer[1]))
    
    def dfs(pos, fed, used, forbidden, customers, output_file_name):
        nonlocal best

        if fed > best:
            print(f'Found a {fed} at position {pos} out of {len(customers)}')
            best = fed
            write_results(list(used), output_file_name)
        
        if pos == len(customers):
            return

        canbeadded = not any(dislike in used for dislike in customers[pos][1]) and not any(like in forbidden for like in customers[pos][0])

        if canbeadded:
            new_ingredients = set(customers[pos][0]) - used
            used |= new_ingredients
            new_forbidden = set(customers[pos][1]) - forbidden
            forbidden |= new_forbidden
            dfs(pos+1, fed+1, used, forbidden, customers, output_file_name)
            used -= new_ingredients
            forbidden -= new_forbidden

        dfs(pos+1, fed, used, forbidden, customers, output_file_name)

    dfs(0, 0, set(), set(), customers, output_file_name)


input_file_name = argv[1]
c, customers = get_input(input_file_name)
output_file_name = '.'.join(map(lambda part: 'out' if part == 'in' else part, input_file_name.split('.')))
solve_smarter_and_slicker(customers, output_file_name)