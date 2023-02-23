import os
import random
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

# LINE Messaging APIの設定
line_bot_api = LineBotApi(process.env.CHANNEL_SECRET)
handler = WebhookHandler(process.env.CHANNEL_ACCESS_TOKEN)

# 数式の問題を生成する関数
def generate_algebra_problems():
    # 問題の種類をランダムに選択
    types = ['simplify', 'expand', 'factor']
    problem_type = random.choice(types)

    # 数式をランダムに生成
    x = random.choice(['x', 'y', 'z'])
    a = random.randint(-10, 10)
    b = random.randint(-10, 10)
    c = random.randint(-10, 10)
    d = random.randint(-10, 10)
    e = random.randint(-10, 10)
    if problem_type == 'simplify':
        problem = f"Simplify the expression: {a}({x} + {b}) - {c}({x} - {d})"
        answer = str(a+b-c+d) + x + "+" + str(a*d-b*c)
    elif problem_type == 'expand':
        problem = f"Expand the expression: ({a}{x} + {b})({c}{x} - {d})"
        answer = str(a*c) + x + "^2 + " + str((a*d-b*c)) + x + " - " + str(b*d)
    else:
        problem = f"Factor the expression: {a}{x}^2 + {b}{x} + {c}"
        discriminant = b**2 - 4*a*c
        if discriminant < 0:
            answer = "Not factorable over real numbers"
        elif discriminant == 0:
            answer = str(-b/(2*a))
        else:
            answer = f"({-b} + sqrt({discriminant}))/{2*a} or ({-b} - sqrt({discriminant}))/{2*a}"

    return [problem, answer]

# 連立方程式の問題を生成する関数
def generate_equations_problems():
    # 問題の種類をランダムに選択
    types = ['two', 'three']
    problem_type = random.choice(types)

    # 連立方程式をランダムに生成
    x = random.choice(['x', 'y', 'z'])
    if problem_type == 'two':
        a11 = random.randint(-10, 10)
        a12 = random.randint(-10, 10)
        a21 = random.randint(-10, 10)
        a22 = random.randint(-10, 10)
        b1 = random.randint(-10, 10)
        b2 = random.randint(-10, 10)
        problem = f"Solve the system of equations:\n{a11}{x} + {a12}y = {b1}\n{a21}{x} + {a22}y = {b2}"
        det = a11*a22 - a12*a21
        if det == 0:
            answer = "No solution"
        else:
            x = (b1*a22 - b2*a12)/det
            y = (a11*b2 - a21*b1)/det
            answer = f"x = {x}, y = {y}"
    else:
        a11 = random.randint(-10, 10)
        a12 = random.randint(-10, 10)
        a13 = random.randint(-10, 10)
        a21 = random.randint(-10, 10)
        a22 = random.randint(-10, 10)
        a23 = random.randint(-10, 10)
        a31 = random.randint(-10, 10)
        a32 = random.randint(-10, 10)
        a33 = random.randint(-10, 10)
        b1 = random.randint(-10, 10)
        b2 = random.randint(-10, 10)
        b3 = random.randint(-10, 10)
        problem = f"Solve the system of equations:\n{a11}{x} + {a12}y + {a13}z = {b1}\n{a21}{x} + {a22}y + {a23}z = {b2}\n{a31}{x} + {a32}y + {a33}z = {b3}"
        det = a11*a22*a33 + a12*a23*a31 + a13*a21*a32 - a31*a22*a13 - a32*a23*a11 - a33*a21*a12
        if det == 0:
            answer = "No solution"
        else:
            x = (b1*a22*a33 + b2*a23*a31 + b3*a21*a32 - a31*a22*b3 - a32*a23*b1 - a33*a21*b2)/det
            y = (a11*b2*a33 + a12*b3*a31 + a13*b1*a32 - a31*b2*a13 - a32*b3*a11 - a33*b1*a12)/det
            z = (a11*a22*b3 + a12*a23*b1 + a13*a21*b2 - b1*a22*a13 - b2*a23*a11 - b3*a21*a12)/det
            answer = f"x = {x}, y = {y}, z = {z}"

    return [problem, answer]

def generate_probability_problems():
    # 問題の種類をランダムに選択
    types = ['coin', 'dice']
    problem_type = random.choice(types)
    # 確率の問題をランダムに生成
    if problem_type == 'coin':
        flips = random.randint(1, 10)
        heads = random.randint(0, flips)
        problem = f"If a fair coin is flipped {flips} times, what is the probability of getting {heads} heads?"
        p = 2**(-flips) * (factorial(flips) / (factorial(heads) * factorial(flips - heads)))
        answer = f"{p:.4f}"
    else:
        rolls = random.randint(1, 5)
        sides = random.randint(4, 20)
        rolls_text = "roll" if rolls == 1 else "rolls"
        sides_text = "side" if sides == 1 else "sides"
        problem = f"If a fair {rolls}-sided die is rolled {rolls} times, what is the probability that the sum of the rolls is equal to {rolls * sides//2}?"
        p = count_ways_to_get_sum(rolls, sides, rolls * sides//2) / sides**rolls
        answer = f"{p:.4f}"

    return [problem, answer]

def generate_data_problems():
    # 問題の種類をランダムに選択
    types = ['mean', 'median', 'mode', 'range']
    problem_type = random.choice(types)
    # データの活用の問題をランダムに生成
    if problem_type == 'mean':
        n = random.randint(5, 10)
        data = [random.randint(0, 100) for i in range(n)]
        mean = sum(data) / n
        problem = f"What is the mean of the following data set: {data}?"
        answer = f"{mean:.2f}"
    elif problem_type == 'median':
        n = random.randint(5, 10)
        data = sorted([random.randint(0, 100) for i in range(n)])
        median = data[n//2] if n % 2 == 1 else (data[n//2-1] + data[n//2]) / 2
        problem = f"What is the median of the following data set: {data}?"
        answer = f"{median:.2f}"
    elif problem_type == 'mode':
        n = random.randint(5, 10)
        data = [random.randint(0, 100) for i in range(n)]
        modes = []
        mode_count = 0
        for value in set(data):
            count = data.count(value)
            if count > mode_count:
                modes = [value]
                mode_count = count
            elif count == mode_count:
                modes.append(value)
        if len(modes) == 1:
            mode = modes[0]
            problem = f"What is the mode of the following data set: {data}?"
            answer = str(mode)
        else:
            problem = f"What are the modes of the following data set: {data}?"
            answer = ", ".join([str(mode) for mode in modes])
    else:
        n = random.randint(5, 10)
        data = [random.randint(0, 100) for i in range(n)]
        data_range = max(data) - min(data)
        problem = f"What is the range of the following data set: {data}?"
        answer = str(data_range)
    return [problem, answer]

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # ユーザーが送信したメッセージを取得
    message = event.message.text
    # 数式の問題を生成する場合
    if message == "文字式":
        problem, answer = generate_expression_problems()
    # 連立方程式の問題を生成する場合
    elif message == "連立方程式":
        problem, answer = generate_system_of_equations_problems()
    # 確率の問題を
    elif message == "確率":
        problem, answer = generate_probability_problems()
# データの活用の問題を生成する場合
    elif message == "データの活用":
        problem, answer = generate_data_problems()
    # サポートする単元以外の場合
    else:
        problem = "申し訳ありませんが、その単元には対応していません。"
        answer = ""

    # 問題と解答をLINEで返信する
    line_bot_api.reply_message(
        event.reply_token,
        [
            TextSendMessage(text=problem),
            TextSendMessage(text=answer)
        ]
    )

if __name__ == "__main__":
    # Flaskアプリケーションを起動
    app.run()


