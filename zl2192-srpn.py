import re
# 23 r
r_value_list = [1804289383,
                846930886,
                1681692777,
                1714636915,
                1957747793,
                424238335,
                719885386,
                1649760492,
                596516649,
                1189641421,
                1025202362,
                1350490027,
                783368690,
                1102520059,
                2044897763,
                1967513926,     # 16
                1365180540,
                1540383426,
                304089172,
                1303455736,
                35005211,
                521595368,
                1804289383
                ]

# main stack
stack = [-2147483648,]
# whether stack has -2147483648 or it's appended later
minus_count = 1
operators = ['+', '-', '*', '/', '%', '^', '=', 'd', 'r', '#']
# polish back stack
stack_append = []
# counting now is which r
r_count = 0
# hash_count == 1 means still in comment, 0 means out of comment now
hash_count = 0

# whether the str can be converted into number(minus number can be recognized)
def is_digit(x):
    try:
        x = int(x)
        return isinstance(x, int)
    except ValueError:
        return False

# turns normal format into polish notation, return a str which is in polish format
def convert_to_polish(s):
    """
    1. receive a str from calculate() function
    2. transfer it into polish notation
    3. return the str with space which is waiting for the main function to recognize them by space
    """
    # split the input s by operator, get a list (if it's -5, just keep it still)
    splited_s = re.split(r'(\+|\-[0-9]+|\-|\*|\/|=|d|\^|\%)', s)
    # set priority
    priority_dict = {'+': 1, '-': 1, '*': 3, '/': 3, '=': 6, 'd': 0, '^': 5, '%': 4}
    operators_list = []  # used for storing operators
    result = ''  # return the result in polish notation

    # for-loop the whole list
    for i in splited_s:
        # recognize "-" is an operator or negative number
        if re.match(r'(\-\d+)', i):
            if splited_s.index(i) == 0:
                continue
            elif splited_s.index(i) != 0:
                # if it has a number before "-", "-" is a sign
                if splited_s[splited_s.index(i)-1].isdigit():
                    for m in i:
                        splited_s.insert(splited_s.index(i), m)
                    operators_list.append('-')
                    del splited_s[splited_s.index(i)]
                    continue
        # operator
        if i == '+' or i == '-' or i == '*' or i == '/' or i == 'd' or i == '=' or i == '^' or i == '%':
            # put it into li list(first)
            if len(operators_list) == 0:
                operators_list.append(i)
            # compare the new operator coming in with the operators already in li list
            elif (priority_dict[operators_list[-1]] <= priority_dict[i] and priority_dict[operators_list[0]] <= priority_dict[i]):
                for p in operators_list:
                    # one of the operator in li is greater than the new one
                    if priority_dict[p] > priority_dict[i]:
                        # pop out all in li, then append the new one into li
                        while len(operators_list) > 0:
                            result += " " + operators_list.pop()
                        operators_list.append(i)
                    # the new operator is greater than any in the li list, append it into li too
                    else:
                        operators_list.append(i)
                        break
            else:
                # pop out all operator in li
                while len(operators_list) > 0:
                    result += " " + operators_list.pop()
                operators_list.append(i)
        # number
        else:
            result += " " + i
    # pop out the rest of the operators in li
    while len(operators_list) > 0:
        result += " " + operators_list.pop()
    return result


# calculet the stuff coming in
def calculate(stuff):
    """
    1.split stuff by space
    2.send them into convert_to_polish() which can change format into convert polish notation
    3.return polish notation from convert_to_polish() back to this function
    4.split them by space again, then start to calculate(numbers, operators)
    """
    global minus_count
    stack_append.clear()
    # split stuff by space
    stuff_split = str(stuff).split(" ")
    # push it to polish transfer
    for m in stuff_split:
        result = convert_to_polish(m)
        # split the result taken from polish-convert by space, make a list
        split_by_space = result.split(" ")
        # for-loop this list, put them into stack_append list
        for l in split_by_space:
            stack_append.append(l)
    # for-loop stack_append list
    for i in stack_append:
        try:
            global hash_count
            if hash_count == 0:
                # meet first hash, ignore everything until it meets the second hash, change hash_count to 0
                if i == "#":
                    hash_count += 1
                    continue
                # no hash at all, calculate normally
                if i != "#":
                    # it's "", empty, ignore it
                    if i == "":
                        continue
                    # it's number
                    elif i not in operators and i != "" and is_digit(i):
                        # hit the ceiling, just append the ceiling number
                        if int(i) >= 2147483647:
                            stack.append(2147483647)
                        # hit the bottom, just append the bottom number
                        elif int(i) <= -2147483648:
                            stack.append(-2147483648)
                        # normal number in range, append in
                        else:
                            if int(stack[0] == -2147483648) and minus_count == 1:
                                stack[0] = int(i)
                                minus_count += 1
                            elif int(stack[0] == -2147483648) and minus_count != 1:
                                stack.append(int(i))
                            else:
                                stack.append(int(i))
                    # it's operator
                    elif i == '+':
                        top1 = stack.pop()
                        top2 = stack.pop()
                        # check the range
                        if top1 + top2 >= 2147483647:
                            stack.append(2147483647)
                        else:
                            stack.append(top1 + top2)
                    elif i == '-':
                        top1 = stack.pop()
                        top2 = stack.pop()
                        # check the range
                        if (top2 - top1) <= -2147483648:
                            stack.append(-2147483648)
                        else:
                            stack.append(top2 - top1)
                    elif i == '*':
                        top1 = stack.pop()
                        top2 = stack.pop()
                        # check the range
                        if (top1 * top2) >= 2147483647:
                            stack.append(2147483647)
                        elif (top1 * top2) <= -2147483648:
                            stack.append(-2147483648)
                        else:
                            stack.append(top1 * top2)
                    elif i == '/':
                        top1 = stack.pop()
                        top2 = stack.pop()
                        stack.append(top2 // top1)
                    elif i == '=':
                        print(stack[-1])
                    elif i == '%':
                        top1 = stack.pop()  # divisor
                        top2 = stack.pop()  # dividend
                        if top2 < 0 and top1 > 0:       # -11%3 = -2
                            divided_result = -(-top2 % top1)
                            stack.append(divided_result)
                        elif top2 > 0 and top1 < 0:     # 11%-3 = 2
                            divided_result = (top2 % -top1)
                            stack.append(divided_result)
                        elif top2 < 0 and top1 < 0:     # -11%-3 = -2
                            divided_result = -(-top2 % -top1)
                            stack.append(divided_result)
                        elif top2 > 0 and top1 > 0:     # 11%3 = 2
                            stack.append(top2 % top1)
                    # print out all in stack
                    elif i == 'd':
                        for j in stack:
                            print(j)
                    elif i == 'r':
                        global r_count
                        if r_count >= 23:
                            r_count = 23
                            print('Stack underflow.')
                        elif r_count < 23:
                            stack.append(r_value_list[r_count])
                            r_count += 1
                    elif i == '^':
                        top1 = stack.pop()
                        top2 = stack.pop()
                        # check the range
                        if (top2 ** top1) >= 2147483647:
                            stack.append(2147483647)
                        # minus power
                        elif (top2 ** top1) < 1:
                            print('Negative power.')
                            stack.append(top2)
                            stack.append(top1)
                        else:
                            stack.append(top2 ** top1)
                    # the thing following the first hash, should be ignored
                    else:
                        print("Unrecognised operator or operand \"%s\"" % i)
                        continue
            if hash_count == 1:
                # comment, ignore it
                if i != "#":
                    continue
                if i == "#":
                    # meet the second hash, change hash_count in order to calculate normally
                    hash_count = 0
                    continue
        # only one time pop succeed
        except IndexError:
            print('Stack underflow.')
            stack.append(top1)
            continue
            # self.calculate()
        # divide by 0
        except ZeroDivisionError:
            print('Divide by 0.')
            stack.append(top2)
            stack.append(top1)
# entrance
def srpn():
    while 1:
        stuff = input()
        calculate(stuff)

# main
if __name__ == '__main__':
    print('start!')
    srpn()