from flask import Flask, request, render_template, redirect, url_for, send_file
from pymongo import MongoClient
import gridfs
from bson.objectid import ObjectId
import io

app = Flask(__name__)

# MongoDB 연결
client = MongoClient('localhost', 27017)
db = client.image_database #image_database 데이터 베이스 사용
fs = gridfs.GridFS(db)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'], endpoint='upload')
def upload():
    if 'image' not in request.files:
        return '이미지를 선택해주세요', 400
    
    file = request.files['image']
    #request를 통해서 html에서 받아온 내용을 File Storage에 담아서 반환환
    if file.filename == '':
        return '파일이 선택되지 않았습니다', 400
    
    # 이미지 저장
    file_id = fs.put(file.read(), filename=file.filename)
    return redirect(url_for('gallery'))

@app.route('/gallery',methods=['GET'], endpoint='gallery')
def gallery():
    # 모든 이미지 정보 가져오기
    images = []
    for grids in fs.find():
        images.append({
            'id': str(grids._id),
            'filename': grids.filename
        })
    return render_template('gallery.html', images=images)

@app.route('/image/<file_id>',methods=['GET'], endpoint='get_image')
def get_image(file_id):
    try:
        file_data = fs.get(ObjectId(file_id))
        return send_file(
            io.BytesIO(file_data.read()),
            mimetype='image/jpeg',
            as_attachment=False  # 브라우저에서 직접 표시
        )
    except:
        return '이미지를 찾을 수 없습니다', 404

@app.route('/delete/<file_id>', methods=['POST'], endpoint='delete_image')
def delete_image(file_id):
    try:
        fs.delete(ObjectId(file_id))
        return redirect(url_for('gallery'))
    except:
        return '삭제 실패', 500

if __name__ == '__main__':
    app.run(debug=True)