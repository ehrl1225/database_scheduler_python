import matplotlib.pyplot as plt
import numpy as np

data = [[2, 81], [4, 93], [6, 91], [8, 97]]  # 데이터셋 설정
x = [i[0] for i in data]  # [2, 4, 6, 8]이 됨
y = [i[1] for i in data]  # [81, 93, 91, 97]이 됨

x_data = np.array(x)  # 넘파이 배열로 변환
y_data = np.array(y)

a = 0  # 기울기 a를 0으로 초기화
b = 0  # y절편 b를 0으로 초기화

lr = 0.05  # 학습률 설정 (learning rate)

epochs = 2000  # 반복 횟수 설정

# 경사 하강법 시작
for i in range(epochs):
    y_pred = a * x_data + b  # y 예측 값을 구하는 식
    error = y_data - y_pred  # 오차 error = y 값 - y 예측 값

    a_diff = -(1 / len(x_data)) * sum(x_data * (error))  # 평균 제곱 오차를 a로 미분한 값
    b_diff = -(1 / len(x_data)) * sum(y_data - y_pred)  # 평균 제곱 오차를 b로 미분한 값

    a = a - lr * a_diff  # 학습률 * 미분 결과 후 기존 a 값 업데이트
    b = b - lr * b_diff  # 학습률 * 미분 결과 후 기존 b 값 업데이트

    if i % 100 == 0:  # epoch가 100번 반복될 때마다 아래의 내용을 출력
        print("epoch = %.f, 기울기 = %.04f, 절편 = %.04f, 에러 = %.04f" % (i, a, b, error.mean()))

plt.scatter(x, y)  # 이하 그래프 출력
plt.plot([min(x_data), max(x_data)], [min(y_pred), max(y_pred)])
plt.show()
