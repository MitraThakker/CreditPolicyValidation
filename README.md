# Credit Policy Validation

[![Build Status](https://travis-ci.com/MitraThakker/CreditPolicyValidation.svg?branch=master)](https://travis-ci.com/github/MitraThakker/CreditPolicyValidation)
[![Coverage Status](https://coveralls.io/repos/github/MitraThakker/CreditPolicyValidation/badge.svg?branch=master)](https://coveralls.io/github/MitraThakker/CreditPolicyValidation?branch=master)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/7c4b81bc7ce24a5d801cb2b9c5224ce8)](https://www.codacy.com/gh/MitraThakker/CreditPolicyValidation/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=MitraThakker/CreditPolicyValidation&amp;utm_campaign=Badge_Grade)

CreditPolicyValidation is a stateless microservice to host credit policies. It accepts customer details as a request. Based on the policies and customer's eligibility, the response would indicate whether the customer is eligible to get more credit or not.

## Contents

1. [Service Architecture](#service-architecture)
    * [Design Considerations](#design-considerations)
2. [Prerequisites](#prerequisites)
3. [Running The Service](#running-the-service)
4. [Executing Unit Tests](#executing-unit-tests)
5. [Cleaning Up](#cleaning-up)
6. [Cases Tested](#cases-tested)
7. [Built With](#built-with)

## Service Architecture

![Service Architecture](https://github.com/MitraThakker/CreditPolicyValidation/blob/master/assets/ServiceArchitecture.jpg?raw=true)

### Design Considerations

* This project uses Docker so that it can be independently run as an isolated container without disturbing the rest of the host system.
* The Docker image used is the Alpine distribution of Linux which means that it is really light-weight and has nothing more than the bare minimum kernel and Python installed by default.
* The controller/API endpoint is separated from the service layer which contains the business logic.
* The validation config comes from a YAML file rather than hard-coding the values in the code. This makes it more convenient to update the config values without the need of any re-deployment which would save time in the long run. The code only needs to be updated when there's a change in config schema or logic about new policies need to be added.
* Along with the given scenarios for accepting/rejecting the given request, additional validation checks are placed on the request attributes, their data types, and validation config schema to avoid errors due to a bad request format or invalid config schema. Examples for all test cases are given in the [Cases Tested](#cases-tested) section below.
* Steps to execute unit tests locally in an independent container are also stated below in the [Executing Unit Tests](#executing-unit-tests) section.
* Travis-CI is used to run the CI pipeline to run unit tests on every push and can be used for more complicated functions including Continuous Deployment in the future.
* Has automated code review setup via Codacy to avoid wasting the reviewers time on silly mistakes and more focus can be put  on the logic and implementation.

## Prerequisites

Prerequisites needed to run this project locally:
1. Docker (can be downloaded from the [official site](https://hub.docker.com/))
2. A clone of this repository
3. A stable internet connection for a hassle-free build :)

## Running The Service

1. Start Docker (if not already running).

2. Open Terminal and go to the root directory of the project.

```bash
cd /path/to/CreditPolicyValidation
```

3. Build the Docker image.

```bash
docker image build -t credit-policy-validation .
```

4. Verify that the image is exists in the list of images.

```bash
docker image ls
```

5. Run the docker container.

```bash
docker run -p 5000:5000 -d credit-policy-validation
```

6. Verify that the container is up and running by checking its status in the list of active containers.

```bash
docker container ls
```

7. Check the logs of the container to verify if the server is running.

```bash
docker container logs CONTAINER_ID
```

8. The validation service endpoint should be accessible on `0.0.0.0:5000/validate`.  Test it using an HTTP client like `curl` command on the terminal or by using a tool like Postman. 

## Executing Unit Tests

1. Start Docker (if not already running).

2. Open Terminal and go to the root directory of the project.

```bash
cd /path/to/CreditPolicyValidation
```

3. Build the Docker image.

```bash
docker image build -t credit-policy-validation-unit-tests -f test.Dockerfile .
```

4. Verify that the image is exists in the list of images.

```bash
docker image ls
```

5. Run the docker container.

```bash
docker run -d credit-policy-validation-unit-tests
```

6. Verify that the container has finished executing by checking the list of all containers.

```bash
docker container ls -a
```

7. Check the logs of the container to see the unit test execution with the overall coverage report.

```bash
docker container logs CONTAINER_ID
```

## Cleaning Up

1. Stop the Docker container.

```bash
docker container stop CONTAINER_ID
```

2. Remove all stopped containers.

```bash
docker system prune
```

OR

2. Remove a specific container.

```bash
docker container rm CONTAINER_ID
```

3. Remove the docker image.
```bash
docker image rm IMAGE_ID
```

## Cases Tested

1. ACCEPT

```
Request:
{
    "customer_income": 1000,
    "customer_debt": 500,
    "payment_remarks_12m": 0,
    "payment_remarks": 1,
    "customer_age": 18
}

Response:
{
    "reason": "",
    "result": "ACCEPT"
}
```

2. Low income: REJECT

```
Request:
{
    "customer_income": 499.99,
    "customer_debt": 500,
    "payment_remarks_12m": 0,
    "payment_remarks": 1,
    "customer_age": 18
}

Response:
{
    "reason": "LOW_INCOME",
    "result": "REJECT"
}
```

3. High debt for income: REJECT

```
Request:
{
    "customer_income": 1000,
    "customer_debt": 501,
    "payment_remarks_12m": 0,
    "payment_remarks": 1,
    "customer_age": 18
}

Response:
{
    "reason": "HIGH_DEBT_FOR_INCOME",
    "result": "REJECT"
}
```

4. Payment remarks 12m: REJECT

```
Request:
{
    "customer_income": 1000,
    "customer_debt": 500,
    "payment_remarks_12m": 1,
    "payment_remarks": 1,
    "customer_age": 18
}

Response:
{
    "reason": "PAYMENT_REMARKS_12M",
    "result": "REJECT"
}
```

5. Payment remarks: REJECT

```
Request:
{
    "customer_income": 1000,
    "customer_debt": 500,
    "payment_remarks_12m": 0,
    "payment_remarks": 2,
    "customer_age": 18
}

Response:
{
    "reason": "PAYMENT_REMARKS",
    "result": "REJECT"
}
```

6. Underage: REJECT

```
Request:
{
    "customer_income": 1000,
    "customer_debt": 500,
    "payment_remarks_12m": 0,
    "payment_remarks": 1,
    "customer_age": 17
}

Response:
{
    "reason": "UNDERAGE",
    "result": "REJECT"
}
```

7. Bad request (status code 400) due to missing field

```
Request:
{
    "customer_income": 1000,
    "customer_debt": 500,
    "payment_remarks_12m": 0,
    "payment_remarks": 1
}

Response:
{
    "error": "Error parsing request. Please check the request attributes and their types."
}
```

8. Bad request (status code 400) due to wrong data type for a request attribute

```
Request:
{
    "customer_income": 1000,
    "customer_debt": 500,
    "payment_remarks_12m": 0,
    "payment_remarks": 1,
    "customer_age": "test"
}

Response:
{
    "error": "Error parsing request. Please check the request attributes and their types."
}
```

9. Server error (status code 500) due to invalid schema/attribute/value in `validation_config.yaml`. This is a server side issue and will be raised even if the request is valid.

```
Request:
{
    "customer_income": 1000,
    "customer_debt": 500,
    "payment_remarks_12m": 0,
    "payment_remarks": 1,
    "customer_age": 18
}

Response:
{
    "error": "Error parsing YAML file containing policy validation config."
}
```

## Built With

* Language: Python 3.9
* Web Framework: Flask
* Deployment: Docker
* CI/CD Pipeline: Travis-CI
* Coverage Report: Coveralls
* Automated Code Review: Codacy
* And... Lots of love! :)
