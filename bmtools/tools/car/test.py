from bmtools.agent.singletool import load_single_tools, STQuestionAnswerer

tool_name, tool_url = 'car',  "http://127.0.0.1:8079/tools/car/"
tools_name, tools_config = load_single_tools(tool_name, tool_url)
print(tools_name, tools_config)

qa =  STQuestionAnswerer()

agent = qa.load_tools(tools_name, tools_config)

agent("介绍一下奔驰GLC这款车？")