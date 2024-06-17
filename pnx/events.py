import logging
from typing_extensions import override
from openai import AsyncAssistantEventHandler
from tools import *

# Configure logging
logging.basicConfig(
    level=logging.WARNING, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# https://platform.openai.com/docs/assistants/overview?context=with-streaming
# https://github.com/openai/openai-python/blob/54a5911f5215148a0bdeb10e2bcfb84f635a75b9/src/openai/lib/streaming/_assistants.py#L459
class AsyncEventHandler(AsyncAssistantEventHandler):
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

    @override
    async def on_tool_call_done(self, tool_call):
        logger.info(f"\ntool call done > {tool_call}\n")
