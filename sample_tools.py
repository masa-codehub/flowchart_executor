import random


def greet(name):
    return {"message": f"Hello, {name}!"}


def random_age():
    age = random.randint(1, 30)
    return {"age": age, "message": f"Generated random age: {age}"}


def check_age(age):
    return {"condition": age >= 18}


def adult_message():
    return {"message": "You are an adult. Exiting."}


def child_message():
    return {"message": "You are a child. Trying again."}
