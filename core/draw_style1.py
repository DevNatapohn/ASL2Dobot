# core/draw_utils_minimal.py
import cv2 as cv

def draw_landmarks(image, landmark_point):
    if len(landmark_point) > 0:
        color = (220, 220, 220)
        for start, end in [(2,3),(3,4),(5,6),(6,7),(7,8),(9,10),(10,11),(11,12),
                           (13,14),(14,15),(15,16),(17,18),(18,19),(19,20),
                           (0,1),(1,2),(2,5),(5,9),(9,13),(13,17),(17,0)]:
            cv.line(image, tuple(landmark_point[start]), tuple(landmark_point[end]), color, 2)

    for idx, lm in enumerate(landmark_point):
        radius = 4 if idx not in [4,8,12,16,20] else 6
        cv.circle(image, (lm[0], lm[1]), radius, (255,255,255), -1)
        cv.circle(image, (lm[0], lm[1]), radius, (180,180,180), 1)

    return image

def draw_bounding_rect(use_brect, image, brect):
    if use_brect:
        cv.rectangle(image, (brect[0],brect[1]), (brect[2],brect[3]), (200,200,200), 1)
    return image

def draw_info_text(image, brect, handedness, hand_sign_text):
    overlay = image.copy()
    cv.rectangle(overlay, (brect[0], brect[1]-26), (brect[2], brect[1]), (50,50,50), -1)
    image = cv.addWeighted(overlay, 0.6, image, 0.4, 0)

    info_text = handedness.classification[0].label
    if hand_sign_text != "":
        info_text += f" : {hand_sign_text}"

    cv.putText(image, info_text, (brect[0]+6, brect[1]-8),
               cv.FONT_HERSHEY_SIMPLEX, 0.55, (255,255,255), 1, cv.LINE_AA)
    return image

def draw_info(image, fps, mode, number):
    cv.putText(image, f"{fps:.0f} FPS", (10,30),
               cv.FONT_HERSHEY_SIMPLEX, 0.8, (240,240,240), 2, cv.LINE_AA)
    return image
