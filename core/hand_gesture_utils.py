# hand_gesture_utils.py
def get_correct_fingers_for_gesture(hand_sign_id: int):
    """
    กำหนดนิ้วที่ถูกตาม gesture
    ตัวอย่าง mapping:
    0 = 'A', 1 = 'B', 2 = 'C', ...
    0=Thumb, 1=Index, 2=Middle, 3=Ring, 4=Pinky
    """
    mapping = {
        0: [0],        # 'A' → นิ้วโป้งถูก
        1: [1,2,3,4],  # 'B' → 4 นิ้วถูก
        2: [1,2],      # 'C' → นิ้วชี้+กลาง
        3: [0,1,2,3,4],# 'D' → ทุกนิ้วถูก
        # เพิ่ม mapping ตาม label จริงทั้งหมด
    }
    return mapping.get(hand_sign_id, [])  # default ไม่มีนิ้วถูก
