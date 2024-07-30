class SimpleRunnable:
    def __init__(self, func):
        self.func = func

    def __or__(self, other):
        def chained_func(*args, **kwargs):
            # the other func consumes the result of this func
            return other(self.func(*args, **kwargs))
        return SimpleRunnable(chained_func)

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)
    

def add_five(x):
    return x + 5

def multiply_by_two(x):
    return x * 2


# wrap the functions with Wrapper
r_add_five = SimpleRunnable(add_five)
r_multiply_by_two = SimpleRunnable(multiply_by_two)

# run them using the object approach
chain = r_add_five.__or__(r_multiply_by_two)
print(chain(3))  # should return 16


# chain the Wrapper functions together
chain = r_add_five | r_multiply_by_two

# invoke the chain
print(chain(5))  # we should return 20