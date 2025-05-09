from openai import AsyncAzureOpenAI
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerHTTP
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from rich.prompt import Prompt

server = MCPServerHTTP(url='http://127.0.0.1:8000/sse')

model_name = 'gpt-4o-mini'

client = AsyncAzureOpenAI()
model = OpenAIModel(model_name, provider=OpenAIProvider(openai_client=client))
agent = Agent(model, mcp_servers=[server])

server.headers = {"client-id": "izzyacademy.msft"}

global_message = """
Hello AI Search Developer,
I am a helpful assistant and I can answer questions about Contoso Groceries - an online grocery service where shopping is a pleasure. 
I have access to the AI Search Index for Contoso Groceries and can help developers interact with the data and resources in the AI Search service.
Please let me know how I can help you. 
Ask me to show you what tools I have available to support your development efforts. If you forget the tools, please ask me again.

"""
prompt = """
How can I help you?"""

print(global_message)


async def main():
    async with agent.run_mcp_servers():

        while True:
            # Prompt the user for input
            # and send it to the agent for processing
            # Use rich prompt for better user experience
            question = Prompt.ask(prompt)
            result = await agent.run(question)
            print(result.output)

if __name__ == '__main__':
    import asyncio
    import sys
    asyncio.run(main())