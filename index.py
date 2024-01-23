import os
from flask import Flask, request, jsonify
from flask_cors import CORS

import sys
sys.path.append('./ai')
from main import textDetection

app = Flask(__name__)
CORS(app, origins="*")


@app.route('/ai/detection', methods=['POST'])
def detection():
    MessageResponse = {
        'message': '', 
        'status': '200', 
        'content': ''
        }
    if request.method == 'POST':
        try:
            # Sử dụng request.get_json() để nhận dữ liệu JSON
            VideoObject = request.get_json()

            # Trích xuất dữ liệu từ JSON
            # B: https://wetalk.ibme.edu.vn/upload/hust-app//B.mp4
            # D: https://wetalk.ibme.edu.vn/upload/hust-app//D.mp4
            # Test: https://wetalk.ibme.edu.vn/upload/hust-app//video_demo.mp4
            videoUrl = VideoObject.get('videoUrl', '')

            if not videoUrl:
                # Nếu videoUrl trống, ghi lỗi vào MessageResponse
                MessageResponse['message'] = 'videoUrl là bắt buộc'
                MessageResponse['status'] = '400'
                
            else:
                # Xử lý video => văn bản sử dụng trí tuệ nhân tạo
                detectedText = textDetection(videoUrl)

                if detectedText is None:
                    MessageResponse['message'] = 'videoUrl sai hoặc không phát hiện được chữ cái!'
                else: 
                    MessageResponse['content'] = detectedText
                    MessageResponse['message'] = 'Xử lý dữ liệu thành công!'

        except Exception as e:
            print(f'Error: {e}')
            MessageResponse['message'] = 'Lỗi Server'
            MessageResponse['status'] = '500'
    else:
        MessageResponse['message'] = 'Phương thức không được phép'
        MessageResponse['status'] = '405'

    return jsonify(MessageResponse)


@app.route('/ai/validation', methods=['POST'])
def validation():
    MessageResponse = {
        'message': '', 
        'status': '200', 
        'content': ''
        }
    
    if request.method == 'POST':
        try:
            # Sử dụng request.get_json() để nhận dữ liệu JSON
            VideoObject = request.get_json()

            # Trích xuất dữ liệu từ JSON
            # B: https://wetalk.ibme.edu.vn/upload/hust-app//B.mp4
            # D: https://wetalk.ibme.edu.vn/upload/hust-app//D.mp4
            # Test: https://wetalk.ibme.edu.vn/upload/hust-app//video_demo.mp4
            videoUrl = VideoObject.get('videoUrl', '')
            videoContent = VideoObject.get('videoContent', '')

            if not videoUrl or not videoContent:
                MessageResponse['message'] = 'videoUrl và videoContent là bắt buộc'
                MessageResponse['status'] = '400'

            else:
                detectedText = textDetection(videoUrl)

                if len(detectedText) > len(videoContent) and videoContent in detectedText:
                    MessageResponse['content'] = detectedText
                    MessageResponse['message'] = f'Phát hiện nhiều chữ cái, có chữ cái "{videoContent}"'
                elif videoContent == detectedText:
                    MessageResponse['content'] = detectedText
                    MessageResponse['message'] = 'Nội dung video trùng khớp với video!'
                else:
                    MessageResponse['message'] = 'Không phát hiện chữ cái nào!'


        except Exception as e:
            print(f'Error: {e}')
            MessageResponse['message'] = 'Lỗi Server'
            MessageResponse['status'] = '500'

    else:
        MessageResponse['message'] = 'Phương thức không được phép'
        MessageResponse['status'] = '405'

    return jsonify(MessageResponse)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int("8040"), debug=True)
