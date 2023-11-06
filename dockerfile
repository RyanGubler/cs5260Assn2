FROM python:3.11
COPY main.py main.py
RUN pip install boto3
CMD ["python", "main.py","s3","usu-cs5260-goob-requests","usu-cs5260-goob-web"]