from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chains import SequentialChain
from langchain_openai import AzureChatOpenAI

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

chain1 = LLMChain(
    llm= AzureChatOpenAI(
        azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        openai_api_version=os.getenv("OPENAI_API_VERSION")
    ),
    prompt=prompt,
    output_key="synopsis",
    verbose=True
)

#두번째 체인 - 평론가
template = """당신은 연극 평론가입니다. 연극의 시놉시스가 주어지면 그 리뷰를 작성하는 것이 당신의 임무입니다.

시놉시스:
{synopsis}
리뷰:"""

prompt = PromptTemplate(
    input_variables=["synopsis"],
    template=template
)

chain2 = LLMChain(
    llm= AzureChatOpenAI(
        azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        openai_api_version=os.getenv("OPENAI_API_VERSION")
    ),
    prompt=prompt,
    output_key="review",
    verbose=True
)


#두 체인을 연결
overall_chain = SequentialChain(
    chains=[chain1, chain2],
    input_variables=["title", "era"],
    output_variables=["synopsis","review"],
    verbose=True
)

print(overall_chain({"title":"서울의 달", "era":"1980년대"}))