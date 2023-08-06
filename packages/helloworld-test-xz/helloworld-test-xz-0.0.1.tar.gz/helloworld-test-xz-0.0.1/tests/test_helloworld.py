from helloworld import say_hello

def test_helloworld_no_params():
    assert say_hello() == "hello, world!"

def test_helloworld_with_params():
    assert say_hello("A") == "hello, A!"
