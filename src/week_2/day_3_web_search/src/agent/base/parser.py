import re,logging
from typing import Union

from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.exceptions import OutputParserException

from langchain.agents.agent import AgentOutputParser
from langchain.agents.mrkl.prompt import FORMAT_INSTRUCTIONS
logger = logging.getLogger(__name__)


FINAL_ANSWER_ACTION = "Final Answer:"
MISSING_ACTION_AFTER_THOUGHT_ERROR_MESSAGE = (
    "Invalid Format: Missing 'Action:' after 'Thought:"
)
MISSING_ACTION_INPUT_AFTER_ACTION_ERROR_MESSAGE = (
    "Invalid Format: Missing 'Input:' after 'Action:'"
)
FINAL_ANSWER_AND_PARSABLE_ACTION_ERROR_MESSAGE = (
    "Parsing LLM output produced both a final answer and a parse-able action:"
)

def space_tool_name(string):
    """
    Adds spaces before capital letters in a string if the string does not already contain spaces.

    Args:
        string (str): The input string to process.

    Returns:
        str: The input string with spaces added before capital letters, or the original string if it already contains spaces.

    Example:
        >>> space_words("HelloWorld")
        'Hello World'
        >>> space_words("Hello World")
        'Hello World'
    """
    # Check if the string contains any spaces
    if ' ' not in string:
        # If no spaces, use the regex to space the words
        spaced_string = re.sub(r'(?<!^)(?=[A-Z])', ' ', string)
        return spaced_string.rstrip()
    else:
        # If spaces already exist, return the original string
        return string.rstrip()
    

class ReActSingleInputOutputParser(AgentOutputParser):

    def get_format_instructions(self) -> str:
        return FORMAT_INSTRUCTIONS

    def parse(self, text: str) -> Union[AgentAction, AgentFinish]:
        includes_answer = FINAL_ANSWER_ACTION in text
        regex = (
            r"Action\s*\d*\s*:[\s]*(.*?)[\s]*Input\s*\d*\s*:[\s]*(.*)"
        )
        
        action_match = re.search(regex, text, re.DOTALL)
        if action_match:
            if includes_answer:
                logger.error("Error occurred while parsing output: \nFINAL_ANSWER_AND_PARSABLE_ACTION_ERROR_MESSAGE: %s", text, exc_info=1)
                if "Action:" in text and "Input:" in text:
                    prunned_text = "Action:"+text.split("Action:")[1]
                    action_match = re.search(regex, prunned_text, re.DOTALL)
            action = action_match.group(1).strip()
            tool_input = action_match.group(2).strip()
            return AgentAction(action, tool_input, text)
        
        elif 'Action:' not in text  and 'Input:' not in text:
            return AgentFinish(
                {"output": text.split(FINAL_ANSWER_ACTION)[-1].strip()}, text
            )
        
        elif includes_answer:
            return AgentFinish(
                {"output": text.split(FINAL_ANSWER_ACTION)[-1].strip()}, text
            )
        if not re.search(r"Action\s*\d*\s*:[\s]*(.*?)", text, re.DOTALL):
            logger.error(
            "Error occurred while parsing output: \nCould not parse LLM output: %s", "MISSING_ACTION_AFTER_THOUGHT_ERROR_MESSAGE", exc_info=1)
            raise OutputParserException(
                f"Could not parse LLM output: `{text}`",
                observation=MISSING_ACTION_AFTER_THOUGHT_ERROR_MESSAGE,
                llm_output=text,
                send_to_llm=True,
            )
        elif not re.search(r"[\s]*Action\s*\d*\s*Input\s*\d*\s*:[\s]*(.*)", text, re.DOTALL):
            raise OutputParserException(
                f"Could not parse LLM output: `{text}`",
                observation=MISSING_ACTION_INPUT_AFTER_ACTION_ERROR_MESSAGE,
                llm_output=text,
                send_to_llm=True,
            )
                            
        else:
            logger.error(
            "Error occurred while parsing output: \nCould not parse LLM output: %s", text, exc_info=1)

    @property
    def _type(self) -> str:
        return "react-single-input"


