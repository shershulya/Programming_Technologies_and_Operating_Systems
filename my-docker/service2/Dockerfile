FROM python
VOLUME [/service2/]
WORKDIR /service2
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
CMD ["python", "service2.py"]