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
        .character {{
            position: absolute;
            bottom: 80px;
            right: 10px;
            width: 100px;
            z-index: 1;
        }}
        @media screen and (max-width: 600px) {{
            .character {{
                width: 80px;
                bottom: 100px;
            }}
            .stButton>button {{
                font-size: 20px;
                padding: 0.5em 1em;
            }}
            .quiz-box {{
                font-size: 48px;
            }}
        }}
        .choice-row {{
            display: flex;
            flex-direction: row;
            justify-content: center;
            align-items: center;
            flex-wrap: wrap;
            gap: 20px;
            margin-top: 20px;
        }}
        .choice-row .stButton>button {{
            font-size: 36px;
            padding: 1em 2em;
            min-width: 100px;
            background-color: #f28ab2;
            color: white;
            border-radius: 20px;
            border: none;
            box-shadow: 0px 4px 8px rgba(0,0,0,0.2);
        }}
        </style>
        """, unsafe_allow_html=True)

set_background("hiraganaApp_project/bg/background.png")

st.markdown("""
<div class='title-text'>🌟えまちゃんの かたかな あぷり🌟</div>
<img src='hiraganaApp_project/bg/character.png' class='character'>
""", unsafe_allow_html=True)

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
    path = os.path.join("hiraganaApp_project/sounds", file)
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

    st.markdown('<div class="choice-row">', unsafe_allow_html=True)
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
