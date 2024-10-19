import os

from langchain.tools import BaseTool
from loguru import logger

class BuildScriptDiscoveryTool(BaseTool):
    name: str = "build_script_discovery"
    description: str = "Discovers Gradle build scripts and dependency files in a project"

    def _run(self, _: str) -> str:
        build_files = []
        project_root: str = f"{os.getcwd()}/../"
        logger.debug("checking {}", project_root)
        for root, _, files in os.walk(project_root):
            for file in files:
                if file in ['build.gradle', 'build.gradle.kts', 'settings.gradle', 'settings.gradle.kts']:
                    build_files.append(os.path.join(root, file))
                elif file.endswith('.gradle') or file.endswith('.gradle.kts'):
                    build_files.append(os.path.join(root, file))

        logger.info("found: {}", build_files)
        return "\n".join(build_files)

    def _arun(self, project_root: str):
        raise NotImplementedError("This tool does not support async")


if __name__ == '__main__':
    BuildScriptDiscoveryTool()._run()
