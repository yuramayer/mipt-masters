"""LangChain tool for retrieving information from Wikipedia."""

from langchain.tools import BaseTool
import wikipedia


class WikipediaTool(BaseTool):
    """
    Tool for retrieving short descriptions from Wikipedia

    Performs summary search for a given topic in Russian
    """

    name: str = "wiki_search"
    description: str = "Ищет краткое описание темы в Википедии"

    def _run(self, query: str) -> str:
        """
        Perform Wikipedia search

        Args:
            query (str): Search term or topic

        Returns:
            str: Short summary or error message
        """
        wikipedia.set_lang("ru")
        try:
            return wikipedia.summary(query, sentences=2)
        except Exception as exc:
            return f"Ошибка при поиске: {exc}"
