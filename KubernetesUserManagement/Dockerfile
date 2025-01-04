FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5001

# # Add initialization step
# RUN python init.py

CMD ["gunicorn", "--bind", "0.0.0.0:5001", "app:app"] 