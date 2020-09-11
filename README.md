### Terminal commands
Note: make sure you have `pip` and `virtualenv` installed and activate with python 3.6+.

    Source .env vars and environment variables


    To run application: python manage.py runserver

    To run all commands at once : make all

Make sure to run the initial migration commands to update the database.
    
    > python manage.py db init

    > python manage.py db migrate --message 'initial database migration'

    > python manage.py db upgrade


### Viewing the app ###

    Open the following url on your browser to view swagger documentation
    http://127.0.0.1:5000/


### Using Postman ####

    Authorization header is in the following format:

    Key: Authorization
    Value: "token_generated_during_login"


## Feature Build
Inventory Management System

## Scope
Backend Micro-service for CRUD operations

## Design Flow
Code Design Flow: controllers => services => data_layer
DTO are maintained for checking input and outputs

For each store multiple inventories can be created like food inventory, clothes inventory etc.

Each Inventory have list of products like biscuits, sports shoes, etc
Each product has a brand. 

An item is a particular unit of goods like shoes. A product can have many items.

Brand are global for the company across Stores.

one store('Retail Store 1') => many inventories (food inventory, store)
one_inventories(food inventory) = > many products(sweets, cake, etc)
one product(shoes) => many items(actually items)
one brand(nike) => many products(shoes, t-shirts, etc) 

## Use Cases:
Used to perform CRUD operations and maintain relations b/w different
components


## Implementation Logic

Simple Crud app with relations so used Flask-restplus extension to expose a REST API. JWT based authentication 

Postgres as database. Heroku for hosting, Swagger for docs

## Assumptions
I have currently allowed any admin to create entities, 
but ideally should be only allowed to admin users from with store  
Since Role management and authentication and authorization are largely out of scope here, I have implement just basics for other entities

It could most likely be the case that we might have different svcs for
things like login. I have just created basics here to give better picture.

