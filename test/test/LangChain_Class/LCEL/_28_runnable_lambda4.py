from langchain_core.runnables import RunnableLambda

def routing_function(input):
    if isinstance(input, str) == True:
        return input.upper()
    elif isinstance(input, int) == True:
        return input + 1
    elif isinstance(input, float) == True:
        return input * 2
    else:
        return "goodbye"


branch = RunnableLambda(routing_function)

print(branch.invoke("hello"))
print(branch.invoke(3))
print(branch.invoke(2.3))
print(branch.invoke(None))

