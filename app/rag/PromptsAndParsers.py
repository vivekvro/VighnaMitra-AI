from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser,PydanticOutputParser
from pydantic import BaseModel,Field
from typing import Literal,Annotated

StrParser = StrOutputParser()

class InputClassifier(BaseModel):
    type: Annotated[
        Literal[
            "NormalChat",
            "Question",
            "CurrentEventQuestion",
            "DocumentQuestion",
            "TechnicalCodingQuestion",
            "OpinionOrAdvice",
            "TaskInstruction",
            "Greeting"
        ],
        Field(description="Classify the User Input into one of the given types")
    ]
InputClassifierParser = PydanticOutputParser(pydantic_object=InputClassifier)
UserInputClassificationPrompt = PromptTemplate(
    template="""
You are an Expert User Input Classifier Assistant.

User input:
    {userinput}

Classify User Input into ONE of the following types:

1. NormalChat → casual conversation
2. Question → general factual question
3. CurrentEventQuestion → news, live events, recent info
4. DocumentQuestion → question related to uploaded document/PDF/text
5. TechnicalCodingQuestion → programming, ML, debugging, code help
6. OpinionOrAdvice → asking suggestion, recommendation, guidance
7. TaskInstruction → asking to generate/write/summarize/create something
8. Greeting → hi, hello, thanks, bye

Note:
- Return ONLY one word from the types.
- Do not explain.

{format_instructions}
""",
    input_variables=["userinput"],
    partial_variables={
        "format_instructions": InputClassifierParser.get_format_instructions()
    }
)




QuestionsFromDocumentPrompt = PromptTemplate(
    template="""
    You are a Helpful Smart Assistent.
    Your work is to Answer User's query from the given context.
    Answer should not be out of context and if given context do not have proper information for User Query , just reply "Sorry there is a problem/No information is available."
        User Query: {userinput}
        and context:
        {context}
"""
)
