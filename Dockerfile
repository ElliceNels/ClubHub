FROM python:3.11.4
WORKDIR /ClubHub
COPY . /ClubHub
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
ENV FLASK_APP=your_flask_app.py
ENV FLASK_RUN_HOST=0.0.0.0
CMD ["flask", "run"]
