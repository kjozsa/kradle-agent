import subprocess

from langchain.tools import BaseTool
from loguru import logger

class GradleExecutionTool(BaseTool):
    name: str = "gradle_execution"
    description: str = "Executes Gradle build commands and returns the output"

    def _run(self, project_root: str, command: str = "build") -> str:
        logger.info("input: {}", command)
        try:
            result = subprocess.run(
                ["./gradlew", command],
                cwd=project_root,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            return f"Gradle build failed with error:\n{e.stderr}"

    def _arun(self, project_root: str, command: str = "build"):
        raise NotImplementedError("This tool does not support async")
