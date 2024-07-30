from langchain_core.runnables import RunnableLambda

def add_one(x: int) -> int:
    return x + 1

runnable = RunnableLambda(add_one)

print("\n")
print(runnable.invoke(1))
print(runnable.batch([1, 2, 3]))
print("\n")