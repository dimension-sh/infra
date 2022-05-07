FROM python:3.10-alpine

ENV ANSIBLE_HOST_KEY_CHECKING=False

RUN apk add gcc python3-dev libc-dev libffi-dev openssl-dev py3-pip bash openssh py3-cryptography
RUN pip3 install --upgrade wheel
RUN pip3 install --upgrade "ansible>=4,<5"
COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
