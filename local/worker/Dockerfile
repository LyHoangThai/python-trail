FROM python:3.12-slim
WORKDIR /worker
COPY worker.py rubric.py new_lessons.py plc.py .
CMD ["python", "-u", "worker.py"]
