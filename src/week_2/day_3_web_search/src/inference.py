import logging
import os
from src.agent.base.agenthead import AISoCAgent
from src.agent.base.parser import ReActSingleInputOutputParser
from src.agent.toolkit.base import AISoCTools
from src.utilities.helpers import load_yaml_file
logger = logging.getLogger(__name__)
from typing import Literal
from src.config.appconfig import Env
from langchain.agents import  AgentExecutor
from src.utilities.messages import *

# Set verbose mode to True by default
verbose =True


class StreamConversation:
    """
    A class to handle streaming conversation chains. It creates and stores memory for each conversation,
    and generates responses using the LLMs.
    """

    LLM=None

    def __init__(self,llm):
        """
        Initialize the StreamingConversation class.

        Args:
            llm: The language model for conversation generation.
        """
        self.llm=llm
        StreamConversation.LLM=llm
        
    @classmethod
    def create_prompt(
        cls, message: str
    )-> (tuple[None, None, str] | tuple[None, None, Literal['something went wrong with retrieving vector store']] | tuple[str, AgentExecutor, list, None] | tuple[Literal[''], None, None, str]):
        """
        Asynchronously create a prompt for the conversation.

        Args:
            message (str): The message to be added to the prompt.
         

        Returns:
            Tuple: A tuple containing message, agent_executor, chat_history, and an error term if any.
        """

        try:
            chat_history=[]
            updated_tools=AISoCTools.call_tool()
            prompt_path = os.path.abspath('src/prompts/instruction.yaml')
            INST_PROMPT = load_yaml_file(prompt_path)

            # instantiate the llm with aisoc multi modal agent
            agent=AISoCAgent.load_llm_and_tools(cls.LLM,updated_tools,INST_PROMPT['INSTPROMPT'],
                                                ReActSingleInputOutputParser(),
                                                "Ayo","male","Africa/Lagos UTC+1","Lagos, Nigeria")

            agent_executor = AgentExecutor(agent=agent,
                                        tools=updated_tools,
                                        max_iterations=8,
                                        handle_parsing_errors=True,
                                        verbose=verbose)
            
            return message,agent_executor,chat_history,None
        except Exception as e:
            logger.warning(
                "Error occurred while creating prompt: %s", str(e), exc_info=1
            )
            return "",None,None,str(e)
    
    @classmethod
    # StreamingResponse does not expect a coroutine function
    async def generate_response(cls,userId: str, message: str):
        """
        Asynchronously generate a response for the conversation.

        Args:
            message: str  The user's message in the conversation
   
        Returns:
            str: The generated response.

        Raises:
            Exception: If create_prompt has not been called before generate_response.
        """
        # generate prompt
        message, agent_executor, chat_history, error_term = cls.create_prompt(message)
        if error_term:
            return error_term
        elif message is None:
            return aisoc_agent_executor_custom_response
        # Check if create_prompt has been called before generate_response
        elif agent_executor is None:
            logger.warning(
                "create_prompt must be called before generate_response", "", exc_info=1
            )
        else:
            try:
                # Initialize an empty string to store the generated response sentence.
                sentence_to_model = ""
                
                # Prepare the input data for the agent's invoke function.
                input_data = {"input": message, "chat_history": chat_history}
                
                # Execute the agent's invoke coroutine function and iterate over the response.
                _agent_response = await agent_executor.ainvoke(input_data)
                # Execute the agent's invoke function and iterate over the response.
            
                # _agent_response = agent_executor.invoke(input_data)
                _agent_response_output = _agent_response.get("output")
                # Check if the output is present in the current iteration.
                if "output" in _agent_response_output:
                    if 'Thought: Do I need to use a tool?' in _agent_response_output.get("output"):
                        return aisoc_agent_executor_custom_response
                    elif 'Agent stopped due to iteration limit or time limit.' in _agent_response_output.get("output"):
                        return aisoc_agent_executor_custom_response
                else:
                    # Append the output to the sentence_to_model variable.
                    sentence_to_model += _agent_response_output
                    # Return the generated output as the response.
                    return _agent_response_output
                
            except Exception as e:
                # Log any exceptions that occur during the generation of the response.
                logger.warning(
                    "Error occurred while generating response: %s", str(e), exc_info=1
                )
                return aisoc_agent_executor_custom_response
     