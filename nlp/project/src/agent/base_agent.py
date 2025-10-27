"""Agent management module: integrates LLM and custom tools."""

from pydantic import SecretStr
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from src.tools.todoist_tool import TodoistTool
from src.tools.wiki_tool import WikipediaTool
from src.config import config


class AgentManager:
    """
    Main class managing the LLM and connected tools

    Responsible for initializing the LangChain agent,
    building prompts, and handling user requests
    """

    def __init__(self) -> None:
        """Initialize the GPT LLM, load tools and prepare the agent"""
        self.llm = ChatOpenAI(
            model=config.model_name,
            temperature=config.temperature,
            api_key=SecretStr(config.openai_api_key),
        )

        self.tools = [TodoistTool(), WikipediaTool()]

        self.agent = create_agent(
            tools=self.tools,
            model=self.llm
        )

    @staticmethod
    def build_prompt(user_input: str) -> tuple:
        """
        Construct the combined system instruction and user prompt.

        Args:
            user_input (str): The input message from user.

        Returns:
            str: Full prompt text including system instructions.
        """
        system_instruction = (
            "Ты — агент по управлению задачами.\n"
            "- Показывай текущие задачи через todoist_manager("
            "action='list_tasks').\n"
            "- Создавай новые через todoist_manager"
            "(action='create_task').\n"
            "- Ищи справки через wiki_search(query).\n"
            "При создании задач уточняй, стоит ли добавить "
            "справку из Википедии.\n"
        )
        return system_instruction, user_input

    def handle_request(self, user_input: str) -> str:
        """
        Process user requests via LangChain agent.

        Args:
            user_input (str): The text command or query from user.

        Returns:
            str: Agent response or formatted error message.
        """
        system, human = self.build_prompt(user_input)
        try:
            result = self.agent.invoke(
                {
                    'messages': [
                        {
                            'role': 'system',
                            'content': system
                        },
                        {
                            'role': 'human',
                            'content': human
                        }
                        ]
                    }
            )  # type: ignore
            if isinstance(result, dict) and "messages" in result:
                messages = result["messages"]
                if messages and hasattr(messages[-1], "content"):
                    return messages[-1].content
            return str(result)

        except Exception as exc:
            return f"⚠️ Ошибка при обработке запроса: {exc}"
