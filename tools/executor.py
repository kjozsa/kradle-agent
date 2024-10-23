import os.path
import subprocess

from langchain.tools import BaseTool
from loguru import logger
from pydantic import BaseModel, Field


class GradleExecutionInput(BaseModel):
    build_file: str = Field(..., description="absolute path")


class GradleExecutionTool(BaseTool):
    name: str = "gradle_tool"
    description: str = "Executes Gradle build commands using the specified kotlin build file and returns the output"
    args_schema: type[BaseModel] = GradleExecutionInput

    def _run(self, build_file: str) -> str:
        logger.info("input: {}", build_file)
        path = os.path.dirname(build_file)
        logger.debug("executing build in dir {}", path)

        try:
            result = subprocess.run(
                ["./gradlew", "-b", "build.gradle.kts", "build"],
                cwd=path,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            return f"Gradle build failed with error:\n{e.stderr}"

    def _arun(self, project_root: str, command: str = "build"):
        raise NotImplementedError("This tool does not support async")
