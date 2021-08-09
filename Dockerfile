FROM python:3.8-slim-buster

WORKDIR /app

COPY . .

RUN pip3 install iota_wallet_python_binding-0.1.0-cp36-abi3-linux_x86_64.whl

RUN pip3 install iota_client_python-0.2.0_alpha.3-cp36-abi3-linux_x86_64.whl

RUN pip3 install -r requirements.txt

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]

# docker build -t api-iota-wallet .
# docker run -d -p 5000:5000 api-iota-wallet