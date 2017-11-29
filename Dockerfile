FROM python:3
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY ./ /app/
EXPOSE 8000
