import streamlit as st
import random
import os
import base64

# 背景画像を表示する関数
def set_background(image_path):
    with open(image_path, "rb") as f:
        data = f.read()
        encoded = base64.b64encode(data).decode()
      st.markdown("""
<style>
.character {
    position: absolute;
    bottom: 80px;  /* ← ここでキャラの位置を上にずらす */
    right: 10px;
    width: 100px;
    z-index: 1;
}
@media screen and (max-width: 600px) {
    .character {
        width: 80px;
        bottom: 100px;
    }
    .stButton>button {
        font-size: 20px;
        padding: 0.5em 1em;
    }
    .quiz-box {
        font-size: 48px;
    }
}
</style>
""", unsafe_allow_html=True)


# キャラクター画像を表示する関数
def show_character(image_path):
    with open(image_path, "rb") as f:
        data = f.read()
        encoded = base64.b64encode(data).decode()
        st.markdown(f"""
        <img src="data:image/png;base64,{encoded}" class="character">
        """, unsafe_allow_html=True)

set_background("hiraganaApp_project/bg/background.png")
show_character("hiraganaApp_project/bg/character.png")

# カスタムCSS（見やすさとサイズ強化）
st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: "Rounded Mplus 1c", "Comic Sans MS", cursive, sans-serif;
    color: #333;
}
.stButton>button {
    background-color: #f28ab2;
    color: white;
    font-size: 48px;
    border-radius: 20px;
    border: none;
    padding: 1em 2em;
    margin: 1em;
    box-shadow: 0px 6px 12px rgba(0,0,0,0.2);
    transition: transform 0.2s ease-in-out;
}
.stButton>button:hover {
    transform: scale(1.07);
    background-color: #f15ca4;
}
.quiz-box {
    background-color: #fff8fb;
    padding: 30px;
    border-radius: 30px;
    margin: 20px 0;
    box-shadow: 0 0 20px rgba(0,0,0,0.1);
    text-align: center;
    font-size: 80px;
    color: #cc0066;
    font-weight: bold;
}
.title-text {
    font-size: 48px;
    text-align: center;
    color: #d63384;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='title-text'>🌟えまちゃんの かたかな あぷり🌟</div>", unsafe_allow_html=True)

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

    colA, colB, colC = st.columns(3)
    for i, col in enumerate([colA, colB, colC]):
        if col.button(choices[i]):
            if choices[i] == correct:
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
