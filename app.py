# -*- coding: utf-8 -*-
# 한글 깨짐 방지

from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import csv

app = Flask(__name__)

@app.route('/')
def main():
# app.py 실행 후 localhost:5000 들어가면 templates 폴더의 index.html 실행
    return render_template('/main.html')


@app.route('/result', methods = ['get'])
def result():
    # 정답 저장된 csv 불러오기
    data = pd.read_csv('./python_answer.csv', encoding = 'utf-8')
    data = data.astype(str)
    df = np.array(data['정답'].to_list())
    
    correct = []
    for i in range(len(data)) :
        if len(df[i]) == 1 :
            correct.append([df[i]])
        else :
            correct.append(df[i].split(','))

#     고르는 정답 넣어줄 빈 리스트
    checked_answer = []
    saving_data = []
#     정답 갯수 초기화
    get_right = 0
#     1 ~ 20 문항 순서대로 값 받아와서 넣기
    for i in range(len(correct)) :
        i = i + 1
        checked_answer.append(request.values.getlist('choice'+str(i)))

#     엑셀에 저장할 답 리스트 만들기
    for i in range(len(checked_answer)) :
        if len(checked_answer[i]) == 1 :
            for j in range(len(checked_answer[i])) :
                saving_data.append(checked_answer[i][j])
        else :
            saving_data.append(",".join(checked_answer[i]))
        
#     정답과 체크한 답 비교해서 정답 갯수에 더해주기
    for i in range(len(data)) :
        if checked_answer[i] == correct[i] :
            get_right = get_right + 1
    
#     이름 받아오기 get방식은 request.args.get(name값) / post방식은 request.form[name값]
    curriculum = request.args.get('curriculum')
    subject = request.args.get('subject')
    name = request.args.get('name')
    date = request.args.get('date')
    
    new_df = pd.DataFrame({'문항' : data['문제'], '정답' : data['정답'], '체크한 답' : saving_data})
    new_df.to_csv('./{0}_{1}_{2}.csv'.format(subject, name, date), 
                  header = 1, index = False, encoding = 'cp949')

    
#     main.html 에서 get으로 받아온 결과들을 result.html 에 출력하고 get_right 변수를 right_ans 에 대입
    return render_template('/result.html', right_ans = get_right, curriculum = curriculum, name = name, 
                          subject = subject, date = date)
        
if __name__ == '__main__':
    app.run()