FROM python:3.11.3 
WORKDIR /app
COPY . /app
RUN apt-get update && apt-get install -y libgl1-mesa-glx
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8040
CMD python ./index.py

# docker build -t quynhpv/ai_server:v3 . 
# docker container run -d -p 8040:8040 quynhpv/ai_server:v3
