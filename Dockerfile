FROM python:3.8
WORKDIR /scripts
COPY scripts/restfulapi.py restfulapi.py
COPY scripts/scrapy_google_maps.py scrapy_google_maps.py
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
EXPOSE 5000
COPY . .
CMD ["python3", "restfulapi.py"]