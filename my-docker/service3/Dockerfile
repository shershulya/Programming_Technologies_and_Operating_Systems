FROM python
VOLUME [/service3/]
WORKDIR /service3
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
CMD ["python", "service3.py"]