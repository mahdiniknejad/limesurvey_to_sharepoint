FROM python:3.8
RUN mkdir /app
RUN cd /app
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "runner.py"]