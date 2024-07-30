from langchain_core.runnables import RunnableLambda
import asyncio

def add_one(x: int) -> int:
    return x + 1

# Async is supported by default by delegating to the sync implementation
async def call_runnable():
    
    runnable = RunnableLambda(add_one)

    print("\n")    
    print(await runnable.ainvoke(1))
    print(await runnable.abatch([1, 2, 3]))
    print("\n")

if __name__ == "__main__":
    asyncio.run(call_runnable())