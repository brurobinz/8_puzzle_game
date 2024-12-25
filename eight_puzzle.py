from colorama import Fore, Back, Style
from copy import deepcopy

BEGIN = []
END = []
MOVE_DIRECTIONS = {"U": [-1, 0], "D": [1, 0], "L": [0, -1], "R": [0, 1]}
left_down_angle = "\u2514"
right_down_angle = "\u2518"
right_up_angle = "\u2510"
left_up_angle = "\u250C"

middle_junction = "\u253C"
top_junction = "\u252C"
bottom_junction = "\u2534"
right_junction = "\u2524"
left_junction = "\u251C"
bar = Style.BRIGHT + Fore.CYAN + "\u2502" + Fore.RESET + Style.RESET_ALL
dash = "\u2500"

first_line = (
    Style.BRIGHT
    + Fore.CYAN
    + left_up_angle
    + dash
    + dash
    + dash
    + top_junction
    + dash
    + dash
    + dash
    + top_junction
    + dash
    + dash
    + dash
    + right_up_angle
    + Fore.RESET
    + Style.RESET_ALL
)
middle_line = (
    Style.BRIGHT
    + Fore.CYAN
    + left_junction
    + dash
    + dash
    + dash
    + middle_junction
    + dash
    + dash
    + dash
    + middle_junction
    + dash
    + dash
    + dash
    + right_junction
    + Fore.RESET
    + Style.RESET_ALL
)
last_line = (
    Style.BRIGHT
    + Fore.CYAN
    + left_down_angle
    + dash
    + dash
    + dash
    + bottom_junction
    + dash
    + dash
    + dash
    + bottom_junction
    + dash
    + dash
    + dash
    + right_down_angle
    + Fore.RESET
    + Style.RESET_ALL
)


class Node:
    def __init__(self, current_node, previous_node, g, h, move):
        self.current_node = current_node
        self.previous_node = previous_node
        self.g = g
        self.h = h
        self.move = move

    def f(seft):
        return seft.g + seft.h


def input_matrix():
    print("Nhập ma trận đầu:")
    for row in range(3):
        BEGIN.append([int(x) for x in input().split()])
    print("Nhập ma trận đích:")
    for row in range(3):
        END.append([int(x) for x in input().split()])


def print_matrix(matrix):
    print(first_line)
    for row in range(len(matrix)):
        for value in matrix[row]:
            if value == 0:
                print(bar, Back.RED + " " + Back.RESET, end=" ")
            else:
                print(bar, value, end=" ")
        print(bar)
        if row == 2:
            print(last_line)
        else:
            print(middle_line)


def get_position_matrix(BEGIN, END):
    index_dict = {}
    index = 0
    for row in END:
        for value in row:
            index_dict[value] = index
            index += 1
    position_array = []
    for row in BEGIN:
        for value in row:
            if value != 0:
                position_array.append(index_dict[value])
    return position_array


def is_solvable(BEGIN, END):
    inv_count = 0
    position_arr = get_position_matrix(BEGIN, END)
    for i in range(0, 8):
        for j in range(i + 1, 8):
            if position_arr[j] < position_arr[i]:
                inv_count += 1
    return inv_count % 2 == 0


def get_pos(element, matrix):
    for row in range(len(matrix)):
        if element in matrix[row]:
            return (row, matrix[row].index(element))


def move_emty_tile(matrix, move):
    emty_tile = get_pos(0, matrix)
    new_row = emty_tile[0] + MOVE_DIRECTIONS[move][0]
    new_col = emty_tile[1] + MOVE_DIRECTIONS[move][1]
    if 0 <= new_row < len(matrix) and 0 <= new_col < len(matrix):
        matrix[emty_tile[0]][emty_tile[1]], matrix[new_row][new_col] = (
            matrix[new_row][new_col],
            matrix[emty_tile[0]][emty_tile[1]],
        )
        return matrix
    else:
        return None

def manhattan_distance(matrix):
    cost = 0
    for row in range(len(matrix)):
        for col in range(len(matrix[row])):
            if matrix[row][col] != 0:
                pos = get_pos(matrix[row][col], END)
                target_row, target_col = pos
                cost += abs(row - target_row) + abs(col - target_col)
    return cost


def get_adj_node(node):
    list_node = []

    for move in MOVE_DIRECTIONS.keys():
        new_state = move_emty_tile(deepcopy(node.current_node), move)
        if new_state != None:
            list_node.append(
                Node(
                    new_state,
                    node.current_node,
                    node.g + 1,
                    manhattan_distance(new_state),
                    move,
                )
            )
    return list_node


def get_best_node(OPEN):
    return min(OPEN.values(), key=lambda node: node.f())


def build_path(CLOSE):
    node = CLOSE[str(END)]
    branch = list()

    while node.move:
        branch.append({"move": node.move, "node": node.current_node})
        node = CLOSE[str(node.previous_node)]
    branch.append({"move": "", "node": node.current_node})
    branch.reverse()
    return branch


def main(puzzle):
    OPEN = {str(puzzle): Node(puzzle, puzzle, 0, manhattan_distance(puzzle), "")}
    CLOSE = {}
    while True:
        best_node = get_best_node(OPEN)
        CLOSE[str(best_node.current_node)] = best_node
        if best_node.current_node == END:
            print("CLOSE: " + str(len(CLOSE)))
            return build_path(CLOSE)

        adj_node = get_adj_node(best_node)

        for node in adj_node:
            if (
                str(node.current_node) in CLOSE.keys()
                or str(node.current_node) in OPEN.keys()
                and OPEN[str(node.current_node)].f() < node.f()
            ):
                continue
            OPEN[str(node.current_node)] = node

        del OPEN[str(best_node.current_node)]
def print_example_matrix():
    example_matrix = [
        [1, 2, 3],
        [3, 4, 6],
        [7, 8, 0]
    ]

    print("Ví dụ nhập ma trận:")
    for row in example_matrix:
        for value in row:
            print(value, end=' ')
        print()

if __name__ == "__main__":
    print_example_matrix()
    def count_elements(matrix):
        count = 0
        for row in matrix:
            count += len(row)
        return count
    while True:
        try:
            input_matrix()
            print(count_elements(BEGIN) + count_elements(END))
            if(count_elements(BEGIN) + count_elements(END) == 18):
                break
            else:
                print("Nhập không đúng vui lòng nhập lại.")
        except ValueError:
            print("Nhập không đúng vui lòng nhập lại.")
        
    if is_solvable(BEGIN, END):
        print("Ma trận khởi tạo có thể trở thành ma trận đích!")
    else:
        print("Ma trận khởi tạo không thể trở thành ma trận đích!")
        exit()
    br = main(BEGIN)
    print("Tổng số bước di chuyển : ", len(br) - 1)
    print()
    print(dash + dash + right_junction, "INPUT", left_junction + dash + dash)
    for b in br:
        if b["move"] != "":
            letter = ""
            if b["move"] == "U":
                letter = "UP"
            elif b["move"] == "R":
                letter = "RIGHT"
            elif b["move"] == "L":
                letter = "LEFT"
            elif b["move"] == "D":
                letter = "DOWN"
            print(dash + dash + right_junction, letter, left_junction + dash + dash)
        print_matrix(b["node"])
        print()

    print(dash + dash + right_junction, "ABOVE IS THE OUTPUT", left_junction + dash + dash)



