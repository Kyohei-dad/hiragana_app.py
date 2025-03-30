import streamlit as st
import random
import os
import base64

# 背景画像の設定
def set_background(image_path):
    with open(image_path, "rb") as f:
        data = f.read()
        encoded = base64.b64encode(data).decode()
        st.markdown(f"""
        <style>
        body {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            overflow-x: hidden;
            font-family: 'Comic Sans MS', 'Rounded Mplus 1c', sans-serif;
        }}

        .title-text {{
            text-align: center;
            font-size: 40px;
            font-weight: bold;
            color: white;
            text-shadow: 2px 2px 4px #ff69b4;
            margin-top: 20px;
        }}

        .character-img {{
            position: fixed;
            bottom: 10px;
            right: 10px;
            width: 120px;
            z-index: 1000;
        }}

        .quiz-box {{
            background-color: rgba(255, 255, 255, 0.9);
            padding: 1em 2em;
            margin: 20px auto;
            text-align: center;
            font-size: 96px;
            font-weight: bold;
            border-radius: 30px;
            width: fit-content;
            box-shadow: 0 8px 20px rgba(0,0,0,0.3);
            color: #222;
        }}

        .choices-container {{
            display: flex;
            flex-direction: row;
            justify-content: center;
            align-items: center;
            gap: 30px;
            flex-wrap: wrap;
            margin-top: 30px;
        }}

        .choice-button {{
            font-size: 56px;
            padding: 1em 2em;
            min-width: 140px;
            background-color: #f28ab2;
            color: white;
            border-radius: 30px;
            border: none;
            box-shadow: 0px 6px 12px rgba(0,0,0,0.3);
            transition: all 0.3s ease;
            cursor: pointer;
        }}

        .choice-button:hover {{
            transform: scale(1.1);
            background-color: #ff9ac2;
        }}

        .star-pop {{
            position: fixed;
            top: 50%;
            left: 50%;
            font-size: 80px;
            animation: pop-star 1s ease-in-out forwards;
            z-index: 9999;
        }}

        @keyframes pop-star {{
            0% {{ transform: scale(0.2) translateY(20px); opacity: 0; }}
            50% {{ transform: scale(1.5) translateY(-10px); opacity: 1; }}
            100% {{ transform: scale(1) translateY(-40px); opacity: 0; }}
        }}
        </style>
        """, unsafe_allow_html=True)

# キャラクター画像読み込み
def load_character_image(image_path):
    with open(image_path, "rb") as f:
        data = f.read()
        encoded = base64.b64encode(data).decode()
        return f'<img src="data:image/png;base64,{encoded}" class="character-img">'

# 音を再生
def play_sound(file):
    path = os.path.join("sounds", file)
    if os.path.exists(path):
        st.audio(path, format="audio/mp3", start_time=0)

# スタート
set_background("bg/background.png")
st.markdown("<div class='title-text'>🌟えまちゃんの かたかな あぷり🌟</div>", unsafe_allow_html=True)
st.markdown(load_character_image("bg/character.png"), unsafe_allow_html=True)

kana_pairs = [
    ("あ", "ア"), ("い", "イ"), ("う", "ウ"), ("え", "エ"), ("お", "オ"),
    ("が", "ガ"), ("ぎ", "ギ"), ("ぐ", "グ"), ("げ", "ゲ"), ("ご", "ゴ"),
    ("さ", "サ"), ("し", "シ"), ("す", "ス"), ("せ", "セ"), ("そ", "ソ"),
    ("た", "タ"), ("ち", "チ"), ("つ", "ツ"), ("て", "テ"), ("と", "ト"),
    ("ぱ", "パ"), ("ぴ", "ピ"), ("ぷ", "プ"), ("ぺ", "ペ"), ("ぽ", "ポ"),
    ("ん", "ン")
]

if 'score_history' not in st.session_state:
    st.session_state.score_history = []
if 'questions' not in st.session_state:
    st.session_state.questions = []
if 'current_index' not in st.session_state:
    st.session_state.current_index = 0
if 'correct_count' not in st.session_state:
    st.session_state.correct_count = 0
if 'current_question' not in st.session_state:
    st.session_state.current_question = None
if 'clicked' not in st.session_state:
    st.session_state.clicked = None

if not st.session_state.questions:
    st.write("### 今までのスコア")
    if st.session_state.score_history:
        for i, s in enumerate(st.session_state.score_history):
            st.write(f"{i+1}回目: {s}/10")
    else:
        st.write("(まだ記録なし)")

    if st.button("💡 クイズスタート！"):
        st.session_state.questions = random.sample(kana_pairs, 10)
        st.session_state.current_index = 0
        st.session_state.correct_count = 0
        st.session_state.current_question = st.session_state.questions[0]
        st.session_state.clicked = None
        st.rerun()

else:
    hira, correct = st.session_state.current_question
    st.markdown(f"<div class='quiz-box'>{hira}</div>", unsafe_allow_html=True)

    wrong_choices = random.sample([k for _, k in kana_pairs if k != correct], 2)
    choices = wrong_choices + [correct]
    random.shuffle(choices)

    st.markdown('<div class="choices-container">', unsafe_allow_html=True)
    for choice in choices:
        if st.button(choice):
            st.session_state.clicked = choice
    st.markdown('</div>', unsafe_allow_html=True)

    clicked = st.session_state.clicked
    if clicked:
        if clicked == correct:
            st.markdown("<div class='star-pop'>⭐</div>", unsafe_allow_html=True)
            play_sound("correct.mp3")
            st.session_state.correct_count += 1
            st.session_state.current_index += 1
            if st.session_state.current_index < 10:
                st.session_state.current_question = st.session_state.questions[st.session_state.current_index]
                st.session_state.clicked = None
            else:
                st.session_state.score_history.append(st.session_state.correct_count)
                st.session_state.questions = []
                st.session_state.clicked = None
            st.rerun()
        else:
            st.error("❌ ブブー！ もう一度！")
            play_sound("wrong.mp3")
            st.session_state.clicked = None
