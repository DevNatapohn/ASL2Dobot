import csv

def logging_csv(number, mode, landmark_list):
    if mode == 0:
        return
    if (mode in [1, 2]) and (0 <= number <= 35):
        csv_path = "model/handpose_classifier/handpose_points.csv"
        with open(csv_path, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([number, *landmark_list])