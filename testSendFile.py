import os
from flask import Flask, request, jsonify
from flask_cors import CORS

import sys
sys.path.append('./ai')
from main import textDetection

sys.path.append('./utils')
from allowedFile import allowedFile

app = Flask(__name__)
CORS(app, origins="*")

@app.route('/ai/validation', methods=['POST'])
def validation():
    MessageResponse = {
        'message': '', 
        'status': '200', 
        'content': ''
        }
    
    if request.method == 'POST':
        try:
            videoContent = request.form['videoContent']
            detectionVideo = request.files['detectionVideo']

            if 'videoContent' not in request.form or 'detectionVideo' not in request.files:
                MessageResponse['message'] = 'Video và nội dung video là bắt buộc'
                MessageResponse['status'] = '400'
            elif not allowedFile(detectionVideo.filename):
                MessageResponse['message'] = 'Video không đúng định dạng!'
            else:
                video_path = 'ai/videos/' + detectionVideo.filename
                detectionVideo.save(video_path)

                # Xử lý video => văn bản sử dụng trí tuệ nhân tạo
                detectedText = textDetection(video_path)

                if (len(detectedText) > len(videoContent)) and (videoContent in detectedText):
                    MessageResponse['content'] = detectedText
                    MessageResponse['message'] = f'Phát hiện nhiều chữ cái, có chữ cái: {videoContent}'
                elif videoContent == detectedText:
                    MessageResponse['content'] = detectedText
                    MessageResponse['message'] = 'Nội dung video trùng khớp với video!'
                else:
                    MessageResponse['message'] = 'Không phát hiện chữ cái nào!'
                
                os.remove(video_path)

        except Exception as e:
            print(f'Error: {e}')
            MessageResponse['message'] = 'Lỗi Server'
            MessageResponse['status'] = '500'

    else:
        MessageResponse['message'] = 'Phương thức không được phép'
        MessageResponse['status'] = '405'

    return jsonify(MessageResponse)


@app.route('/ai/detection', methods=['POST'])
def detection():
    MessageResponse = {
        'message': '', 
        'status': '200', 
        'content': ''
        }
    
    if request.method == 'POST':
        try:        
            detectionVideo = request.files['detectionVideo']

            if detectionVideo.filename == '':
                MessageResponse['message'] = 'Không có video!'
                MessageResponse['status'] = '400'
            elif not allowedFile(detectionVideo.filename):
                MessageResponse['message'] = 'Video không đúng định dạng!'
            else:
                video_path = 'ai/videos/' + detectionVideo.filename
                detectionVideo.save(video_path)

                # Xử lý video => văn bản sử dụng trí tuệ nhân tạo
                detectedText = textDetection(video_path)
                if detectedText is None:
                    MessageResponse['message'] = 'Video bị lỗi hoặc không phát hiện được chữ cái!'
                else: 
                    MessageResponse['content'] = detectedText
                    MessageResponse['message'] = 'Xử lý dữ liệu thành công!'

                os.remove(video_path)


        except Exception as e:
            print(f'Error: {e}')
            MessageResponse['message'] = 'Lỗi Server'
            MessageResponse['status'] = '500'
    else:
        MessageResponse['message'] = 'Phương thức không được phép'
        MessageResponse['status'] = '405'

    return jsonify(MessageResponse)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int("5000"), debug=True)
