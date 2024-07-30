from langchain_core.runnables import RunnableLambda

def add_one(x: int) -> int:
    return x + 1

def mul_three(x: int) -> int:
    return x * 3

def mul_four(x: int) -> int:
    return x * 4


runnable_add_one = RunnableLambda(add_one)
runnable_mul_three = RunnableLambda(mul_three)
runnable_mul_four = RunnableLambda(mul_four)

sequence = (
    runnable_add_one 
    | (lambda x: x+2)
    | {"mul_three": runnable_mul_three, "mul_four": runnable_mul_four}
)

print("\n")
print(sequence.invoke(1))
print(sequence.batch([1, 2, 3]))
print("\n")

