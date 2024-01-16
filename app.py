from flask import Flask, request, jsonify
from flask_cors import CORS

import sys
sys.path.append('./AI_HandSign')
from main import textDetection

app = Flask(__name__)
CORS(app, origins="*")

@app.route('/text_detection', methods=['POST'])
def result():
    MessageResponse = {
        'message': '', 
        'status': '', 
        'detectedText': ''}

    if request.method == 'POST':
        try:
            # Sử dụng request.get_json() để nhận dữ liệu JSON
            VideoObject = request.get_json()

            # Trích xuất dữ liệu từ JSON
            urlVideo = VideoObject.get('urlVideo', '')

            if not urlVideo:
                # Nếu urlVideo trống, ghi lỗi vào MessageResponse
                MessageResponse['message'] = 'urlVideo là bắt buộc'
                MessageResponse['status'] = '400'
                
            else:
                # Xử lý video => văn bản sử dụng trí tuệ nhân tạo
                detectedText = textDetection(urlVideo)

                MessageResponse['message'] = 'Xử lý dữ liệu thành công!'
                MessageResponse['status'] = '200'
                MessageResponse['detectedText'] = detectedText

        except Exception as e:
            MessageResponse['message'] = 'Lỗi Server'
            MessageResponse['status'] = '500'
    else:
        MessageResponse['message'] = 'Phương thức không được phép'
        MessageResponse['status'] = '405'

    return jsonify(MessageResponse)

if __name__ == '__main__':
    app.run(debug=True, host="localhost", port=5000)
