from langchain.tools import BaseTool
from langchain_ollama.llms import OllamaLLM
from loguru import logger
from pydantic import Field, BaseModel


class KotlinConverterInput(BaseModel):
    script: str = Field(..., description="path")


class KotlinConverterTool(BaseTool):
    name: str = "kotlin_converter"
    description: str = "Converts Gradle build scripts from Groovy to Kotlin DSL"
    args_schema: type[BaseModel] = KotlinConverterInput
    llm: OllamaLLM = Field(default_factory=lambda: OllamaLLM(model="llama3.1:8b", base_url="http://ai:11434/"))

    def _run(self, script: str) -> str:
        logger.info("input: {}", script)

        # input = self.llm.invoke(f"""return only the script path (including filename) of this input: {script}
        #
        # Return the path only, no comments or formatting.
        # """)
        # logger.info("sanitized input: {}", input)
        input = script

        with open(input, 'r') as file:
            content = file.read()

        prompt = f"""
        Convert the following Gradle build script from Groovy to Kotlin DSL:

        {content}

        Provide only the converted Kotlin DSL script without any explanations or formatting like backticks.
        """

        logger.debug("invoking converter: {}", prompt)
        return self.llm.invoke(prompt)

    def _arun(self, script: str):
        raise NotImplementedError("This tool does not support async")


if (__name__ == '__main__'):
    result = KotlinConverterTool()._run("/home/kjozsa/workspace/ai/hello-langchain-agent/../hello-langchain-agent/sample/demo/build.gradle")
    logger.debug("result: {}", result)
