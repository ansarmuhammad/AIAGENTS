# -*- coding: utf-8 -*-
"""crewai_v1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Cg2daEUkzIlxlswylyVpLQ4jUJEvv40v
"""

2+2

!pip install -q crewai

!pip install -q anthropic

import os
from crewai import Agent, Task, Crew
from anthropic import Anthropic

os.environ["ANTHROPIC_API_KEY"] = "removed the secret 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"

client=Anthropic()

sonnet="claude-3-5-sonnet-20240620"
new_sonnet="max-tokens-3-5-sonnet-2024-07-15"
haiku="claude-3-haiku-20240307"

message = client.messages.create(
    model=sonnet,
    max_tokens=100,
    temperature=0.7,
    messages=[
        {

         "role":"user",
         "content":"hello claude, can you hear me"
        }
    ]

)
print(message.content[0].text)

#niche=input("enter business nicshe:")
#location=input("enter location:")
#num_leads=int(input("enter number of leads:"))

niche="facebook ads agency"
location="sydney"
num_leads=5

!pip install -q langchain-anthropic

from langchain_anthropic import ChatAnthropic

Consistent = ChatAnthropic(
    temperature=0.0,
    model_name=sonnet
)

Creative = ChatAnthropic(
    temperature=0.8,
    model_name=sonnet
)

variation_agent = Agent(
    role="search query specialist",

    goal="Generate 10 different and effective search queries for lead generation",

    backstory="""you are an expert in crafting search queries that yield high quality business leads. your expertise lies
    in understanding user intent and translation it into 10 various search phrases
    that capture different aspects of the target business niche and location.""",

    verbose = True,

    allow_delegation=False,

    llm=Creative



)

generate_variations=Task(
    description = f"""Generate 10 different and concise search queries for {niche} in {location}.
    make sure every search query is short and direct, it should be optimized for SerpAPI.
    each query should be unique and different from the rest. do not use quotation marks.
    DO NOT INCLUDE ANY EXTRA TEXT. JUST OUTPUT THE 10 SEARCH QUERY VARIATIONS. NOTHING BEFORE IT, NOTHING AFTER IT.
    """,

    expected_output="A list of 10 unique search queries, each on a new line",
    agent=variation_agent

)

search_query_crew=Crew(
    agents=[variation_agent],
    tasks=[generate_variations],
    verbose=2
)

search_queries_result=search_query_crew.kickoff()
print("\ngenerate search queries:")
print(search_queries_result)

!pip install -q 'crewai[tools]'

from crewai_tools import SerperDevTool

os.environ["SERPER_API-KEY"]="removed the secret b698d3f4c6e2f11b19bf3367a8e0a1ceb814a106"

search_tool = SerperDevTool()

search_agent = Agent(
    role = "Web Search Specialist",
    goal = "use the search tool function you have assigned. only use the tool.",
    backstory = """your only task is to execute the search tool you have access to.
    do not perform any other actions, or generate any other text, simply use the tool.""",
    verbose = True,
    allow_delegation = False,
    tools = [search_tool],
    llm = Consistent

)

search_task = Task(
    description=f"""use the provided search tool to find {num_leads} unique {niche} in {location},
    use these exact search queries : {search_queries_result}. do not invent your own search terms, only use those 10 queries,
    only output the websites of those businesses. no other info, website only.
    do not add formatting. simply output each website on a new line. thats it.""",
    expected_output=f"clean list with no formatting, of {num_leads} website in the {niche} niche",
    agent = search_agent

)

search_queries_result

search_crew = Crew(
    agents = [search_agent],
    tasks = [search_task],
    verbose = 2
)

search_result = search_crew.kickoff()
print("\nsearch results:")
print(search_result)
