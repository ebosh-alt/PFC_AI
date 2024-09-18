import logging

from services.OpenAI.Base import BaseClient

logger = logging.getLogger(__name__)


class Client(BaseClient):
    async def analysis(self, path_file, vector_store_id, thread_id, user_id=None):
        with open(path_file, "rb") as f:
            vector_store_id = await self._update_expired_vector_store(vector_store_id=vector_store_id, user_id=user_id)
            self._del_copy_file(path_file=path_file, vector_store_id=vector_store_id)
            file = self._upload_file(f)
            self._create_vector_store_file(vector_store_id=vector_store_id,
                                           file_id=file.id)
            self._create_message(thread_id=thread_id,
                                 content="Проанализируй фото",
                                 file_id=file.id)
        return await self.__answer(thread_id, user_id)

    async def question(self, content, thread_id=None, user_id=None):
        self._create_message(thread_id=thread_id,
                             content=content)
        return await self.__answer(thread_id, user_id)

    async def __answer(self, thread_id, user_id):
        run = await self._create_run(thread_id, user_id)
        if type(run) is str:
            return run
        messages = self._list_message(thread_id)
        text = self._get_text(messages, run.id)
        return text

    async def analysis_image(self, path_file) -> str:
        response = await self._analysis_image(path_file)
        answer = response["choices"][0]["message"]["content"]
        return answer

    def create_vector_store(self, user_id):
        return self._create_vector_store(user_id)

    def create_thread(self):
        return self._create_thread()

    def list_files(self):
        return self._list_files()

    def create_assistant(self):
        return self._create_assistant()
