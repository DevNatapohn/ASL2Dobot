# core/draw_utils.py
import cv2 as cv

# วาดเส้นและจุดสำคัญของมือบนภาพ
def draw_landmarks(image, landmark_point):
    if len(landmark_point) > 0:
        # วาดเส้นเชื่อมข้อต่าง ๆ ของนิ้วแต่ละนิ้วและฝ่ามือ
        # Thumb
        cv.line(image, tuple(landmark_point[2]), tuple(landmark_point[3]), (0,0,0), 6)
        cv.line(image, tuple(landmark_point[2]), tuple(landmark_point[3]), (255,255,255), 2)
        cv.line(image, tuple(landmark_point[3]), tuple(landmark_point[4]), (0,0,0), 6)
        cv.line(image, tuple(landmark_point[3]), tuple(landmark_point[4]), (255,255,255), 2)
        # Index finger
        cv.line(image, tuple(landmark_point[5]), tuple(landmark_point[6]), (0,0,0), 6)
        cv.line(image, tuple(landmark_point[5]), tuple(landmark_point[6]), (255,255,255), 2)
        cv.line(image, tuple(landmark_point[6]), tuple(landmark_point[7]), (0,0,0), 6)
        cv.line(image, tuple(landmark_point[6]), tuple(landmark_point[7]), (255,255,255), 2)
        cv.line(image, tuple(landmark_point[7]), tuple(landmark_point[8]), (0,0,0), 6)
        cv.line(image, tuple(landmark_point[7]), tuple(landmark_point[8]), (255,255,255), 2)
        # Middle finger
        cv.line(image, tuple(landmark_point[9]), tuple(landmark_point[10]), (0,0,0), 6)
        cv.line(image, tuple(landmark_point[9]), tuple(landmark_point[10]), (255,255,255), 2)
        cv.line(image, tuple(landmark_point[10]), tuple(landmark_point[11]), (0,0,0), 6)
        cv.line(image, tuple(landmark_point[10]), tuple(landmark_point[11]), (255,255,255), 2)
        cv.line(image, tuple(landmark_point[11]), tuple(landmark_point[12]), (0,0,0), 6)
        cv.line(image, tuple(landmark_point[11]), tuple(landmark_point[12]), (255,255,255), 2)
        # Ring finger
        cv.line(image, tuple(landmark_point[13]), tuple(landmark_point[14]), (0,0,0), 6)
        cv.line(image, tuple(landmark_point[13]), tuple(landmark_point[14]), (255,255,255), 2)
        cv.line(image, tuple(landmark_point[14]), tuple(landmark_point[15]), (0,0,0), 6)
        cv.line(image, tuple(landmark_point[14]), tuple(landmark_point[15]), (255,255,255), 2)
        cv.line(image, tuple(landmark_point[15]), tuple(landmark_point[16]), (0,0,0), 6)
        cv.line(image, tuple(landmark_point[15]), tuple(landmark_point[16]), (255,255,255), 2)
        # Pinky finger
        cv.line(image, tuple(landmark_point[17]), tuple(landmark_point[18]), (0,0,0), 6)
        cv.line(image, tuple(landmark_point[17]), tuple(landmark_point[18]), (255,255,255), 2)
        cv.line(image, tuple(landmark_point[18]), tuple(landmark_point[19]), (0,0,0), 6)
        cv.line(image, tuple(landmark_point[18]), tuple(landmark_point[19]), (255,255,255), 2)
        cv.line(image, tuple(landmark_point[19]), tuple(landmark_point[20]), (0,0,0), 6)
        cv.line(image, tuple(landmark_point[19]), tuple(landmark_point[20]), (255,255,255), 2)
        # Palm connections
        palm_pairs = [(0,1),(1,2),(2,5),(5,9),(9,13),(13,17),(17,0)]
        for start,end in palm_pairs:
            cv.line(image, tuple(landmark_point[start]), tuple(landmark_point[end]), (0,0,0),6)
            cv.line(image, tuple(landmark_point[start]), tuple(landmark_point[end]), (255,255,255),2)

    # วาดจุด landmark
    for idx, lm in enumerate(landmark_point):
        radius = 5 if idx != 4 and idx != 8 and idx != 12 and idx != 16 and idx != 20 else 8
        cv.circle(image, (lm[0], lm[1]), radius, (255,255,255), -1)
        cv.circle(image, (lm[0], lm[1]), radius, (0,0,0),1)

    return image

# วาดกรอบล้อมรอบมือ
def draw_bounding_rect(use_brect, image, brect):
    if use_brect:
        cv.rectangle(image, (brect[0],brect[1]), (brect[2],brect[3]), (0,0,0),1)
    return image

# วาดข้อความบนภาพ (มือซ้าย/ขวา + gesture)
def draw_info_text(image, brect, handedness, hand_sign_text):
    cv.rectangle(image, (brect[0], brect[1]), (brect[2], brect[1]-22), (0,0,0), -1)
    info_text = handedness.classification[0].label
    if hand_sign_text != "":
        info_text += ":" + hand_sign_text
    cv.putText(image, info_text, (brect[0]+5,brect[1]-4), cv.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255),1,cv.LINE_AA)
    return image

# วาดข้อมูล FPS และโหมดบนภาพ
def draw_info(image, fps, mode, number):
    cv.putText(image, f"FPS:{fps}", (10,30), cv.FONT_HERSHEY_SIMPLEX,1.0,(0,0,0),4,cv.LINE_AA)
    cv.putText(image, f"FPS:{fps}", (10,30), cv.FONT_HERSHEY_SIMPLEX,1.0,(255,255,255),2,cv.LINE_AA)

    mode_string = ["Logging Key Point","Capturing Landmarks From Provided Dataset Mode"]
    if 1 <= mode <= 2:
        cv.putText(image, f"MODE:{mode_string[mode-1]}", (10,90), cv.FONT_HERSHEY_SIMPLEX,0.6,(255,255,255),1,cv.LINE_AA)
        if 0 <= number <= 9:
            cv.putText(image, f"NUM:{number}", (10,110), cv.FONT_HERSHEY_SIMPLEX,0.6,(255,255,255),1,cv.LINE_AA)
    return image


