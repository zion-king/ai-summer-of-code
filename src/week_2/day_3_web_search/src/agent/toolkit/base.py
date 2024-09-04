# Importing necessary libraries and modules
from typing import List
from src.agent.toolkit.google_search import create_google_tool
import logging

from src.utilities.Printer import printer
logger = logging.getLogger(__name__)

# Defining AISoCTools class
class AISoCTools:

    # Creating Google search tool
    google_tool = create_google_tool("Get Google Search",
                                     description="""Useful for when you need to look up information about topics, \
    these topics can be a wide range of topics e.g who won the superbowl 2024, this tool is ONLY needed when you need to answer questions about information beyond year 2023, currently it is year {}. \
    Use it for generic questions that you can not answer directly.""")


    # List of all tools
    toolkit = [google_tool]

    # Constructor for AISoCTools class
    def __init__(self):
        # Displaying a message after loading preliminary tools
        printer(" ⚡️⚙️  preliminary tools::loaded","purple")

    # Method to call the appropriate tool based on the specified retriever
    @classmethod
    def call_tool(cls) -> List:
        """
        Calls the appropriate tools based on the specified retriever.

        Parameters:
        - retriever: Optional, the retriever to be used. If None, default tools are used.

        Returns:
        - List of tools to be executed.
        """
        try:
            tool_names=[]
            tools = cls.toolkit

            # Logging tool names
            for tl in tools:
                tool_names.append(tl.name)
            logger.info(f"""\nTools loaded Successfully!\n -------TOOL REPORT--------\ntool names: {str(tool_names)}\nnumber of tools: {len(tool_names)}\n---------------------\n""")

            return tools

     

        except Exception as e:
            # Log an error message if an exception occurs
            logger.warning(
                "Error occurred while creating tools: %s", str(e), exc_info=1
            )
