from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np
import warnings

# 忽略版本警告（1.6.1和1.3.0兼容，不影响功能）
warnings.filterwarnings('ignore', category=UserWarning)

app = Flask(__name__)

# 加载模型
model = joblib.load('model.pkl')

# 直接在这里定义特征映射（不需要单独的pkl文件）
FEATURE_MAPPING = {
    '年龄': {'青年': 0, '中年': 1, '老年': 2},
    '视力状况': {'近视': 0, '远视': 1},
    '是否散光': {'否': 0, '是': 1},
    '泪液分泌率': {'减少': 0, '正常': 1}
}

# 类别映射
CLASS_NAMES = {0: '硬隐形眼镜', 1: '软隐形眼镜', 2: '不佩戴'}
CLASS_COLORS = {
    0: '#e74c3c',  # 红色-硬镜
    1: '#27ae60',  # 绿色-软镜  
    2: '#f39c12'   # 橙色-不佩戴
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        
        # 将中文输入转换为数字编码
        age = FEATURE_MAPPING['年龄'][data['age']]
        vision = FEATURE_MAPPING['视力状况'][data['vision']]
        astigmatism = FEATURE_MAPPING['是否散光'][data['astigmatism']]
        tear_rate = FEATURE_MAPPING['泪液分泌率'][data['tear_rate']]
        
        # 预测
        features = np.array([[age, vision, astigmatism, tear_rate]])
        prediction = model.predict(features)[0]
        probas = model.predict_proba(features)[0]
        
        # 获取概率
        prob_dict = {
            CLASS_NAMES[i]: round(float(probas[i]), 3) 
            for i in range(len(probas))
        }
        
        result = {
            'prediction': CLASS_NAMES[prediction],
            'prediction_class': int(prediction),
            'color': CLASS_COLORS[prediction],
            'probabilities': prob_dict,
            'confidence': round(float(probas[prediction]) * 100, 1)
        }
        
        return jsonify({'success': True, 'result': result})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False)