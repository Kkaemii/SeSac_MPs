from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

@app.route('/')
def home():
  return render_template('index.html')

#method는 리스트 형태로 제공해야 flask가 해석하는 방식이기 때문이다.
@app.route('/user', methods=['POST'])
def user():
  username = request.form.get('username', '')
  return render_template('user.html', username = username)

#method는 리스트 형태로 제공해야 flask가 해석하는 방식이기 때문이다.
@app.route('/multiple_form', methods=['POST','GET']) 
def multiple_form():
  num = request.form.get('num', '')
  print(num)
  #서버에서 유효성 검증
  if num.isdigit() and 1 <= int(num) <= 9:
    return redirect(url_for('multiple', num = num))
  #get으로 들어오는 요청 처리
  #get에서는 args.get으로 input을 처리한다.
  elif request.method == 'GET':
    num = request.args.get('num','')
    return redirect(url_for('multiple', num = num))    
  else:
    return '1부터 9까지의 숫자 하나만 입력하세요',400

@app.route('/multiple/<int:num>')
def multiple(num):
  return render_template('multiple.html', num = num)


if __name__ == '__main__':
  app.run(port= 3000 ,debug=True)