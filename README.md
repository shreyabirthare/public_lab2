Compsci 677: Distributed and Operating Systems

Spring 2022

# Lab 2

## Goals and Learning Outcomes

1. Learn about multi-tier architecture and microservices.
2. Learn how to implement a REST API server.
3. Learn how to handle cache consistency.
4. Learn how to containerize your service using Docker, and how to manage an application consisting
   of multiple containers using Docker Compose.

## Instructions

1. You may work in groups of two for this lab. If you decide to work in groups, you should briefly
    describe how the work is divided between the two team members in your README file.

2. You can use either python or Java for this assignment. You may optionally use C++ but TA support
    for C++ issues will be limited. For this lab you may use different languages for different
    microservices if you want.

## Lab Description

In this lab we will extend the toy store application that we implemented in the first lab. Instead
of having a monolithic server, we will now employ a two-tier design - a front-end tier and a
back-end tier - and use microservices at each tier.

### Part 1

The clients should communicate with the front-end service using the following REST APIs:

1. `GET /products/<product_name>`

    This API is used to query the details of a product. If the query is successful, the server should

    ```json
    {
        "data": {
            "name": "Tux",
            "price": 15.99,
            "quantity": 100
        }
    }
    ```

    If things went wrong, for example if the product name provided by the client does not exit, you

2. `POST /orders`

    This API will try to place an order for a certain product. The client should attach a JSON body to the POST request to provide the information needed for the order (name and quantity)

    ```json
    {
        "name": "Tux",
        "quantity": 1
    }
    ```

### Part 2
