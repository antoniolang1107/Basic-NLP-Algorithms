# Author: Antonio Lang
# Date: 25 February 2023

class Node():
    def __init__(self, value=0) -> None:
        self.value = value
        self.path = None
    def __str__(self) -> str:
        return f"{self.value}"

def calc_min_edit_dist(source, target) -> int:
    return get_edit_table(source, target)[len(source)][len(target)]

def align(source, target) -> tuple:
    table = get_edit_table(source, target)
    path = []
    cur_node = table[len(target)-1][len(source)-1]
    while cur_node.path != None:
        path.append(cur_node.path[0])
        cur_node = cur_node.path[1]
    path.reverse()
    align_source = []
    align_target = []
    source_change = 0
    target_change = 0

    for index, operation in enumerate(path):
        if operation == "i": # add * to source
            align_source.append("*")
            align_target.append(target[index-target_change])
            source_change+=1
        if operation == "d": # add * to target
            align_source.append(source[index-source_change])
            align_target.append("*")
            target_change+=1
        if operation == " " or operation == "s":
            align_source.append(source[index-source_change])
            align_target.append(target[index-target_change])
    return "".join(align_source), "".join(align_target), path

def get_edit_table(source, target) -> list:
    # target word on x-axis, source on y-axis
    
    insert_cost = delete_cost = 1
    source_copy = '#' + source
    target_copy = '#' + target
    n = len(target)+1
    m = len(source)+1
    edit_table = [[0]*n for j in range(m)]
    edit_table = [[Node(0) for i in range(n)] for j in range(m)]

    for i in range(1,m): # for each column
        edit_table[i][0].value = i
    for j in range(1,n): # for each row
        edit_table[0][j].value = j

    calc_table(source_copy, target_copy, edit_table)
    return edit_table

def calc_table(source, target, edit_table):
    for i in range (1,len(source)):
        for j in range(1,len(target)):
            if source[i-1]==target[j-1]:
                edit_table[i][j].value = edit_table[i-1][j-1].value
                edit_table[i][j].path = (" ", edit_table[i-1][j-1])
            else:
                index_list = [(i-1,j), (i-1, j-1), (i, j-1)]
                operations = ['i', 's', 'd']
                operation_costs = [edit_table[i-1][j].value, 
                                edit_table[i-1][j-1].value+1,
                                edit_table[i][j-1].value]
                min_index = operation_costs.index(min(operation_costs))
                edit_table[i][j].value = operation_costs[min_index]+1
                edit_table[i][j].path = (operations[min_index], edit_table[index_list[min_index][0]][index_list[min_index][1]])

if __name__ == "__main__":
    print(calc_min_edit_dist("intention", "execution"))
    print(align("intention", "execution"))