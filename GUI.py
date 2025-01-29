import streamlit as st
from streamlit_webrtc import webrtc_streamer,WebRtcMode
import AI_functionality
import cv2
import numpy as np
import random
st.set_page_config(page_title="إيماء" ,)
if "picture_taken" not in st.session_state:
    st.session_state["picture_taken"] = False
if "selected_letter" not in st.session_state:
    st.session_state["selected_letter"] = None
if "mode" not in st.session_state:
    st.session_state["mode"] = None
if "prediction" not in st.session_state:
    st.session_state["prediction"] = None
if "accuracy" not in st.session_state:
    st.session_state["accuracy"] = None
if "letter_active" not in st.session_state:
    st.session_state["letter_active"] = False
if "game_active" not in st.session_state:
    st.session_state["game_active"] = False
if "random_word" not in st.session_state:
    st.session_state["random_word"] = None
if "current_letter_index" not in st.session_state:
    st.session_state["current_letter_index"] = 0
if "letter_accuracies" not in st.session_state:
    st.session_state["letter_accuracies"] = []
if "play_again" not in st.session_state:
    st.session_state["play_again"] = False

st.markdown(
    """
    <style>
    .wave {
        animation-name: wave-animation;
        animation-duration: 2.5s;
        animation-iteration-count: infinite;
        transform-origin: 70% 70%;
        display: inline-block;
        font-size: 1em;
        vertical-align: middle;
    }
    @keyframes wave-animation {
        0% { transform: rotate( 0.0deg) }
        10% { transform: rotate(14.0deg) }
        20% { transform: rotate(-8.0deg) }
        30% { transform: rotate(14.0deg) }
        40% { transform: rotate(-4.0deg) }
        50% { transform: rotate(10.0deg) }
        60% { transform: rotate( 0.0deg) }
        100% { transform: rotate( 0.0deg) }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <h1 style="text-align: center; color: #4CAF50; font-family: Lemonada, Medium 500;">
    <span class="wave">👋🏻</span> إيماء
    </h1>
    <p style="text-align: center; color: #fbfcfa; font-family: Arial, sans-serif; font-size: 18px;">
        منصة لتعلم لغة الإشارة العربية
    </p>
    """,
    unsafe_allow_html=True,
)

st.markdown("<hr>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

with col1:
    learn_button = st.button("تعلم الحروف", use_container_width=True, key="learn")

with col2:
    test_button = st.button("اختبر نفسك", use_container_width=True, key="test")

if learn_button:
    st.session_state["mode"] = "تعلم الحروف"
if test_button:
    st.session_state["mode"] = "اختبر نفسك"

if st.session_state["mode"] == "تعلم الحروف":
    st.markdown(
        """
        <h3 style="text-align: center; color: #4CAF50; font-family: Arial, sans-serif;">
            اختر حرفًا لتتعلم لغة الإشارة
        </h3>
        """,
        unsafe_allow_html=True,
    )

    signs = {
        "Alef": "ا", "Beh": "ب", "Teh": "ت", "Theh": "ث", "Jeem": "ج",
        "Hah": "ح", "Khah": "خ", "Dal": "د", "Thal": "ذ", "Reh": "ر",
        "Zain": "ز", "Seen": "س", "Sheen": "ش", "Sad": "ص", "Dad": "ض",
        "Tah": "ط", "Zah": "ظ", "Ain": "ع", "Ghain": "غ", "Feh": "ف",
        "Qaf": "ق", "Kaf": "ك", "Lam": "ل", "Meem": "م", "Noon": "ن",
        "Heh": "ه", "Waw": "و", "Yeh": "ي", "Laa": "لا", "Al": "ال",
        "Teh_Marbuta": "ة"
    }

    letters = list(signs.values())

    letters_with_default = ["اختر حرفًا"] + letters

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        letter_choice = st.selectbox(
            "اختر حرفًا",
            letters_with_default,
            index=0,
            help="اختر أي حرف لتظهر لك صورته في لغة الإشارة."
        )

    st.session_state["selected_letter"] = letter_choice

    if st.session_state["selected_letter"] and st.session_state["selected_letter"] != "اختر حرفًا":
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(
                f"/Users/nawaf/PycharmProjects/sdaia_Asign_language/a_letters/{letter_choice}.png",
                use_container_width=False,
                width=380,
            )

if st.session_state["mode"] == "اختبر نفسك":
    st.markdown(
        """
        <h3 style="text-align: center; color: #4CAF50; font-family: Arial, sans-serif;">
            اختبر معرفتك بلغة الإشارة
        </h3>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        letter_button = st.button("اختبر نفسك بالحروف")
    with col3:
        words_button = st.button("اختبر نفسك بتركيب الحروف")

    if letter_button:
        st.session_state["letter_active"] = True

    if st.session_state["letter_active"]:
        letters = {
            "Alef": "ا", "Beh": "ب", "Teh": "ت", "Theh": "ث", "Jeem": "ج",
            "Hah": "ح", "Khah": "خ", "Dal": "د", "Thal": "ذ", "Reh": "ر",
            "Zain": "ز", "Seen": "س", "Sheen": "ش", "Sad": "ص", "Dad": "ض",
            "Tah": "ط", "Zah": "ظ", "Ain": "ع", "Ghain": "غ", "Feh": "ف",
            "Qaf": "ق", "Kaf": "ك", "Lam": "ل", "Meem": "م", "Noon": "ن",
            "Heh": "ه", "Waw": "و", "Yeh": "ي", "Laa": "لا", "Al": "ال",
            "Teh_Marbuta": "ة"
        }
        signs_with_default = ["اختر حرفًا"] + list(letters.values())

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            letter = st.selectbox("اختر حرفًا للاختبار", signs_with_default, index=0)

        if letter != "اختر حرفًا":
            st.markdown(
                f"<p style='text-align: center;'>قم بعمل إشارة الحرف <strong>{letter}</strong> أمام الكاميرا</p>",
                unsafe_allow_html=True,
            )
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                pic = st.camera_input("التقط صورة لك وأنت تؤدي الإشارة.")

            if pic:
                with st.spinner("جاري المعالجة..."):
                    img_bytes = pic.getvalue()
                    img = cv2.imdecode(np.frombuffer(img_bytes, np.uint8), cv2.IMREAD_COLOR)
                    prediction = AI_functionality.predict_sign(img, letter)

                    if prediction[1] != 0:
                        st.success(f"Predicted sign:  {prediction[0]}, Confidence: {prediction[1]}%")
                    else:
                        st.error(f"Predicted sign: {prediction[0]}, Confidence: {prediction[1]}%")

    if words_button:
        st.session_state["game_active"] = True
    if st.session_state["game_active"]:
        if st.session_state.get("random_word") == None:
            words = ["محمد", "خروف", "فهد", "حصان", "نواف", "شهر", "يوم", "سيارة", "كرسي",
                     "اكل", "مويه", "مدينة", "قهوة", "نورة", "ملك"]
            st.session_state["random_word"] = random.choice(words)
            st.session_state["current_letter_index"] = 0
            st.session_state["letter_accuracies"] = []

        word = st.session_state["random_word"]
        letters = list(word)
        current_index = st.session_state["current_letter_index"]
        with col2:
            st.write(f"كلمتك هي:{word}")

        if current_index < len(letters):
            current_letter = letters[current_index]
            st.markdown(
                f"<p style='text-align: center; font-size: 24px;'>قم بعمل إشارة الحرف: <strong>{current_letter}</strong></p>",
                unsafe_allow_html=True
            )

            pic = st.camera_input("التقط صورة للحرف", key="single_camera")

            if pic:
                with st.spinner("جاري المعالجة..."):
                    img_bytes = pic.getvalue()
                    img = cv2.imdecode(np.frombuffer(img_bytes, np.uint8), cv2.IMREAD_COLOR)


                    prediction = AI_functionality.predict_sign(img, current_letter)

                    if prediction[1] != 0:
                        st.success(f"تم التعرف على الحرف {current_letter} بدقة {prediction[1]}%")
                        st.session_state["letter_accuracies"].append(prediction[1])
                        st.session_state["current_letter_index"] += 1
                    else:
                        st.error(f"لم يتم التعرف على الحرف {current_letter}، حاول مرة أخرى.")


                if st.session_state["current_letter_index"] >= len(letters):
                    final_accuracy = (
                            sum(st.session_state["letter_accuracies"]) /
                            len(st.session_state["letter_accuracies"])
                    ) if st.session_state["letter_accuracies"] else 0

                    st.markdown(
                        f"<h3 style='text-align: center;'>لقد أكملت الكلمة <strong>{word}</strong> بدقة إجمالية: <span style='color: green;'>{final_accuracy:.2f}%</span></h3>",
                        unsafe_allow_html=True
                    )
                    st.session_state["random_word"] = None
                    st.session_state["current_letter_index"] = 0
                    st.session_state["letter_accuracies"] = []
                    st.session_state["game_active"] = False