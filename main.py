from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

from tools.discovery import BuildScriptDiscoveryTool
from tools.executor import GradleExecutionTool
from tools.file_writer import FileWriter
from tools.kotlin_converter import KotlinConverterTool

# llm = OllamaLLM(model="llama3.1:8b", base_url="http://ai:11434/", temperature=0)
# llm = OllamaLLM(model="gemma2:9b", base_url="http://ai:11434/", temperature=0)
llm = OllamaLLM(model="mistral-nemo:12b", base_url="http://ai:11434/", temperature=0)

tools = [
    BuildScriptDiscoveryTool(),
    GradleExecutionTool(),
    FileWriter(),
    KotlinConverterTool(llm)
]

prompt = ChatPromptTemplate.from_messages([
    ("system", """
    You are an AI assistant capable of managing Gradle builds and converting Groovy builds to the Kotlin DSL format. 
    You have access to the following tools:
    {tools}

    When specifying actions, use the exact tool name without any additional formatting or punctuation.
    When using the kotlin_converter_tool, only specify a single filename as the input.
    When using the file_writer_tool, provide a single string with the file_path, a newline character, and then the full content to write.  
    When using the gradle_execution tool, provide the absolute path of the converted kotlin build script to the tool as the input. 

    Use the following format:
    Question: the input question you must answer
    Thought: you should always think about what to do
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action without any comments in parentheses
    Observation: the result of the action
    Thought: I now know the final answer
    Final Answer: the final answer to the original input question

    Begin!
    Question: {input}
    Thought:{agent_scratchpad}
    """)
])

agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
result = agent_executor.invoke({
    "input": """Execute the following plan step by step:
    1. Find the existing Gradle build scripts
    2. For each script in the list of scripts:
    2a. Convert the single script to Kotlin DSL
    2b. Write the converted build script to the disk, to the original path, but adding a '.kts' suffix to the filename
    3. Execute the build with the 'gradle_execution' tool, to verify that it still succeeds.
    """
})
print(result)
