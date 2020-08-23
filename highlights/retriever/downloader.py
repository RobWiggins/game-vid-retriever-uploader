import requests
import logging
import os
from pathlib import Path


class Downloader:
    """
    Accepts urls or get responses, scrapes video downloads video files into folders.
    """

    def __init__(self):
        self.CHUNK_SIZE = 1024
        self.CONNECT_TIMEOUT = 5
        self.RETRY_COUNT = 5

    def download_video_from_url(self, url, path):
        """
        Downloads video to the specified directory and returns the size of the downloaded file.
        clear_dir_if_exists(dir), which clears the target folder if it already exists, should be called
        prior to invoking this function.
        """
        tmp_path = path + ".tmp"
        Path(tmp_path).touch()
        clip_res = requests.get(url, stream=True, timeout=self.CONNECT_TIMEOUT)
        print(clip_res)
        size = 0
        with open(tmp_path, 'wb') as target:
            for chunk in clip_res.iter_content(self.CHUNK_SIZE):
                target.write(chunk)
                size += len(chunk)
        print('finished downloading')
        return size

    def clear_dir_if_exists(self, dir):
        if not Path('./downloads').exists():
            Path('./downloads').mkdir()
        else:
            files = os.listdir('./downloads')
            for file in files:
                os.remove(f'./downloads/{file}')
