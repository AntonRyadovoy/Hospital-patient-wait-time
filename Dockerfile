FROM python:3.11-slim

WORKDIR /opt/emg_bot

COPY . .

RUN mkdir emgg

RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3", "emg_bot.py"]