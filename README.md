# Vendor-Management-System
## Description

This project contains codeBase for all vendor related, integration, financial calculations related implementation.


# Following the instructions to Generate database diagram(ERD) with Django Extensions Automatically.
![img.png](docs/img/imagefile_name.png)

(https://www.linkedin.com/pulse/generate-database-diagramerd-django-extensions-automatically-srujan-s/
) AND (https://www.wplogout.com/export-database-diagrams-erd-from-django/)


***
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
***

# Django and Python Version for project.

    Django - 5.0.4
    Python - 3.11.5
    Django Rest Framework = 3.15.1


***
## Installing python3.11.5 using pyenv

* The simplest and easiest way to install python3.11.5 along side your existing python version is using `pyenv`.

* Follow the instructions to install `pyenv`.
    [https://github.com/pyenv/pyenv#getting-pyenv](https://github.com/pyenv/pyenv#getting-pyenv)

* Fetch latest publications of python from remote into local
```shell
pyenv update
```
or

Run the command printed on the terminal.
When run the below command.
```shell
pyenv install 3.11.5
```

* Fetch the latest updates. Sample

```shell
cd /Users/deesh/.pyenv/plugins/python-build/../.. && git pull && cd -
```

***

## How to Install Poetry for this Repo.
* Deactivate your current environment if you have any.

1) To check Python.
```shell
which python
```
2) To check the current python existing and other functionality.
```shell
ls -lrtha
```
3) If python 3.11 is not present. Do the below point.
```shell
python -m pip install poetry
```
4) Installing Poetry.
```shell
python 3.11 -m poetry
```
5) Close the shell --> Add new Interpreter --> Local --> Poetry Environment Existing --> 3.11.5

6) Close the terminal and Start again.

Baam !! Its done.

## LTS support for Django.

![img.png](docs/img/django_lts.png)

***

## LTS support for Python

![img.png](docs/img/python_lts.png)

***

# Setup Poetry install before starting the development.

## Getting started

1. Install poetry in any of the following ways.

    ```
   pip install poetry
    ```

2. Run the following command in the root of the project to install the dependecies.

    ```
   poetry install
   ```
   * will install all the dependencies including the dev deps.

3. to configure the environment the poetry created.

    ```
   poetry show -v
   ```
   * Will show the complete path and the packages installed.

4. To activate the terminal
    ```
   poetry shell
   ```

5. To Run the project manually we can run the following command.

   ```
   poetry run python manage.py runserver 8666
   ```

6. Generate `requirements.txt` file from the `pyproject.toml` file.
    * Non-Dev dependency Alone.
      ```shell
        poetry export --without-hashes --without=dev --format=requirements.txt > requirements.txt
      ```
    * All dependecies to use in local.
      ```shell
        poetry export --without-hashes --format=requirements.txt > requirements.txt
       ```


#  Testing in Local on Postman (CURL COMMAND GIVEN BELOW TO DIRECTLY COPY PASTE IN POSTMAN):::

POST API - Create a new vendor
```commandline
curl --location 'http://localhost:8666/api/create-vendors/' \
--header 'Content-Type: application/json' \
--data '{
    "name": "Anurag",
    "contact_details": "Anurag Markets Vendor Details",
    "address": "HSR Banglore",
    "vendor_code": "VENDOR113",
    "on_time_delivery_rate": 95.0,
    "quality_rating_avg": 4.5,
    "average_response_time": 24.0,
    "fulfillment_rate": 99.0
}
'
```
GET --> Get all the vendors list.
```commandline
curl --location 'http://localhost:8666/api/vendors/' \
--data ''
```
GET --> Get a particular vendor detail.
```commandline
curl --location 'http://localhost:8666/api/vendors/1/' \
--data ''
```
PUT --> This PUT API will update any details for a given lender. Given by ID
```commandline
curl --location --request PUT 'http://localhost:8666/api/vendors/2/' \
--header 'Content-Type: application/json' \
--data '{
    "name": "Anurag",
    "contact_details": "Anurag-Grocery Markets Vendor Details",
    "address": "HSR Banglore",
    "vendor_code": "VENDOR113",
    "on_time_delivery_rate": 95.0,
    "quality_rating_avg": 4.5,
    "average_response_time": 24.0,
    "fulfillment_rate": 99.0
}
'
```
DELETE --> This will delete a particular vendor given by ID.
```commandline
curl --location --request DELETE 'http://localhost:8666/api/vendors/3/' \
--data ''
```

## NOTE :: Here is a test suite demonstrating the functionality and reliability of the endpoints.
#### FROM HERE BELOW API's ARE TOKEN AUTHENTICATED. (EVERYTHING IS GIVEN IN CURL FOR TESTING.)
#### HEADER : Authorization Token 8560d16694d9d1a53009145de85bc088be73371a

POST --> Create new Purchase Order.
```commandline
curl --location 'http://localhost:8666/api/purchase_orders/' \
--header 'Content-Type: application/json' \
--header 'Authorization: Token 8560d16694d9d1a53009145de85bc088be73371a' \
--data '{
    "po_number": "PO12335131",
    "vendor": 1,
    "order_date": "2024-05-01T08:00:00",
    "delivery_date": "2024-05-15T08:00:00",
    "items": [
        {
            "name": "Cadbury Bites",
            "description": "Chocolate",
            "unit_price": 10.50,
            "quantity": 2
        },
        {
            "name": "Sting",
            "description": "Glucose",
            "unit_price": 15.75,
            "quantity": 1
        }
    ],
    "quantity": 3,
    "status": "pending",
    "quality_rating": 4.5,
    "acknowledgment_date": "2024-04-30T10:00:00"
}
'
```
GET --> To fetch a particular purchase_order.
```commandline
curl --location 'http://localhost:8666/api/purchase_orders/1/' \
--header 'Content-Type: application/json' \
--header 'Authorization: Token 8560d16694d9d1a53009145de85bc088be73371a' \
--data ''
```
GET --> To fetch all the Purchase Orders.
```commandline
curl --location 'http://localhost:8666/api/purchase_orders/' \
--header 'Authorization: Token 8560d16694d9d1a53009145de85bc088be73371a'
```
PUT --> Update a particular record by given PurchaseOrder ID.
```commandline
curl --location --request PUT 'http://localhost:8666/api/purchase_orders/5/' \
--header 'Content-Type: application/json' \
--data '{
    "po_number": "PO12335111",
    "vendor": 1,
    "order_date": "2024-05-01T08:00:00",
    "delivery_date": "2024-05-15T08:00:00",
    "items": [
        {
            "name": "Cadbury Bite",
            "description": "Chocolate",
            "unit_price": 10.50,
            "quantity": 2
        },
        {
            "name": "Sting",
            "description": "Glucose",
            "unit_price": 15.75,
            "quantity": 1
        }
    ],
    "quantity": 3,
    "status": "pending",
    "quality_rating": 4.5,
    "acknowledgment_date": "2024-04-30T10:00:00"
}
'
```
DELETE --> Delete a particular PurchaseOrder entry by giving ID.
  ```commandline
  curl --location --request DELETE 'http://localhost:8666/api/purchase_orders/2/' \
  --data ''
  ```

GET --> PERFOMANCE MATRIX :: NOTE :: DEPENDS ON THE DATA MATRIX IS CALCULATED.
```commandline
curl --location 'http://localhost:8666/api/vendors/1/performance/' \
--header 'Authorization: Token 8560d16694d9d1a53009145de85bc088be73371a'
```
POST --> /api/purchase_orders/{po_id}/acknowledge
```commandline
curl --location --request POST 'http://localhost:8666/api/purchase_orders/1/acknowledge/' \
--header 'Authorization: Token 8560d16694d9d1a53009145de85bc088be73371a' \
--data ''
```
POST --> Token Authentication API to fetch the Token Credentials.
```commandline
curl --location 'http://127.0.0.1:8666/api-token-auth/' \
--header 'Content-Type: application/json' \
--header 'Cookie: csrftoken=sdUpVT8JkemOalwakq53dYC2Mj7FDF9U' \
--data '{
    "username": "soham",
    "password": "Starson007"
}'
```



# Setting up Postgres in local

1. Install Postgres in your system.
   - [x][Postgres Installation for all Systems](https://www.timescale.com/blog/how-to-install-psql-on-mac-ubuntu-debian-windows/)


2.  Facing > django.db.utils.OperationalError: connection to server at "localhost" (127.0.0.1), port 5432 failed: FATAL:  password authentication failed for user "postgres"?. Follow below lines :

    * Step 1: Check the status of the Postgres cluster.
    ```
    pg_lsclusters
    ```

    * Step 2: Restart the Postgres cluster
    ```
    sudo pg_ctlcluster 15 main start
    ```
    . Make sure to replace 15 with your version of Postgres.

    * Step 3: Check again and connect.
      ```
      pg_lsclusters
      ```
      ```
      sudo -i -u postgres
      ```
      ```
      psql
      ```

3. Facing > django.db.utils.OperationalError: connection to server at "localhost" (127.0.0.1), port 5432 failed: FATAL:  database "otolmsdbloc" does not exist. Facing this error?. Follow below steps:
      ```
      sudo -i u postgres
      ```
      ```
      CREATE DATABASE otolmsdbloc;
      ```
      ```
      ALTER USER postgres WITH PASSWORD 'postgres';
      ```


***
# Dev Responses
- [x] [Django LTS versions](https://www.djangoproject.com/download/)
- [x] [Python LTS versions](https://www.python.org/downloads/)


[//]: # (## Test and Deploy)

***


# Setting up pre-commit hooks

* pre-commit hooks run when we are trying to commit change into the remote repo.
* This will be make sure the steps mentioned in the file `pre-commit-config.yaml` are run if any of the steps fails it will not allow us to commit the changes.
* install pre-commit hooks.
   * mac os

      ```commandline
      brew install pre-commit
      ```
   * linux(any)

     ```commandline
     snap install pre-commit --classic
     ```
   * windows/Any environment

     ```commandline
     python3 -m pip install pre-commit
     ```

* Configuring pre-commit hooks.

1. To configure the pre-commits hooks run the following command.

  * if you install via python3 method.

    ```commandline
    python3 -m pre_commit install
    ```

  * if you installed via apt or brew run the following command to install.

     ```commandline
     pre-commit install
     ```

  * For manually running the commit hooks without even staging the files.

      ```commandline
      pre-commit run --all-files
      ```

    ## or

  * python -m flag.

    ```commandline
    python3 -m pre_commit run --all-files
    ```


# Dev Note:

![img.png](docs/img/devloper.gif)

# Reason For addition of Packages.

* python-benedict
  * East to handle with the nested dictionaries
  * ref:: https://github.com/fabiocaccamo/python-benedict#keypath
