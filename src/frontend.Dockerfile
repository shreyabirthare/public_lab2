FROM python:3.8-slim
WORKDIR /spring24-lab2-spring24-lab2-shreya-simran/src/front_end_service
RUN pip install --no-cache-dir requests
COPY ./front_end_service/front_end_service.py /spring24-lab2-spring24-lab2-shreya-simran/src/front_end_service/front_end_service.py
EXPOSE 12500
CMD ["python","-u","./front_end_service.py"]