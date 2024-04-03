FROM python:3.8-slim
WORKDIR /spring24-lab2-spring24-lab2-shreya-simran/src/catalog
RUN pip install --no-cache-dir requests
COPY ./catalog/catalog.py /spring24-lab2-spring24-lab2-shreya-simran/src/catalog/catalog.py
COPY ./catalog/catalog_data/catalog.csv /spring24-lab2-spring24-lab2-shreya-simran/src/catalog/catalog_data/catalog.csv
EXPOSE 12501
CMD ["python","-u","./catalog.py"]
