from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import ChatPromptTemplate
from langchain_community.tools import WriteFileTool
from langchain_ollama.llms import OllamaLLM

from tools.discovery import BuildScriptDiscoveryTool
from tools.executor import GradleExecutionTool
from tools.gradle_converter import KotlinConverterTool

tools = [
    BuildScriptDiscoveryTool(),
    GradleExecutionTool(),
    WriteFileTool(root_dir='.')
    KotlinConverterTool()
]

prompt = ChatPromptTemplate.from_messages([
    ("system", """
    You are an AI assistant capable of managing Gradle builds and converting Groovy builds to the Kotlin DSL format. 
    You have access to the following tools:
    {tools}

    Use the following format:

    Question: the input question you must answer
    Thought: you should always think about what to do
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action, if any, without any comments in parentheses!
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    Final Answer: the final answer to the original input question

    Begin!

    Question: {input}
    Thought:{agent_scratchpad}
    """)
])

llm = OllamaLLM(model="llama3.1:8b", base_url="http://ai:11434/")

agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
result = agent_executor.invoke({"input": """Execute the following plan:
    1. Find the existing Gradle build scripts
    2. Iterate on the list of scripts:
    2a. Convert the script to Kotlin DSL
    2b. Write the converted build script to the disk, to the original path
    3. Verify the build still executing successfully."""
})
print(result)
