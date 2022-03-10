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
back-end tier - and use microservices at each tier. The front-end is implemented as a single
microservice, while the back-end tier is implemented as two separate services: a catalog service and
an order service.

## Part 1: Implement Your Application as Microservices

### Front-end Service

The clients can communicate with the front-end service using the following two REST APIs:

1. `GET /products/<product_name>`

    This API is used to query the details of a product. If the query is successful, the server
    should return a JSON reply with a top-level `data` object. Similar to lab 1 the `data` object
    has three fields: `name`, `price`, and `quantity`. For instance,

    ```json
    {
        "data": {
            "name": "Tux",
            "price": 15.99,
            "quantity": 100
        }
    }
    ```

    If things went wrong, for example if the product name provided by the client does not exit, the
    front-end service should return a JSON reply with a top-level `error` object. The `error` object
    should contain two fields: `code` (for identifying the type of the error) and `message` (human
    readable explanation of what went wrong). For instance,

    ```json
    {
        "error": {
            "code": 404,
            "message": "product not found"
        }
    }
    ```

2. `POST /orders`

    This API will try to place an order for a certain product. The client should attach a JSON body
    to the POST request to provide the information needed for the order (`name` and `quantity`).

    ```json
    {
        "name": "Tux",
        "quantity": 1
    }
    ```

    If the order is placed successfully, the front-end service returns a JSON object with a
    top-level `data` object, which only has one field named `order_number`.

    ```json
    {
        "data": {
            "order_number": 10
        }
    }
    ```

    In case of error, the front-end service returns a JSON reply with a top-level `error` object,
    which has two fields `code` and `message`, similar to the product query API.

    **Note that when implementing the front-end service you can NOT using existing web frameworks
    like [`Django`](https://github.com/perwendel/spark),
    [`Flask`](https://github.com/pallets/flask), [`Spark`](https://github.com/perwendel/spark),
    etc.** You'll have to handle the HTTP requests directly or you can implement your own simple web
    framework (it's actually not as hard as you may think). If you don't know how to get started on
    this part, be sure to check out the [FAQ](https://piazza.com/class/kymwriudjoy7c4?cid=220) on
    Piazza.

### Catalog Service

When the front-end service receives a query request, it will forward the request to the catalog
service. The catalog service needs to maintain the catalog data, both in a memory cache and in a CSV
file on disk (in production people usually have a separate database service, but here we just use a
file to simulate it).

### Order Service

When the front-end service receives an order request, it will forward the request to the order
service. Obviously the order service still needs to talk with the catalog service to complete the
order. If the order was successful, the order service generates an order number and returns it to
the front-end service. The order number should be an unique, incremental number, starting from 0.
The order service also need to maintain the order log (including order number, product name, and
quantity) in a persistent manner. Similar to the catalog service, we will just use a simple CSV file
on disk as the persistent storage.


### Client

The client in this lab works in the following way. First it opens a connection with the front-end
service, then it randomly queries an item. If the returned quantity is greater than zero, with
probability $p$ it will send another order request using the same connection. Make $p$ and
adjustable parameter in the range $[0, 1]$ so that you can test how your application performs when
the percentage of order requests changes.

### Communication

We have specified that the front-end services should provide REST APIs to the client, but it's up to
you to decide how the microservices talk with each other. You can use REST API, RPC, RMI, raw
socket, etc.

### Concurrency

It's important that all your microservices can handle requests concurrently. You can use any of the
concurrency models taught in class: thread-per-request, threadpool, async, etc.

## Part 2: Containerize Your Application

Create a dockerfile for each of the three microservices that you implemented in part 1. Verify that
they build and run without issue.

After that write a docker compose file that can bring up (or tear down) all three services using one
`docker-compose up` (or `docker-compose down`) command.

Note that files you write in a docker container are not directly accessible from the host, and they
will be erased when the container is removed. Therefore, you should mount a directory on the host as
a volume to the catalog and order services, so that the logs can be persisted after the containers
are removed.

Another thing to notice is that when you use docker compose to bring up containers it will set up a
new network for all the containers, the containers will have a different IP address in this network
than your host IP address. Therefore, you need to consider how to pass the ip/hostnames to the
services so that they know how to locate other services regardless of whether they are running on
"bare metal" or inside containers. (HINT: you can set environment variables when building a docker
image or in a docker compose file).

## Part 3: Performance Evaluation

TODO

## What to Submit

At the top of this README file add the name(s) and umass email address(es) of all the team members .
Also if you are working in a group, briefly describe how the work is divided.

You solution should contain source code for both parts separately. Inside the `src` directory, you
should have a separate folder for each component/microservice, e.g., a `client` folder for client
code, a `front-end` folder for the front-end service, etc.

The dockerfiles and docker compose files should be placed under the root folder. Also include a
`build.sh` script that can build all your images. This script should be able to build your images on
Edlab machines.

Submit the following additional documents inside the docs directory. 1) A Brief design document (1
to 2 pages) that explains your design choices (include citations, if you used referred to Internet
sources), 2) An Output file (1 to 2 pages), showing sample output or screenshots to indicate your
program works, and 3) An Evaluation doc (2 to 3 pages), for part 3 showing plots and making
observations.

Your GitHub repo is expected to contain many commits with proper commit messages (which is good
programming practice). Use GitHub to develop your lab and not just to submit the final version. We
expect a reasonable number of commits and meaningful commit messages from both members of the group
(there is no "target" number of commits that is expected, just enough to show you are using GitHub
as one should).

## Grading Rubric

1) Part 1 50% of the lab grade.

    For full credit:

    * Source code should build and work correctly (25%),
    * Code should have in-line comments (5%),
    * A design doc should be submitted (10%),
    * An output file should be included (5%),
    * GitHub repo should have adequate commits and meaningful commit messages (5%).

2) Part 2 is 35% of the lab grade.

    For full credit:

    * The dockerfiles should build each microservice successfully (15%),
    * The docker compose file should be able to bring up/tear down the whole application using one
        command (10%),
    * The catalog file and order log file should be persisted after container removal (5%).

3) Part 3 is % of the grade.

    For full credit:

    * Eval document should be turned in with measurements for Part 1 and 2 (shown as plots where
        possible and tables otherwise) (10%),
    * Explaining the plots by addressing answers to the 4 questions listed in Part 3 (10%).

Late policy will include 10% of points per day. Medical or covid exceptions require advance notice,
and should be submitted through pizza (use exceptionRequests folder in pizza). Three free late days
per group are available for the entire semester - use them wisely and do not use them up for one lab
by managing your time well.

## References

1. HTTP protocol: https://en.wikipedia.org/wiki/Hypertext_Transfer_Protocol
2. Dockerfile reference: https://docs.docker.com/engine/reference/builder/
3. Compose file reference: https://docs.docker.com/compose/compose-file/
4. Docker volumes: https://docs.docker.com/storage/volumes/
