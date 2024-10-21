import os
from pathlib import Path

from langchain.tools import BaseTool
from loguru import logger
from pydantic import BaseModel, Field


class FileWriterInput(BaseModel):
    file_path_and_contents: str = Field(..., description="absolute path")


class FileWriter(BaseTool):
    name: str = "file_writer_tool"
    description: str = """file_path, a newline character and then the contents of the file"""
    args_schema: type[BaseModel] = FileWriterInput

    def _run(self, input: str) -> str:
        logger.info("input: {}", input)
        file_path, content = input.split("\n", 1)

        try:
            with Path(file_path).open("w", encoding="utf-8") as f:
                for line in content:
                    f.write(f"{line}\n")
            return f"Success."
        except Exception as e:
            return "Error: " + str(e)

    async def _arun(self, file_path: str, content: str) -> str:
        raise NotImplementedError("This tool does not support async")


if __name__ == "__main__":
    file_path = os.path.join(os.getcwd(), "../sample/demo/build.gradle.kts")
    input = file_path + """\n
buildscript {
    repositories {
        mavenCentral()
    }
    dependencies {
        classpath("io.spring.gradle:dependency-management-plugin:1.1.6")
        classpath("org.springframework.boot:spring-boot-gradle-plugin:3.3.4")
    }
}

plugins {
    id("java")
    id("org.springframework.boot") version "3.3.4"
    id("io.spring.dependency-management") version "1.1.6"
}

group = "com.example"
version = "0.0.1-SNAPSHOT"

java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(21)
    }
}

repositories {
    mavenCentral()
}

dependencies {
    implementation("org.springframework.boot:spring-boot-starter-actuator")
    implementation("org.springframework.boot:spring-boot-starter-web")
    implementation("org.apache.camel.springboot:camel-spring-boot-starter:4.8.0")
    testImplementation("org.springframework.boot:spring-boot-starter-test")
    testRuntimeOnly("org.junit.platform:junit-platform-launcher")
}
tasks.named("test") {
    useJUnitPlatform()
}
"""
    FileWriter()._run(input)
