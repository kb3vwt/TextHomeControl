FROM python:3.8-buster
WORKDIR /server/
COPY requirements.txt /server/
RUN pip install -r requirements.txt --no-cache-dir
COPY . /server/
ENV PYTHONUNBUFFERED 1
#ENTRYPOINT ["python3"]
#CMD ["main.py"]