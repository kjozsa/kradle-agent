from langchain.tools import BaseTool
from langchain_ollama.llms import OllamaLLM
from pydantic import Field


class KotlinConverterTool(BaseTool):
    name: str = "kotlin_converter"
    description: str = "Converts Gradle build scripts from Groovy to Kotlin DSL"
    llm: OllamaLLM = Field(default_factory=lambda: OllamaLLM(model="llama3.1:8b", base_url="http://ai:11434/"))

    def _run(self, script: str) -> str:
        prompt = f"""
        Convert the following Gradle build script from Groovy to Kotlin DSL:

        {script}

        Provide only the converted Kotlin DSL script without any explanations.
        """

        return self.llm(prompt)

    def _arun(self, script: str):
        raise NotImplementedError("This tool does not support async")
