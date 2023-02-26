# Author: Antonio Lang
# Date: 25 February 2023

class Node():
    def __init__(self, value=0) -> None:
        self.value = value
        self.path = None

def calc_min_edit_dist(source, target) -> int:
    return get_edit_table(source, target)[len(target)][len(source)].value

def align(source, target) -> tuple:
    table = get_edit_table(source, target)
    path = []
    dummy = table[len(target)][len(source)]
    cur_node = dummy
    while cur_node.path != None:
        path.append(cur_node.path[0])
        cur_node = cur_node.path[1]
    path.reverse()
    return path

def get_edit_table(source, target) -> list:
    # target word on x-axis, source on y-axis
    # on re-visit, try code as described in book with initial n and m values flipped
    insert_cost = delete_cost = 1

    source_copy = '#'.join(source)
    target_copy = '#'.join(target)
    n = len(source_copy)
    m = len(target_copy)
    edit_table = [[Node(0) for i in range(n)] for j in range(m)]

    for i in range(1,m): # for each column
        edit_table[i][0].value = edit_table[i-1][0].value + insert_cost
        edit_table[i][0].path = edit_table[i-1][0]
    for j in range(1,n): # for each row
        edit_table[0][j].value = edit_table[0][j-1].value + delete_cost
        edit_table[0][j].path = edit_table[0][j-1]

    calc_table(source_copy, target_copy, edit_table)
    return edit_table

def calc_table(source, target, edit_table):
    for i in range(1,len(source)):
        for j in range(1, len(target)):
            substitute = (2,"s", edit_table[i-1][j-1]) if source[i] != target[j] else (0," ", edit_table[i-1][j-1])
            operation = [(1,"d", edit_table[i-1][j]), substitute, (1,"i", edit_table[i][j-1])]
            operation_costs = [edit_table[i-1][j].value + 1, 
                               edit_table[i-1][j-1].value + substitute[0],
                               edit_table[i][j-1].value + 1]
            min_index = operation_costs.index(min(operation_costs))
            edit_table[i][j] = Node(operation_costs[min_index])
            edit_table[i][j].path = (operation[min_index][1], operation[min_index][2])

if __name__ == "__main__":
    # print(calc_min_edit_dist("intention", "execution"))
    print(align("intention", "execution"))
    # print(calc_min_edit_dist("traps", "tricks"))