import logging
from typing_extensions import override
from openai import AsyncAssistantEventHandler
from tools.crypto import *

# Configure logging
logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# https://platform.openai.com/docs/assistants/overview?context=with-streaming
# https://github.com/openai/openai-python/blob/54a5911f5215148a0bdeb10e2bcfb84f635a75b9/src/openai/lib/streaming/_assistants.py#L459
class EventHandler(AsyncAssistantEventHandler):
    @override
    async def on_text_created(self, text) -> None:
        print(f"\nAgent > ", end="")

    @override
    async def on_text_delta(self, delta, snapshot):
        print(delta.value, end="")

    # https://platform.openai.com/docs/assistants/tools/file-search/step-5-create-a-run-and-check-the-output
    @override
    async def on_message_done(self, message) -> None:
        # logger.info a citation to the file searched
        message_content = message.content[0].text
        annotations = message_content.annotations
        citations = []
        for index, annotation in enumerate(annotations):
            message_content.value = message_content.value.replace(
                annotation.text, f"[{index}]"
            )
            """
            if file_citation := getattr(annotation, "file_citation", None):
                cited_file = client.files.retrieve(file_citation.file_id)
                citations.append(f"[{index}] {cited_file.filename}")
            """

        logger.info(message_content.value)
        logger.info("\n".join(citations))
        print("\n")

    @override
    async def on_tool_call_created(self, tool_call):
        logger.info(f"\ntool call > {tool_call}\n")
        return

    @override
    async def on_tool_call_done(self, tool_call):
        logger.info(f"\ntool call done > {tool_call}\n")

    @override
    async def on_tool_call_delta(self, delta, snapshot):
        if delta.type == "code_interpreter":
            if delta.code_interpreter.input:
                logger.info(delta.code_interpreter.input)
            if delta.code_interpreter.outputs:
                logger.info(f"\n\noutput >")
                for output in delta.code_interpreter.outputs:
                    if output.type == "logs":
                        logger.info(f"\n{output.logs}")

        elif delta.type == "get_coin_price":
            if delta.get_coin_price.input:
                logger.info(delta.get_coin_price.input)
            if delta.get_coin_price.outputs:
                logger.info(f"\n\noutput >")
                for output in delta.get_coin_price.outputs:
                    if output.type == "logs":
                        logger.info(f"\n{output.logs}")
