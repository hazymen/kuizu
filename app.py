from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

# クイズデータ
QUIZ_DATA = [
    {
        "id": 1,
        "question": "波源が1秒間に50回振動し、速さ 20 m/s で伝わる波があります。この波の波長は何mですか？",
        "background": "波の基本式",
        "options": [
            {"text": "0.40 m", "is_correct": True},
            {"text": "2.5 m", "is_correct": False},
            {"text": "1000 m", "is_correct": False},
            {"text": "0.025 m", "is_correct": False}
        ],
        "explanation": "波の基本式 $v = f\\lambda$ より、$\\lambda = v / f$ を計算します。$\\lambda = 20 / 50 = 0.40$ [m] となります。"
    },
    {
        "id": 2,
        "question": "媒質の振動方向が、波の進行方向に対して「垂直」である波を何と呼びますか？",
        "background": "横波と縦波",
        "options": [
            {"text": "縦波（疎密波）", "is_correct": False},
            {"text": "横波", "is_correct": True},
            {"text": "定常波", "is_correct": False},
            {"text": "衝撃波", "is_correct": False}
        ],
        "explanation": "振動と進行が垂直なのが「横波」、平行なのが「縦波（疎密波）」です。光や弦の振動は横波の代表例です。"
    },
    {
        "id": 3,
        "question": "波が平面の壁で反射するとき、入射角が 30° であった場合、反射角は何度になりますか？",
        "background": "反射の法則",
        "options": [
            {"text": "0°", "is_correct": False},
            {"text": "30°", "is_correct": True},
            {"text": "60°", "is_correct": False},
            {"text": "90°", "is_correct": False}
        ],
        "explanation": "反射の法則により、入射角と反射角は常に等しくなります。"
    },
    {
        "id": 4,
        "question": "波が異なる媒質に進むとき、波の速さが「遅くなる」方へ進むと、波長はどう変化しますか？",
        "background": "波の屈折",
        "options": [
            {"text": "長くなる", "is_correct": False},
            {"text": "変わらない", "is_correct": False},
            {"text": "短くなる", "is_correct": True},
            {"text": "ゼロになる", "is_correct": False}
        ],
        "explanation": "屈折しても「周波数 $f$」は変わりません。$v = f\\lambda$ より、速さ $v$ が小さくなれば、波長 $\\lambda$ も短くなります。"
    },
    {
        "id": 5,
        "question": "同じ振幅 0.1m の2つの波が重なり合ったとき、山と山が重なる点での合成波の振幅は最大で何mになりますか？",
        "background": "波の干渉（重ね合わせ）",
        "options": [
            {"text": "0.05 m", "is_correct": False},
            {"text": "0.1 m", "is_correct": False},
            {"text": "0.2 m", "is_correct": True},
            {"text": "0.4 m", "is_correct": False}
        ],
        "explanation": "重ね合わせの原理により、山と山が重なると振幅は和になります。$0.1 + 0.1 = 0.2$ [m] です。"
    }
]

@app.route('/')
def index():
    """クイズ一覧ページ"""
    return render_template('index.html', quiz_count=len(QUIZ_DATA))

@app.route('/quiz/<int:quiz_id>')
def quiz(quiz_id):
    """クイズ表示ページ"""
    # クイズIDは1から始まるため、0ベースのインデックスに変換
    if quiz_id < 1 or quiz_id > len(QUIZ_DATA):
        return redirect(url_for('index'))
    
    quiz_data = QUIZ_DATA[quiz_id - 1]
    progress_width = int((quiz_id / len(QUIZ_DATA)) * 100)
    return render_template('quiz.html', quiz=quiz_data, quiz_number=quiz_id, total_quizzes=len(QUIZ_DATA), progress_width=progress_width)

@app.route('/result', methods=['POST'])
def result():
    """結果ページ"""
    quiz_id = int(request.form.get('quiz_id'))
    selected_index = int(request.form.get('selected'))
    
    if quiz_id < 1 or quiz_id > len(QUIZ_DATA):
        return redirect(url_for('index'))
    
    quiz_data = QUIZ_DATA[quiz_id - 1]
    selected_option = quiz_data['options'][selected_index]
    is_correct = selected_option['is_correct']
    correct_index = next(i for i, opt in enumerate(quiz_data['options']) if opt['is_correct'])
    
    # スコア計算（セッションで管理）
    return render_template('result.html', 
                         quiz=quiz_data,
                         quiz_number=quiz_id,
                         total_quizzes=len(QUIZ_DATA),
                         is_correct=is_correct,
                         selected_option=selected_option,
                         correct_index=correct_index,
                         selected_index=selected_index)

if __name__ == '__main__':
    # LAN内からのアクセスを許可（0.0.0.0でバインド）
    app.run(host='0.0.0.0', port=5000, debug=True)
