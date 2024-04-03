#!/bin/bash

# Function to delete the containers
delete_containers() {
    echo "Stopping and removing containers..."
    docker stop frontend-container order-container catalog-container
    docker rm frontend-container order-container catalog-container
    echo "Containers removed."
}

# Check if the first argument is 'delete'
if [ "$1" == "delete" ]; then
    delete_containers
    exit 0
fi

# Create the docker network if it doesn't already exist
network_name="my_network"
if [ -z $(docker network ls --filter name=^${network_name}$ --format="{{ .Name }}") ]; then
   docker network create ${network_name}
fi

# Build the docker images without using cache
docker build --no-cache -f frontend.Dockerfile -t frontend-image .
docker build --no-cache -f catalog.Dockerfile -t catalog-image .
docker build --no-cache -f order.Dockerfile -t order-image .

# Run the docker containers with hardcoded values
docker run -d --network my_network --name frontend-container -p 12503:12503 \
  -e FRONTEND_HOST=frontend-container \
  -e FRONT_END_PORT=12503 \
  -e CATALOG_HOST=catalog-container \
  -e CATALOG_PORT=12501 \
  -e ORDER_HOST=order-container \
  -e ORDER_PORT=12502 \
  frontend-image

docker run -d --network my_network --name order-container -p 12502:12502 \
  -e CATALOG_HOST=catalog-container \
  -e CATALOG_PORT=12501 \
  -e ORDER_HOST=order-container \
  -e ORDER_PORT=12502 \
  -v "$(pwd)/order/order_data:/spring24-lab2-spring24-lab2-shreya-simran/src/order/order_data" \
  order-image

docker run -d --network my_network --name catalog-container -p 12501:12501 \
  -e CATALOG_HOST=catalog-container \
  -e CATALOG_PORT=12501 \
  -v "$(pwd)/catalog/catalog_data:/spring24-lab2-spring24-lab2-shreya-simran/src/catalog/catalog_data" \
  catalog-image
