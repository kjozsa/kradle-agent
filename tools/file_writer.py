import os
from pathlib import Path

from langchain.tools import BaseTool
from loguru import logger
from pydantic import BaseModel, Field


class FileWriterInput(BaseModel):
    file_path_and_content: str = Field(..., description="path\ncontent")


class FileWriter(BaseTool):
    name: str = "file_writer_tool"
    description: str = "Write content to a file at the specified path"
    args_schema: type[BaseModel] = FileWriterInput

    def _run(self, input: str) -> str:
        logger.info("input: {}", input)
        split = input.split("\n")
        file_path: str = split[0]
        content: list[str] = split[1:]
        logger.debug("writing content to {}: {}", file_path, content)

        try:
            with Path(file_path).open("w", encoding="utf-8") as f:
                for line in content:
                    f.write(f"{line}\n")
            return f"File written successfully to {file_path}."
        except Exception as e:
            return "Error: " + str(e)

    async def _arun(self, file_path: str, content: str) -> str:
        raise NotImplementedError("This tool does not support async")


if __name__ == "__main__":
    FileWriter()._run(
        os.getcwd() + "/../sample/demo/build.gradle.kts\n" +
        """buildscript {\n    repositories {\n        mavenCentral()\n    }\n    dependencies {\n        classpath("io.spring.gradle:dependency-management-plugin:1.1.6")\n        classpath("org.springframework.boot:spring-boot-gradle-plugin:3.3.4")\n    }\n}\n\nplugins {\n    id(\"java\")\n    id(\"org.springframework.boot\") version \"3.3.4\"\n    id(\"io.spring.dependency-management\") version \"1.1.6\"\n}\n\n group = \"com.example\"\nversion = \"0.0.1-SNAPSHOT\"\n\n java {\n    toolchain {\n        languageVersion = JavaLanguageVersion.of(21)\n    }\n}\n\n repositories {\n    mavenCentral()\n}\n\n dependencies {\n    implementation(\"org.springframework.boot:spring-boot-starter-actuator\")\n    implementation(\"org.springframework.boot:spring-boot-starter-web\")\n    implementation(\"org.apache.camel.springboot:camel-spring-boot-starter:4.8.0\")\n    testImplementation(\"org.springframework.boot:spring-boot-starter-test\")\n    testRuntimeOnly(\"org.junit.platform:junit-platform-launcher\")\n}\ntasks.named(\"test\") {\n    useJUnitPlatform()\n}\n""")
