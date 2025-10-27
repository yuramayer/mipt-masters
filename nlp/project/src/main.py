"""Entry point for the proactive LangChain-based task management agent."""

from src.agent.base_agent import AgentManager


def main() -> None:
    """
    Run the interactive agent session in CLI mode

    Provides a command-line interface for creating and
    viewing tasks through Todoist and Wikipedia tools.
    """
    agent_manager = AgentManager()
    print("Агент запущен. Введи запрос ('exit' для выхода):")

    while True:
        user_input = input("\n> ").strip()
        if user_input.lower() in {"exit", "quit"}:
            print("👋 До встречи!")
            break

        response = agent_manager.handle_request(
            user_input
            )
        print(f"\nResponse: {response}")


if __name__ == "__main__":
    main()


