import asyncio
import logging

from aiogram.enums import ChatAction
from openai import OpenAI
from openai.pagination import SyncCursorPage
from openai.types.beta import CodeInterpreterToolParam
from openai.types.beta.threads import Run
from openai.types.beta.threads.message_create_params import Attachment
from openai.types.beta.vector_stores import VectorStoreFile

from data.config import OPENAI_API_KEY, ASSISTANT, bot
from entity.database import users

logger = logging.getLogger(__name__)


class BaseClient:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    def _create_thread(self):
        thread = self.client.beta.threads.create()
        return thread

    def _retrieve_thread(self, thread_id):
        thread = self.client.beta.threads.retrieve(thread_id)
        return thread

    def _create_vector_store(self, user_id):
        vector_store = self.client.beta.vector_stores.create(
            name=str(user_id)
        )
        return vector_store

    def _retrieve_vector_store(self, vector_store_id):
        vector_store = self.client.beta.vector_stores.retrieve(
            vector_store_id=vector_store_id
        )
        return vector_store

    async def _update_expired_vector_store(self, user_id, vector_store_id):
        try:
            vector = self._retrieve_vector_store(vector_store_id)
            vector_store_id = vector.id
            if vector.status == "expired":
                vector = self._create_vector_store(user_id)
                vector_store_id = vector.id
                user = await users.get(user_id)
                user.vector_store_id = vector_store_id
                await users.update(user)
        except Exception as ex:
            logger.info(ex)
            vector = self._create_vector_store(user_id)
            vector_store_id = vector.id
            user = await users.get(user_id)
            user.vector_store_id = vector_store_id
            await users.update(user)
        return vector_store_id

    def _create_vector_store_file(self, vector_store_id, file_id):

        vector_store_file = self.client.beta.vector_stores.files.create(
            vector_store_id=vector_store_id,
            file_id=file_id
        )

        self._update_vector_store(vector_store_id, file_id)
        return vector_store_file

    def _update_vector_store(self, vector_store_id, file_id=None):
        self.client.beta.assistants.update(
            assistant_id=ASSISTANT,
            tool_resources={"file_search": {"vector_store_ids": [vector_store_id]}},
        )
        if file_id:
            self.client.beta.assistants.update(
                assistant_id=ASSISTANT,
                tool_resources={"code_interpreter": {"file_ids": [file_id]}},
            )

    def _list_files_vector_store(self, vector_store_id) -> SyncCursorPage[VectorStoreFile]:
        vector_store_files = self.client.beta.vector_stores.files.list(
            vector_store_id=vector_store_id
        )
        logger.info(f"Listing vector store files: {vector_store_files}")

        return vector_store_files

    def _create_message(self, thread_id, content, file_id=None):
        if file_id:
            attachments = [Attachment(file_id=file_id, tools=[CodeInterpreterToolParam(type="code_interpreter")])]
        else:
            attachments = None
        message = self.client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=content,
            attachments=attachments
        )
        logger.info(f"Created message: {message.id}")
        return message

    def _list_message(self, thread_id):
        messages = self.client.beta.threads.messages.list(thread_id=thread_id,
                                                          order="desc")
        logger.info("Listing messages")
        return messages

    def _retrieve_message(self, thread_id, message_id):
        message = self.client.beta.threads.messages.retrieve(
            message_id=thread_id,
            thread_id=message_id,
        )
        return message

    async def _create_run(self, thread_id, user_id) -> Run | str:
        run = self.client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=ASSISTANT
        )
        logger.info(f"Created run: {run.id}")
        await self._retrieve_run(run, thread_id, user_id)
        return run

    async def _retrieve_run(self, run, thread_id, user_id=None) -> Run | str:
        while run.status != "completed":
            run = self.client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run.id
            )
            logger.info(f"Retrieved run: {run.id}, run status: {run.status}")
            if run.status == "incomplete" or run.status == "failed":
                return "Произошла ошибка. Попробуйте чуть позже"
            await asyncio.sleep(2)
            if user_id:
                await bot.send_chat_action(chat_id=user_id, action=ChatAction.TYPING, request_timeout=2)

        return run

    def _upload_file(self, file):
        file = self.client.files.create(
            file=file,
            purpose="assistants")
        logger.info(f"Uploaded file: {file.id}")
        return file

    def _list_files(self):
        files = self.client.files.list()
        return files

    def _delete_file(self, file_id, vector_store_id=None):
        self.client.files.delete(file_id)
        if vector_store_id:
            self.client.beta.vector_stores.files.delete(file_id=file_id,
                                                        vector_store_id=vector_store_id)
            self._update_vector_store(vector_store_id)

    def _del_all_files(self):
        files = self._list_files()
        for i in files:
            self._delete_file(i.id)

    @staticmethod
    def _get_text(messages, run_id):
        text = ""
        for message in messages:
            if message.run_id == run_id:
                text = message.content[0].text.value
        return text

    def _del_copy_file(self, path_file, vector_store_id=None):
        list_files = self._list_files()
        file_name = path_file.split("/")[-1]
        files_name = []
        for file in list_files:
            if file.filename == file_name:
                self._delete_file(file_id=file.id,
                                  vector_store_id=vector_store_id)
                logger.info(f"Deleted copy file - file_id: {file.id}, file_name: {file.filename}")
                continue
            files_name.append({"filename": file.filename, "file_id": file.id})
        logger.info(f"Uploaded files to the system: {files_name}")
