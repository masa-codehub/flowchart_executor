import random
from flowchart_option import NodeResponse


def greet(name):
    return NodeResponse(
        message=f"Hello, {name}!"
    )


def random_age():
    age = random.randint(1, 30)
    return NodeResponse(
        result={"age": age}, message=f"Your age is {age}."
    )


def check_age(age):
    return NodeResponse(
        condition=age >= 18,
        message="You are an adult. Exiting."
    )


def adult_message():
    return NodeResponse(
        message="You are an adult. Exiting."
    )


def child_message():
    return NodeResponse(
        message="You are a child. Trying again."
    )
