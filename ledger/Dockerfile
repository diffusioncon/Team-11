FROM ubuntu:18.04
RUN apt update
RUN apt upgrade -y
RUN apt install python3 -y
RUN apt install python3-pip -y
RUN apt install python3-dev
RUN apt-get install librdkafka-dev -y
RUN apt-get install git -y
RUN mkdir app


WORKDIR /app
RUN apt install vim -y
RUN apt install ipython3 -y



COPY . /app

RUN git clone https://github.com/fetchai/ledger.git --branch release/v0.8.x --single-branch
RUN cd ledger
RUN apt-get install sudo

WORKDIR /app/ledger

RUN ./scripts/quickstart.sh
# ENTRYPOINT ["python"]
# CMD ["python3","-u","../app.py"]
