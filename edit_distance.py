# Author: Antonio Lang
# Date: 20 February 2023

def calc_min_edit_dist(source, target) -> int:
    return get_edit_table(source, target)[len(source)][len(target)]

def align(source, target) -> tuple:
    pass

def get_edit_table(source, target) -> list:
    # target word on x-axis, source on y-axis
    # on re-visit, try code as described in book with initial n and m values flipped
    insert_cost = delete_cost = 1
    substitute_cost = 2

    n = len(target)
    m = len(source)
    edit_table = [[0 for i in range(n+1)] for j in range(m+1)]

    for i in range(1,n+1): # for each column
        edit_table[0][i] = edit_table[0][i-1] + insert_cost
    for j in range(1,m+1): # for each row
        edit_table[j][0] = edit_table[j-1][0] + delete_cost

    for i in range(1,m+1):
        for j in range(1, n+1):
            edit_table[i][j] = min(edit_table[i-1][j] + delete_cost,
                                   edit_table[i-1][j-1] + substitute_cost,
                                   edit_table[i][j-1] + insert_cost)
    for line in edit_table:
        print(line)
    return edit_table

if __name__ == "__main__":
    print(calc_min_edit_dist("intention", "execution"))