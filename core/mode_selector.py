def select_mode(key, mode):
    number = -1
    if 65 <= key <= 90:  # A-Z
        number = key - 65
    if key == 110:  # n
        mode = 0
    if key == 107:  # k
        mode = 1
    if key == 100:  # d
        mode = 2
    return number, mode