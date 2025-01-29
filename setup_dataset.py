import cv2
import mediapipe as mp
import os
import numpy as np
import pandas as pd

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=True, max_num_hands=1)
mp_drawing = mp.solutions.drawing_utils

def process_dataset(dataset_path):
    data = []
    labels = []
    skipped_files = []  

    for label in os.listdir(dataset_path):
        folder_path = os.path.join(dataset_path, label)
        for image_file in os.listdir(folder_path):
            image_path = os.path.join(folder_path, image_file)
            try:
                image = cv2.imread(image_path)
                if image is None:
                    raise ValueError("Image is None")
                image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                results = hands.process(image_rgb)

                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        landmarks = [
                            lm.x for lm in hand_landmarks.landmark
                        ] + [
                            lm.y for lm in hand_landmarks.landmark
                        ]
                        data.append(landmarks)
                        labels.append(label)
            except Exception as e:
                skipped_files.append(image_path)
                print(f"Skipped file {image_path}: {e}")
    print(f"Skipped {len(skipped_files)} files.")
    return np.array(data), np.array(labels)

dataset_path = "dataset path"  #put your dataset path here
X, y = process_dataset(dataset_path)

df = pd.DataFrame(X)
df['label'] = y
df.to_csv('features_labels.csv', index=False)
print("Data saved to features_labels.csv")
