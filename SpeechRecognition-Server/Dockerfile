FROM python:3

WORKDIR /usr/src/app

# DO "pip freeze > requirements.txt" TO SAVE YOUR REQUIREMENTS IN A FILE
# COPY "requirements.txt" "./"
RUN pip install SpeechRecognition

# Since I cannot do pip freeze, we will manually install speech recognition
# RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./server.py" ]