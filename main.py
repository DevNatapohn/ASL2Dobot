import copy
import cv2 as cv
import mediapipe as mp
import csv

from utils.cvfpscalc import CvFpsCalc
from model.handpose_classifier.handpose_classifier import HandPoseClassifier

# import core modules
from core.args_parser import get_args
from core.mode_selector import select_mode
from core.hand_utils import calc_bounding_rect, calc_landmark_list
from core.preprocess import pre_process_landmark
from core.logger import logging_csv

from core.draw_utils import draw_bounding_rect, draw_landmarks, draw_info_text, draw_info
#from core.draw_style1 import draw_bounding_rect, draw_landmarks, draw_info_text, draw_info

from core.dataset_processor import process_dataset

def main():
    # get args
    args = get_args()
    cap_device = args.device
    cap_width = args.width
    cap_height = args.height
    use_static_image_mode = args.use_static_image_mode
    min_detection_confidence = args.min_detection_confidence
    min_tracking_confidence = args.min_tracking_confidence
    use_brect = True

    # camera setup
    cap = cv.VideoCapture(cap_device)
    cap.set(cv.CAP_PROP_FRAME_WIDTH, cap_width)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, cap_height)

    # mediapipe setup
    mp_hands = mp.solutions.hands # type: ignore
    hands = mp_hands.Hands(
        static_image_mode=use_static_image_mode,
        max_num_hands=2,
        min_detection_confidence=min_detection_confidence,
        min_tracking_confidence=min_tracking_confidence,
    )

    # classifier setup
    handpose_classifier = HandPoseClassifier()
    with open("model/handpose_classifier/handpose_labels.csv", encoding="utf-8-sig") as f:
        handpose_labels = [row[0] for row in csv.reader(f)]

    cvFpsCalc = CvFpsCalc(buffer_len=10)
    mode = 0

    while True:
        fps = cvFpsCalc.get()
        key = cv.waitKey(10)
        if key == 27:  # ESC
            break
        number, mode = select_mode(key, mode)

        ret, image = cap.read()
        if not ret:
            break
        image = cv.flip(image, 1)
        debug_image = copy.deepcopy(image)

        # mediapipe process
        image_rgb = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        image_rgb.flags.writeable = False
        results = hands.process(image_rgb)
        image_rgb.flags.writeable = True

        # dataset mode
        if mode == 2:
            process_dataset(hands, mode)
            break
        else:
            if results.multi_hand_landmarks is not None:
                for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                    brect = calc_bounding_rect(debug_image, hand_landmarks)
                    landmark_list = calc_landmark_list(debug_image, hand_landmarks)
                    pre_processed = pre_process_landmark(landmark_list)

                    logging_csv(number, mode, pre_processed)
                    hand_sign_id = handpose_classifier(pre_processed)

                    debug_image = draw_bounding_rect(use_brect, debug_image, brect)
                    debug_image = draw_landmarks(debug_image, landmark_list)
                    debug_image = draw_info_text(debug_image, brect, handedness, handpose_labels[hand_sign_id])

            debug_image = draw_info(debug_image, fps, mode, number)
            cv.imshow("Hand Gesture Recognition", debug_image)

    cap.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    main()
