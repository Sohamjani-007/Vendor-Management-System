# Vendor-Management-System
## Description

This project contains codeBase for all vendor related, integration, financial calculations related implementation.

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
   poetry run python manage.py runserver
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


# Setting up Redis in local.

1. Install redis cache in the system

  * mac os

  ```commandline
  brew install redis
  ```
       
   * linux(any)

  ```commandline
  sudo apt-get install redis
  ```
       
  or

  ```commandline
  sudo snap install redis --classic
  ```
 
## OR 
       
2. Installing via docker
    * pull the latest docker redis server image.

      ```dockerfile
      docker run --name local-redis -p 6379:6379 -d redis
      ```

    * to check the server logs
   
      ```dockerfile
      docker logs local-redis
      ```

    * To loging into the redis server(for any reason)
      
      ```dockerfile
      docker exec -it local-redis redis-cli
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