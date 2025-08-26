# core/draw_utils_neon.py
import cv2 as cv

def draw_landmarks(image, landmark_point):
    if len(landmark_point) > 0:
        neon_outer = (120, 0, 255)   # ม่วงนีออน
        neon_inner = (0, 255, 255)   # ฟ้านีออน
        for start, end in [(2,3),(3,4),(5,6),(6,7),(7,8),(9,10),(10,11),(11,12),
                           (13,14),(14,15),(15,16),(17,18),(18,19),(19,20),
                           (0,1),(1,2),(2,5),(5,9),(9,13),(13,17),(17,0)]:
            cv.line(image, tuple(landmark_point[start]), tuple(landmark_point[end]), neon_outer, 6)
            cv.line(image, tuple(landmark_point[start]), tuple(landmark_point[end]), neon_inner, 2)

    for idx, lm in enumerate(landmark_point):
        radius = 6 if idx in [4,8,12,16,20] else 4
        cv.circle(image, (lm[0], lm[1]), radius+2, (120,0,255), -1) # outer glow
        cv.circle(image, (lm[0], lm[1]), radius, (0,255,255), -1)   # inner glow

    return image

def draw_bounding_rect(use_brect, image, brect):
    if use_brect:
        cv.rectangle(image, (brect[0],brect[1]), (brect[2],brect[3]), (0,255,255), 2)
    return image

def draw_info_text(image, brect, handedness, hand_sign_text):
    cv.rectangle(image, (brect[0], brect[1]-26), (brect[2], brect[1]), (120,0,255), -1)
    info_text = handedness.classification[0].label
    if hand_sign_text != "":
        info_text += f" : {hand_sign_text}"
    cv.putText(image, info_text, (brect[0]+6, brect[1]-8),
               cv.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,255), 2, cv.LINE_AA)
    return image

def draw_info(image, fps, mode, number):
    cv.putText(image, f"{fps:.0f} FPS", (10,30),
               cv.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,255), 2, cv.LINE_AA)
    return image
