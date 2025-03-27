import streamlit as st
import random
import os
import base64

# 背景画像を表示する関数
def set_background(image_path):
    with open(image_path, "rb") as f:
        data = f.read()
        encoded = base64.b64encode(data).decode()
        st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-position: center;
        }}
        .character-img {{
            position: fixed;
            bottom: 10px;
            right: 10px;
            width: 100px;
            z-index: 1000;
        }}
        .quiz-box {{
            background-color: rgba(255, 255, 255, 0.85);
            padding: 1em 2em;
            margin: 20px auto;
            text-align: center;
            font-size: 96px;
            font-weight: bold;
            border-radius: 20px;
            width: fit-content;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            color: #000;
        }}
        .choices-container {{
            display: flex;
            flex-direction: row;
            justify-content: center;
            align-items: center;
            gap: 20px;
            flex-wrap: wrap;
            margin-top: 20px;
        }}
        .choices-container .stButton>button {{
            font-size: 48px;
            padding: 1em 2em;
            min-width: 120px;
            background-color: #f28ab2;
            color: white;
            border-radius: 20px;
            border: none;
            box-shadow: 0px 4px 8px rgba(0,0,0,0.2);
        }}
        @media screen and (max-width: 600px) {{
            .character-img {{
                width: 80px;
                bottom: 10px;
                right: 10px;
            }}
            .quiz-box {{
                font-size: 72px;
            }}
            .choices-container {{
                flex-direction: row;
                flex-wrap: wrap;
                justify-content: center;
            }}
            .choices-container .stButton>button {{
                font-size: 42px;
                min-width: 100px;
            }}
        }}
        </style>
        """, unsafe_allow_html=True)

set_background("bg/background.png")

# キャラクター画像をbase64で表示
def load_character_image(image_path):
    with open(image_path, "rb") as f:
        data = f.read()
        encoded = base64.b64encode(data).decode()
        return f'<img src="data:image/png;base64,{encoded}" class="character-img">'

st.markdown("""
<div class='title-text'>🌟えまちゃんの かたかな あぷり🌟</div>
""", unsafe_allow_html=True)

st.markdown(load_character_image("bg/character.png"), unsafe_allow_html=True)

kana_pairs = [
    ("あ", "ア"), ("い", "イ"), ("う", "ウ"), ("え", "エ"), ("お", "オ"),
    ("か", "カ"), ("き", "キ"), ("く", "ク"), ("け", "ケ"), ("こ", "コ"),
    ("さ", "サ"), ("し", "シ"), ("す", "ス"), ("せ", "セ"), ("そ", "ソ"),
    ("た", "タ"), ("ち", "チ"), ("つ", "ツ"), ("て", "テ"), ("と", "ト"),
    ("な", "ナ"), ("に", "ニ"), ("ぬ", "ヌ"), ("ね", "ネ"), ("の", "ノ"),
    ("は", "ハ"), ("ひ", "ヒ"), ("ふ", "フ"), ("へ", "ヘ"), ("ほ", "ホ"),
    ("ま", "マ"), ("み", "ミ"), ("む", "ム"), ("め", "メ"), ("も", "モ"),
    ("や", "ヤ"), ("ゆ", "ユ"), ("よ", "ヨ"),
    ("ら", "ラ"), ("り", "リ"), ("る", "ル"), ("れ", "レ"), ("ろ", "ロ"),
    ("わ", "ワ"), ("を", "ヲ"), ("ん", "ン")
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

def play_sound(file):
    path = os.path.join("sounds", file)
    if os.path.exists(path):
        with open(path, "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            st.markdown(f"""
                <audio autoplay>
                    <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                </audio>
            """, unsafe_allow_html=True)

if not st.session_state.questions:
    col1, col2 = st.columns([1, 2])
    with col1:
        st.write("### 今までのスコア")
        if st.session_state.score_history:
            for i, s in enumerate(st.session_state.score_history):
                st.write(f"{i+1}回目: {s}/10")
        else:
            st.write("(まだ記録なし)")

    with col2:
        if st.button("💡 クイズスタート！"):
            st.session_state.questions = random.sample(kana_pairs, 10)
            st.session_state.current_index = 0
            st.session_state.correct_count = 0
            st.session_state.current_question = st.session_state.questions[0]
            st.rerun()

else:
    hira, correct = st.session_state.current_question
    st.markdown(f"<div class='quiz-box'>{hira}</div>", unsafe_allow_html=True)

    wrong_choices = random.sample([k for _, k in kana_pairs if k != correct], 2)
    choices = wrong_choices + [correct]
    random.shuffle(choices)

    st.markdown('<div class="choices-container">', unsafe_allow_html=True)
    for choice in choices:
        if st.button(choice, key=choice):
            if choice == correct:
                st.success("⭕ ピンポン！")
                play_sound("correct.mp3")
                st.session_state.correct_count += 1
                st.session_state.current_index += 1
                if st.session_state.current_index < 10:
                    st.session_state.current_question = st.session_state.questions[st.session_state.current_index]
                else:
                    st.session_state.score_history.append(st.session_state.correct_count)
                    st.session_state.questions = []
                st.rerun()
            else:
                st.error("❌ ブブー！ もう一度！")
                play_sound("wrong.mp3")
    st.markdown('</div>', unsafe_allow_html=True)
