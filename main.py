from dotenv import load_dotenv
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from tools.discovery import BuildScriptDiscoveryTool
from tools.executor import GradleExecutionTool
from tools.file_writer import FileWriter
from tools.kotlin_converter import KotlinConverterTool

load_dotenv()
llm = ChatOpenAI(model="gpt-4o-mini")
# llm = OllamaLLM(model="llama3.1:8b", base_url="http://ai:11434/", temperature=0.5)
# llm = OllamaLLM(model="gemma2:9b", base_url="http://ai:11434/", temperature=0.5)
# llm = OllamaLLM(model="mistral-nemo:12b", base_url="http://ai:11434/", temperature=0.3)

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

    Instructions:
    1. When specifying actions, use the exact tool name without any additional formatting or punctuation.
    2. For kotlin_converter_tool:
       - Provide only the absolute file path of the script to convert.
       - Do not include any explanations, comments, or parentheses.
       - The input should be a single line containing only the file path.
       - Example correct input: "/home/user/project/build.gradle"
       - Example incorrect input: "/path/to/build.gradle (the path to the discovered Gradle build script)"
    3. For file_writer_tool:
       - Provide a single string as input.
       - Format the string as follows:
         <file_path>
         <file_contents>
       - The file path and contents must be separated by exactly one newline character (\n).
       - Do not include any additional newlines, spaces, or separators.
       - Example input:
         /path/to/file.txt
         This is the content of the file.  
    4. When using the gradle_tool tool, provide the absolute path of the converted kotlin build script to the tool as the input. 

    Use the following format:
    Question: the input question you must answer
    Thought: you should ALWAYS think about what to do
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

# prompt = ChatPromptTemplate.from_messages([
#     SystemMessagePromptTemplate.from_template("""
#     You are an AI assistant specialized in managing Gradle builds and converting Groovy builds to Kotlin DSL format.
#
#     You have access to the following tools:
#     {tools}
#
#     Instructions:
#     1. Use exact tool names without additional formatting: {tool_names}
#     2. For kotlin_converter_tool: Provide the absolute path of the script to convert.
#     3. For file_writer_tool:
#        - Provide a single string as input.
#        - Format the string as follows:
#          <file_path>
#          <file_contents>
#        - The file path and contents must be separated by exactly one newline character (\n).
#        - Do not include any additional newlines, spaces, or separators.
#        - Example input:
#          /path/to/file.txt
#          This is the content of the file.
#     4. For gradle_tool: Provide the absolute path of the converted Kotlin build script.
#
#     Follow this format strictly:
#     Question: <input question>
#     Thought: <your reasoning>
#     Action: <tool name>
#     Action Input: <tool input>
#     Observation: <tool output>
#     ... (repeat Thought/Action/Action Input/Observation as needed)
#     Thought: I now know the final answer
#     Final Answer: <your conclusion>
#
#     Begin your analysis:
#     Thought:{agent_scratchpad}
#     """),
#     HumanMessagePromptTemplate.from_template("{input}")
# ])

agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parse_errors=True)
result = agent_executor.invoke({"input": """
    Convert Gradle build scripts from Groovy to Kotlin DSL and verify the build. Follow these steps precisely:

    1. Discover build scripts:
       - Use the build_script_discovery tool to find all Gradle build scripts in the project.

    2. Convert and save each script:
       - For each discovered script:
         a. Use the kotlin_converter_tool to convert the script to Kotlin DSL.
         b. Use the file_writer_tool to save the converted script:
            - Use the original path but append '.kts' to the filename.
            - Example: '/path/to/build.gradle' becomes '/path/to/build.gradle.kts'

    3. Verify the build:
       - Use the gradle_tool to execute the build with the converted scripts.
       - Analyze the output to confirm the build succeeds.

    4. Report results:
       - Provide a summary of converted files and the build outcome.

    Execute these steps sequentially and report your progress after each major step.
    """
                                })
print(result)
