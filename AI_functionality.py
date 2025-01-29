import cv2
import mediapipe as mp
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from streamlit_webrtc import WebRtcMode,webrtc_streamer




model = joblib.load('sign_language_model.pkl')

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1)

sign_names = {
    "Ain": "ع", "Al": "ال", "Alef": "ا", "Beh": "ب", "Dad": "ض",
    "Dal": "د", "Feh": "ف", "Ghain": "غ", "Hah": "ح", "Heh": "ه",
    "Jeem": "ج", "Kaf": "ك", "Khah": "خ", "Laa": "لا", "Lam": "ل",
    "Meem": "م", "Noon": "ن", "Qaf": "ق", "Reh": "ر", "Sad": "ص",
    "Seen": "س", "Sheen": "ش", "Tah": "ط", "Teh": "ت", "Teh_Marbuta": "ة",
    "Thal": "ذ", "Theh": "ث", "Waw": "و", "Yeh": "ي", "Zah": "ظ", "Zain": "ز"
}



def predict_sign(image, letter) -> tuple[str, float]:
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)
    if not results.multi_hand_landmarks:
        return "Unknown", 0

    hand_landmarks = results.multi_hand_landmarks[0]

    landmarks = [lm.x for lm in hand_landmarks.landmark] + [lm.y for lm in hand_landmarks.landmark]
    landmarks = np.array(landmarks).reshape(1, -1)
    prediction = model.predict(landmarks)
    confidence_list = model.predict_proba(landmarks)[0]

    counter = 0
    for classs in sign_names.keys():
        if classs == prediction:
            break
        counter += 1
    if letter == sign_names.get(prediction[0],prediction[0]):
        return sign_names.get(prediction[0], prediction[0]), confidence_list[counter]*100
    else:
        return "Fault sign", 0
