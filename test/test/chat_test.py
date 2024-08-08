from langchain_core.prompts import ChatPromptTemplate, PromptTemplate, PipelinePromptTemplate


prompt = PromptTemplate.from_template("{uid}")
prompt2 = ChatPromptTemplate.from_messages([
    ("system", "order: {order}, content: {content}")
])

pipeline_prompts = [
    ("order", prompt),
]
pipe = PipelinePromptTemplate(
    final_prompt=prompt2, pipeline_prompts=pipeline_prompts
)

print(pipe.invoke({
    "uid": "test",
    "content": "test2"
}))
