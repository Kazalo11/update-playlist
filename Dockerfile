FROM python:3.10-alpine
WORKDIR /usr/app/src
COPY main.py ./
COPY requirements.txt ./
RUN pip install -r requirements.txt
CMD ["python3", "./main.py"]