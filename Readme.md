# Customer Portal

## Introduction

Nebula Block Customer Portal is a web service for Nebula Block customers to manage their account.

## Features

* Customer Login
* Customer Account Management
* Customer Deposit Management
* Customer Withdrawal Management
* Customer Order Management
* Customer Trade Management
* Customer Transaction History Management

## Tech Stack

* Python 3.10+
* FastAPI
* MySQL 8.0+
* Pytest
* Docker
* Docker Composer

## Install

* Install Python 3.10+
* Install MySql 8.0+
* Install Pipenv

```shell
pip install pipenv
pipenv install
```

* DB schema

import from [app.mwb](app.mwb)

## Setup & Run

setup environment variables

```shell
cp .env_template .env
```
update the following settings

```shell
# MYSQL
MYSQL_SERVER=localhost
MYSQL_USER=root
MYSQL_PASSWORD=password
MYSQL_DB=app
```
Start the application

```shell
uvicorn main:app --reload
```
The service is running on http://127.0.0.1:8000

Documentation is on http://127.0.0.1:8000/docs

**Notice**

If you are on macOS, try running the following command to install the certificates:
```shell
/Applications/Python\ 3.x/Install\ Certificates.command
```
