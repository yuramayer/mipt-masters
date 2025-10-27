"""LangChain tool for interacting with Todoist API."""

from langchain.tools import BaseTool
from todoist_api_python.api import TodoistAPI
from src.config import config


class TodoistTool(BaseTool):
    """
    Tool for interacting with Todoist task manager

    Provides functionality to list existing tasks and create new ones
    """

    name: str = "todoist_manager"
    description: str = (
        "Позволяет просматривать и создавать задачи в Todoist."
        "Используй действие 'list_tasks' или 'create_task'"
    )

    def _run(
            self,
            action: str,
            task_content: str | None = None
            ) -> str:
        """
        Execute Todoist-related actions.

        Args:
            action (str): The desired action ('list_tasks' or 'create_task').
            task_content (Optional[str]): The task text to create.

        Returns:
            str: Result message or list of tasks.
        """
        api = TodoistAPI(config.todoist_api_key)

        if action == "list_tasks":
            tasks = api.get_tasks()
            if not tasks:
                return "Нет задач"
            return "\n".join(
                f"- {t}"
                for t in tasks
                )

        if action == "create_task" and task_content:
            task = api.add_task(content=task_content)
            return f"✅ Создана задача: {task.content}"

        return "Неверное действие. Используй 'list_tasks' или 'create_task'"
