FROM python:3.9-slim
RUN mkdir /app
COPY requirements.txt /app
RUN python3 -m pip install --upgrade pip
RUN pip3 install -r /app/requirements.txt --no-cache-dir
COPY api /app/api
COPY api_yamdb /app/api_yamdb
COPY reviews /app/reviews
COPY static /app/static
COPY templates /app/templates
COPY users /app/users
COPY ./manage.py /app
WORKDIR /app
CMD ["python3", "manage.py", "runserver", "0:8000"]
