FROM python:3.9-alpine
WORKDIR /app
ADD . /app
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["pytest", "--cov=src", "tests/", "--cov-report=term"]
