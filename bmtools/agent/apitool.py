"""Interface for tools."""
from inspect import signature
from typing import Any, Awaitable, Callable, Optional, Union

from langchain.agents import Tool as LangChainTool
from langchain.tools.base import BaseTool
import requests
import json
import http.client
http.client._MAXLINE = 655360

from bmtools import get_logger

logger = get_logger(__name__)

class Tool(LangChainTool):
    tool_logo_md: str = ""

class RequestTool(BaseTool):
    """Tool that takes in function or coroutine directly."""

    description: str = ""
    func: Callable[[str], str]
    coroutine: Optional[Callable[[str], Awaitable[str]]] = None
    max_output_len = 4000
    tool_logo_md: str = ""

    def _run(self, tool_input: str) -> str:
        """Use the tool."""
        return self.func(tool_input)

    async def _arun(self, tool_input: str) -> str:
        """Use the tool asynchronously."""
        if self.coroutine:
            return await self.coroutine(tool_input)
        raise NotImplementedError("Tool does not support async")


    def convert_prompt(self,params):
        lines = "Your input should be a json: {{"
        for p in params:
            logger.debug(p)
            optional = not p['required']
            description = p.get('description', '')
            if len(description) > 0:
                description = "("+description+")"

            lines +=  '"{name}" : {type}{desc},'.format(
                                                                    name=p['name'],
                                                                    type= p['schema']['type'], 
                                                                    optional=optional,
                                                                    desc=description)

        lines += "}}"
        return lines
        


    def __init__(self, root_url, func_url, method, request_info,  **kwargs):
        """ Store the function, description, and tool_name in a class to store the information
        """
        url = root_url + func_url
    
        def func(json_args):
            if isinstance(json_args, str):
                # json_args = json_args.replace("\'", "\"")
                # print(json_args)
                try:
                    json_args = json.loads(json_args)
                except:
                    return "Your input can not be parsed as json, please use thought."
            response = requests.get(url, json_args) #TODO
            if response.status_code == 200:
                message = response.text
            else:
                message = f"Error code {response.status_code}. You can try (1) Change your input (2) Call another function. (If the same error code is produced more than 4 times, please use Thought: I can not use these APIs, so I will stop. Final Answer: No Answer, please check the APIs.)"
            
            message = message[:self.max_output_len] # TODO: not rigorous, to improve
            return message
        
        tool_name = func_url.replace("/", ".").strip(".")

        if 'parameters' in request_info[method]:
            str_doc = self.convert_prompt(request_info[method]['parameters'])
        else:
            str_doc = ''


        description = f"- {tool_name}:\n" + \
             request_info[method].get('summary', '').replace("{", "{{").replace("}", "}}") \
                + "," \
                + request_info[method].get('description','').replace("{", "{{").replace("}", "}}") \
                + str_doc \
                + f"The Action to trigger this API should be {tool_name}\n and the input parameters should be a json dict string. Pay attention to the type of parameters.\n"

        logger.info("API Name: {}".format(tool_name))
        logger.info("API Description: {}".format(description))

        super(RequestTool, self).__init__(
            name=tool_name, func=func, description=description, **kwargs
        )

