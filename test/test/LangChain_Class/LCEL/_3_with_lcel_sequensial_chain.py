from langchain_core.prompts import PromptTemplate
from langchain_openai import AzureChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from dotenv import load_dotenv
import os

load_dotenv()


#첫번째 체인 - 극작가
template = """당신은 극작가입니다. 연극 제목이 주어졌을 때, 그 줄거리를 작성하는 것이 당신의 임무입니다.

제목:{title}
시대:{era}
시놉시스:"""

prompt = PromptTemplate(
    input_variables=["title","era"],
    template=template
)

model = AzureChatOpenAI(
            azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
            openai_api_version=os.getenv("OPENAI_API_VERSION"),
            callbacks=[StreamingStdOutCallbackHandler()],
            streaming=True,
            verbose=True               
        )

output_parser = StrOutputParser()
chain1 = prompt | model | output_parser



#두번째 체인 - 평론가
template = """당신은 연극 평론가입니다. 연극의 시놉시스가 주어지면 그 리뷰를 작성하는 것이 당신의 임무입니다.

시놉시스:
{synopsis}
리뷰:"""

prompt = PromptTemplate(
    input_variables=["synopsis"],
    template=template
)
chain2 = prompt | model | output_parser

#LCEL을 이용한 체인 연결
overall_chain = chain1 | chain2

print(overall_chain.invoke({"title":"서울의 달","era":"1980년대"}))

