FROM python:3.10

COPY . .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -e .

ENV FLASK_APP=mindflow/app/app.py

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]

