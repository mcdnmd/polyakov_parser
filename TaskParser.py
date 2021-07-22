import os
import re
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


from Task import TaskBasic


class TaskParser:
    URL = 'https://kpolyakov.spb.ru/school/ege/gen.php?action=viewTopic&topicId='
    IMG_URL = 'https://kpolyakov.spb.ru/cms/images/'
    FILE_URL = 'https://kpolyakov.spb.ru/cms/files/ege-stream/'

    BASE_DIR = os.path.dirname(__file__)

    def __init__(self):
        self.task_pattern = re.compile("changeImageFilePath\('(.*?)'\)")
        self.img_pattern = re.compile('<img src=\"(.*?)\"/>')
        self.file_pattern = re.compile('<a href=\"ege-stream/(.*?)\">')

    def parse(self, task_number: int) -> TaskBasic:
        with requests.get(f'{self.URL}{task_number}') as response:
            dir_name = os.path.join(self.BASE_DIR, str(task_number))
            os.makedirs(dir_name, exist_ok=True)

            content = response.text
        soup = BeautifulSoup(content, 'lxml')
        main_div = soup.find_all('div', {'class': 'center'})

        text = str(main_div[0])

        task = TaskBasic(task_number)
        task.text = self.get_task(text)
        task.ans = self.get_ans(text, task_number)
        task.images = self.get_image_name(text)
        task.files = self.get_files_names(text)
        task.dir_name = dir_name
        self.download_full_task_info(task)
        return task

    def download_full_task_info(self, task: TaskBasic):
        with open(os.path.join(task.dir_name, f'{task.id}.html'), 'w', encoding='utf-8') as f:
            f.write(f'{task.text}\n{task.ans}')

        if len(task.images) > 0:
            self.download_images(task.dir_name, task.images)

        if len(task.files) > 0:
            self.download_files(task.dir_name, task.files)

    def download_images(self, dir_name: str, images: list):
        for img in images:
            with requests.get(urljoin(self.IMG_URL, img)) as r:
                with open(os.path.join(dir_name, f'{img}'), 'wb') as f:
                    f.write(r.content)

    def download_files(self, dir_name: str, files: list):
        for file in files:
            with requests.get(urljoin(self.FILE_URL, file)) as r:
                filename = os.path.join(dir_name, f'{file.split("/")[-1]}')
                with open(filename, 'wb') as f:
                    f.write(r.content)

    def get_task(self, text: str):
        result = self.task_pattern.findall(text)
        return result[0]

    def get_ans(self, text: str, id: int):
        # TODO: Избавиться от создания патерна при повторном парсинге!
        PATTERN_ANS = f'class=\"hidedata\" id=\"{id}\">(.*)</div>'
        result = re.findall(PATTERN_ANS, text)
        return result[0]

    def get_image_name(self, text: str):
        result = self.img_pattern.findall(text)
        return result

    def get_files_names(self, text: str):
        result = self.file_pattern.findall(text)
        return result
