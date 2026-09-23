# pip install flask
# pip install flask waitress    # 실무용 서버

from flask import Flask # 웹서버(was, application server) 생성에 필요
# 현재 was : python 프로그램 코드를 실행해서 요청을 처리하는 서버

# flask 기본 웹서버는 실무용 아님, 개발/학습용 - light-weight server
# 실무용 서버 : gunicorn, waitress, nginx ...
from waitress import serve  # waitress 서버 서비스 용

app = Flask(__name__); # flask 객체 생성. 현재 모듈의 이름을 생성자에 전달

@app.route('/about') # URL 매핑(라우팅). 클라이언트 요청이 '/'일 때 아래 함수 수행
def about():
    return '플라스크에 대해 ...'

# def abc():  # 클라이언트 요청을 처리하는 핸들러 함수
#    return '<h2>안녕하세요.</h2> 반가워요'; # 클라이언트 브라우저에 반환(전송)

@app.route('/user/<name>')  # url에 변수에 값이 담긴 경우
def user(name):
    return f'네 친구 {name}';

if __name__ == '__main__':
    # app.run()   # 실습용 기본 서버로 서비스를 실행
    # app.run(debug=False, host='0.0.0.0', port=5000); # 위와 동일
    # app.run(debug=True, host='0.0.0.0', port=5000);   # 실습에서는 이거를 활용

    # waitress 서버 사용 시
    print('웹 서버 서비스 중...')
    serve(app=app, host='0.0.0.0', port=5500);


