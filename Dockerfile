# Sử dụng image chứa Python 3.11.3
FROM python:3.11.3

# Thiết lập thư mục làm việc trong container
WORKDIR /app

# Sao chép tệp requirements.txt vào container
COPY requirements.txt requirements.txt

# Cài đặt các dependencies từ requirements.txt
RUN pip install -r requirements.txt

# Sao chép tất cả các tệp từ thư mục hiện tại của máy chủ vào thư mục /app trong container
COPY . .

# CMD để chạy ứng dụng Flask sử dụng Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
