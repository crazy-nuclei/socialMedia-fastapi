
# SOCIAL MEDIA BACKEND

Hosted on Render: 

https://socialmedia-fastapi.onrender.com/docs

![Alt Text](./WhatsApp%20Image%202023-10-19%20at%2016.49.08.jpeg)



## TECH USED : 

FASTAPI : 

It is a modern, fast, web framework for building APIs with Python. It's designed to be efficient, easy to use, and well-documented. FastAPI is built on top of the popular ASGI (Asynchronous Server Gateway Interface) standard, which allows it to take full advantage of asynchronous programming in Python.

PostgreSQL:

Often simply referred to as "Postgres," is an open-source relational database management system (RDBMS). It is one of the most advanced and feature-rich database systems available and is known for its robustness, extensibility, and support for advanced data types.

SQLAlchemy:

It is an open-source SQL toolkit and Object-Relational Mapping (ORM) library for Python. It provides a set of high-level and low-level API tools for working with relational databases, making it easier to interact with databases while also allowing developers to work with data in an object-oriented way. 

Pydantic:

It is a Python library that simplifies data validation and parsing by providing a way to create data models with type annotations and validation rules. It's often used in conjunction with web frameworks, data serialization, and data validation. 

JWT: 

What is a JWT:

JWT is a compact, self-contained, and digitally signed token.
It consists of three parts: a header, a payload, and a signature.
The header and payload are JSON objects, which are base64-encoded to form the token.
The signature is used to verify the authenticity of the token.

How JWT Authentication Works:

A user logs in or is authenticated by a system.
Upon successful authentication, a JWT is generated and returned to the client.

The client stores the JWT (usually in a cookie or local storage) and includes it in the headers of subsequent HTTP requests.

The server, which issued the JWT or trusts the entity that issued it, verifies the token's signature and uses the data in the token to authenticate the user.

Alembic: 

It is an open-source database migration tool for Python, primarily used with SQLAlchemy. It provides a way to manage database schema changes and versioning. Database migration tools like Alembic are essential for maintaining and evolving your database schema over time, especially in the context of evolving software applications. 

Docker: 

It is an open-source platform that automates the deployment, scaling, and management of applications within containers. Containers are lightweight, portable, and self-sufficient units that can run applications and their dependencies in an isolated environment

Pytest: 

Pytest is an open-source Python testing framework that makes it easy to write simple and scalable test cases for your Python applications. It is widely used for unit testing, functional testing, and integration testing. 



