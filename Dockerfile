FROM python:3.9

WORKDIR /book_review

COPY ./requirements.txt /book_review/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /book_review/requirements.txt

COPY ./app /book_review/app

EXPOSE 8002

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8002"]