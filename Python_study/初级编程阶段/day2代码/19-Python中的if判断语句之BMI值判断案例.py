'''
计算公式为：BMI=体重（kg）÷身高²（m）
'''

# 接收用户的身高（m）
height = float(input('请输入您的身高(m)：'))
# 接收用户的体重(kg)
weight = float(input('请输入您的体重(kg)：'))
# 求BMI的值
bmi = weight / height ** 2

if bmi >= 10 and bmi <= 18.4:
    print(f'您的BMI值为{bmi:.2f}，身体状态【偏瘦】')
elif bmi >= 18.5 and bmi <= 23.9:
    print(f'您的BMI值为{bmi:.2f}，身体状态【正常】')
elif bmi >= 24 and bmi <= 27.9:
    print(f'您的BMI值为{bmi:.2f}，身体状态【过重】')
else:
    print(f'您的BMI值为{bmi:.2f}，身体状态【肥胖】')