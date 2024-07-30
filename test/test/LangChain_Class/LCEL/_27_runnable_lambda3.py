from langchain_core.runnables import RunnableLambda
import asyncio

def add_one(x: int) -> int:
    print("sync add_one : ", x+1)

async def add_one_async(x: int) -> int:
    print("async add_one : ", x+1)

async def call_runnable():
    
    # Alternatively, can provide both synd and sync implementations
    runnable = RunnableLambda(add_one, afunc=add_one_async)

    print("\n")
    runnable.invoke(1)
    await runnable.ainvoke(1)
    print("\n")

if __name__ == "__main__":
    asyncio.run(call_runnable())
