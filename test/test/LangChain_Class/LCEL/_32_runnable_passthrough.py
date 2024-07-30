from langchain_core.runnables import RunnablePassthrough


print(RunnablePassthrough().invoke(1))

print(RunnablePassthrough().invoke({"num":1}))

runnable_assign = RunnablePassthrough().assign(plus_one=lambda x: x["num"]+1)
print(runnable_assign.invoke({"num":2}))

