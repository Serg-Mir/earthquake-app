FROM python:3.11-slim

WORKDIR /earthquake_app
ENV PYTHONPATH="${PYTHONPATH}:earthquake_app"

COPY requirements/*.txt ./requirements/

RUN pip install --no-cache-dir -r requirements/base.txt

COPY . .

ENTRYPOINT ["python", "earthquake_app/main.py"]
