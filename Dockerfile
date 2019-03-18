FROM nreinhol/python3_web3:1.0

COPY ./pyapp ./app
WORKDIR ./app

RUN pip3 install -r requirements.txt

CMD [ "python", "./src/lem_sim/simulate.py" ]
