import os
import cv2 as cv
import copy
import numpy as np
import imageio  # ต้องติดตั้ง: pip install imageio

from core.hand_utils import calc_bounding_rect, calc_landmark_list
from core.preprocess import pre_process_landmark
from core.logger import logging_csv

datasetdir = "model/dataset/datasets"
gif_dir = "assets/loading_gif"  # โฟลเดอร์เก็บ GIF
gif_name = "loading.gif"        # ชื่อไฟล์ GIF

def show_loading_gif(gif_path, window_name="Hand Gesture Recognition", duration=1000):
    """อ่าน GIF และแสดง animation แทน Loading"""
    try:
        frames = [cv.cvtColor(frame, cv.COLOR_RGB2BGR) for frame in imageio.mimread(gif_path)]
        start = cv.getTickCount()
        i = 0
        while True:
            cv.imshow(window_name, frames[i % len(frames)])
            if cv.waitKey(50) & 0xFF == 27:  # ESC เพื่อออก
                break
            i += 1
            if (cv.getTickCount() - start) / cv.getTickFrequency() * 1000 > duration:
                break
    except Exception as e:
        print(f"ไม่สามารถโหลด GIF {gif_path}: {e}")

def process_image(img, hands, mode, imglabel):
    """Process ภาพเดี่ยว"""
    if img is None:
        return
    debug_img = copy.deepcopy(img)
    img_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    img_rgb.flags.writeable = False
    results = hands.process(img_rgb)
    img_rgb.flags.writeable = True

    if results.multi_hand_landmarks is not None:
        for hand_landmarks in results.multi_hand_landmarks:
            brect = calc_bounding_rect(debug_img, hand_landmarks)
            landmark_list = calc_landmark_list(debug_img, hand_landmarks)
            pre_processed = pre_process_landmark(landmark_list)
            logging_csv(imglabel, mode, pre_processed)

def process_video(video_path, hands, mode, imglabel):
    """Process วิดีโอ"""
    cap = cv.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"ไม่สามารถเปิดวิดีโอ: {video_path}")
        return
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        process_image(frame, hands, mode, imglabel)
    cap.release()

def process_dataset(hands, mode):
    # แสดง GIF loading
    gif_path = os.path.join(gif_dir, gif_name)
    if os.path.exists(gif_path):
        show_loading_gif(gif_path, duration=1000)
    else:
        loading_img = 255 * np.ones((200, 400, 3), dtype=np.uint8)
        cv.putText(loading_img, "Loading...", (20, 100),
                   cv.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), 2, cv.LINE_AA)
        cv.imshow("Hand Gesture Recognition", loading_img)
        cv.waitKey(1000)

    # นับจำนวนไฟล์ทั้งหมด
    total_files = 0
    for imgclass in os.listdir(datasetdir):
        class_path = os.path.join(datasetdir, imgclass)
        if not os.path.isdir(class_path):
            continue
        total_files += len([f for f in os.listdir(class_path) if os.path.isfile(os.path.join(class_path, f))])

    print(f"Total files to process: {total_files}")

    imglabel = -1
    processed_count = 0
    success_count = 0
    fail_count = 0

    for imgclass in os.listdir(datasetdir):
        imglabel += 1
        class_path = os.path.join(datasetdir, imgclass)
        if not os.path.isdir(class_path):
            continue
        for fname in os.listdir(class_path):
            fpath = os.path.join(class_path, fname)
            processed_count += 1
            print(f"Processing file {processed_count}/{total_files}: {fpath}")
            try:
                ext = fname.lower().split('.')[-1]
                if ext in ["jpg", "jpeg", "png"]:
                    img = cv.imread(fpath)
                    if img is None:
                        print(f"ไม่สามารถอ่านภาพ: {fpath}")
                        fail_count += 1
                        continue
                    process_image(img, hands, mode, imglabel)
                    success_count += 1
                elif ext in ["avi", "mp4"]:
                    process_video(fpath, hands, mode, imglabel)
                    success_count += 1
                else:
                    print(f"ไฟล์ไม่รองรับ: {fpath}")
                    fail_count += 1
            except Exception as e:
                print(f"ปัญหากับไฟล์ {fpath}: {e}")
                fail_count += 1

    print(f"สิ้นสุดการทำงาน! อ่านได้ {success_count} ไฟล์, อ่านไม่ได้ {fail_count} ไฟล์")
    cv.destroyAllWindows()
