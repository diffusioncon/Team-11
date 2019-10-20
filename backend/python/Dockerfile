FROM ubuntu:19.04
RUN apt update
RUN apt upgrade -y
RUN apt install python3.7 -y
RUN apt install python3-pip -y
RUN apt install python3-dev
RUN apt-get install librdkafka-dev -y
RUN apt-get install git -y

RUN apt-get install protobuf-compiler -y

#RUN git clone --single-branch --branch release/v0.7.x https://github.com/fetchai/ledger-api-py.git

RUN git clone https://github.com/fetchai/ledger-api-py.git

WORKDIR /ledger-api-py 

RUN python3.7 setup.py install 

RUN mkdir app
WORKDIR /app

#RUN python3 setup.py install

COPY requirements.txt /app
RUN python3.7 -m pip install -r /app/requirements.txt
COPY . /app
RUN apt-get install ipython3 -y
# ENTRYPOINT ["python"]
CMD ["python3.7","-u","mainEntry.py"]
# CMD ["python3.7","-u","APPSTOP.py"]

