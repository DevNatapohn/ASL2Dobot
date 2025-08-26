import copy
import itertools

def pre_process_landmark(landmark_list):
    temp_landmark_list = copy.deepcopy(landmark_list)

    base_x, base_y = temp_landmark_list[0]
    for index, (x, y) in enumerate(temp_landmark_list):
        temp_landmark_list[index][0] = x - base_x
        temp_landmark_list[index][1] = y - base_y

    temp_landmark_list = list(itertools.chain.from_iterable(temp_landmark_list))
    max_value = max(map(abs, temp_landmark_list))
    return [n / max_value for n in temp_landmark_list]
