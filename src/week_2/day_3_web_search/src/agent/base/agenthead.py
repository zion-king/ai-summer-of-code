from typing import Sequence
from langchain.tools import BaseTool
from langchain.prompts import PromptTemplate
from langchain.agents.format_scratchpad import format_log_to_str
from langchain.tools.render import render_text_description
from src.utilities.helpers import get_day_date_month_year_time


class AISoCAgent:
    @classmethod
    def create_prompt(cls, tools: Sequence[BaseTool], system_prompt):
        """
        Create a AISoC prompt by formatting the system prompt with dynamic input.

        Args:
        - tools (Sequence[BaseTool]): List of tools to include in the prompt.
        - system_prompt: The system prompt template.

        Returns:
        str: Formatted AISoC prompt.
        """

        # Initialize a PromptTemplate with input variables and the system prompt
        AISoC_prompt = PromptTemplate(
            input_variables=[
                "agent_scratchpad",
                "chat_history",
                "input",
                "tool_names",
                "tools",
            ],
            template=system_prompt,
        )

        # Generate the prompt by partially filling in the template with dynamic values
        return AISoC_prompt.partial(
            tools=render_text_description(tools),
            tool_names=", ".join([t.name for t in tools]),
            current_date=get_day_date_month_year_time()[0],
            current_day_of_the_week=get_day_date_month_year_time()[1],
            current_year=get_day_date_month_year_time()[4],
            current_time=str(get_day_date_month_year_time()[5:][0])+":"+str(get_day_date_month_year_time()[5:][1])+":"+str(get_day_date_month_year_time()[5:][2])
        )

    @classmethod
    def create_prompt_with_user_data(
        cls, tools: Sequence[BaseTool], system_prompt, name, gender,timezone,current_location,
    ):
        """
        Create a AISoC prompt by formatting the system prompt with dynamic input.

        Args:
        - tools (Sequence[BaseTool]): List of tools to include in the prompt.
        - system_prompt: The system prompt template.

        Returns:
        str: Formatted AISoC prompt.
        """

        # Initialize a PromptTemplate with input variables and the system prompt
        AISoC_prompt = PromptTemplate(
            input_variables=[
                "agent_scratchpad",
                "chat_history",
                "input",
                "tool_names",
                "tools",
                "name",
                "gender",
                "timezone",
                "current_location"
              
            ],
            template=system_prompt,
        )

        # Generate the prompt by partially filling in the template with dynamic values
        return AISoC_prompt.partial(
            tools=render_text_description(tools),
            tool_names=", ".join([t.name for t in tools]),
            name=name,
            gender=gender,
            timezone=timezone,
            current_location=current_location,
            current_date=get_day_date_month_year_time()[0],
            current_day_of_the_week=get_day_date_month_year_time()[1],
            current_year=get_day_date_month_year_time()[4],
             current_time=str(get_day_date_month_year_time()[5:][0])+":"+str(get_day_date_month_year_time()[5:][1])+":"+str(get_day_date_month_year_time()[5:][2])
        )

    @classmethod
    def load_llm_and_tools(
        cls,
        llm,
        tools,
        system_prompt,
        output_parser,
        name,
        gender,
        timezone,
        current_location,

    ):
        """
        Load the language model (llm) and tools, create a prompt, and parse the output.

        Args:
        - llm: The language model.
        - tools: List of tools.
        - system_prompt: The system prompt template.
        - get_day_date_month_year_time: Function to get current date and time.
        - output_parser: Function to parse the output.

        Returns:
        dict: Output of the loaded language model and tools.
        """
        if name is None:
            # Create a prompt using the create_prompt method
            prompt = cls.create_prompt(tools=tools, system_prompt=system_prompt)
        else:
            # Create a prompt using the create_prompt method
            prompt = cls.create_prompt_with_user_data(
                tools=tools,
                system_prompt=system_prompt,
                name=name,
                gender=gender,
                timezone=timezone,
                current_location=current_location,
            )

        # Bind the language model with a stop token for generating output
        llm_with_stop = llm.bind(stop=["\nObservation"])

        # Define a sequence of processing steps for input/output data
        return (
            {
                "input": lambda x: x["input"],
                "agent_scratchpad": lambda x: format_log_to_str(
                    x["intermediate_steps"]
                ),
                "chat_history": lambda x: x["chat_history"],
            }
            | prompt  # Apply prompt processing
            | llm_with_stop  # Apply language model processing
            | output_parser  # Apply output parsing
        )
