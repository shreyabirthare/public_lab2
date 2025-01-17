FROM python:3.8-slim
WORKDIR /spring24-lab2-spring24-lab2-shreya-simran/src/order
RUN pip install --no-cache-dir requests
COPY ./order/order.py /spring24-lab2-spring24-lab2-shreya-simran/src/order/order.py
EXPOSE 12502
CMD ["python","-u","./order.py"]
