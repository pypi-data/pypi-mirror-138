import os
import random
import re
import shutil
from pathlib import Path
from typing import List

from imagedominantcolor import DominantColor
from PIL import Image

from .downloader import Download
from .framesextractor import FramesExtractor
from .utils import (
    create_and_return_temporary_directory,
    does_path_exists,
    get_list_of_all_files_in_dir,
)
from .videoduration import video_duration as videoduration


class VideoFingerprint:
    """
    Relative Luminance gradient and Dominant Color of Frames (RLGDCF)
    based Digital Video Fingerprinting
    """

    storage_path = None
    download_worst = False
    dominant_color = DominantColor
    dominant_color.resize_value = 16
    dominant_color.minimum_percent_difference_of_rgb = 10
    previous_color = 0

    def __init__(self, path=None, url=None):
        self.path = path
        self.url = url
        self.fingerprint = ""
        self.luminance_fingerprint = ""
        self.chrominance_fingerprint = ""
        self.video_path: str = ""
        self.task_uid = VideoFingerprint.get_task_uid()
        self.create_required_dirs_and_check_for_errors()
        self.copy_video_to_video_dir()
        FramesExtractor(self.video_path, self.frames_dir)
        self.frames = get_list_of_all_files_in_dir(self.frames_dir)
        self.generate_fingerprint()

    @property
    def video_duration():
        return videoduration(self.video_path)

    def copy_video_to_video_dir(self):

        if self.path:
            # create a copy of the video at self.storage_path
            match = re.search(r"\.([^.]+$)", self.path)

            if match:
                extension = match.group(1)

            else:
                raise ValueError("File name (path) does not have an extension.")

            self.video_path = os.path.join(self.video_dir, (f"video.{extension}"))

            shutil.copyfile(self.path, self.video_path)

        if self.url:

            Download(
                self.url,
                self.video_download_dir,
                worst=self.download_worst,
            )

            downloaded_file = get_list_of_all_files_in_dir(self.video_download_dir)[0]
            match = re.search(r"\.(.*?)$", downloaded_file)

            extension = "mkv"

            if match:
                extension = match.group(1)

            self.video_path = f"{self.video_dir}video.{extension}"

            shutil.copyfile(downloaded_file, self.video_path)

    def create_required_dirs_and_check_for_errors(self) -> None:
        if not self.path and not self.url:
            raise DidNotSupplyPathOrUrl(
                "You must specify either a path or an URL of the video."
            )

        if self.path and self.url:
            raise ValueError("Specify either a path or an URL and NOT both.")

        if not VideoFingerprint.storage_path:
            VideoFingerprint.storage_path = create_and_return_temporary_directory()
        if not does_path_exists(VideoFingerprint.storage_path):
            raise StoragePathDoesNotExist(
                f"Storage path '{VideoFingerprint.storage_path}' does not exist."
            )

        os_path_sep = os.path.sep

        VideoFingerprint.storage_path = os.path.join(
            VideoFingerprint.storage_path, (f"{self.task_uid}{os_path_sep}")
        )

        self.video_dir = os.path.join(
            VideoFingerprint.storage_path, (f"video{os_path_sep}")
        )
        Path(self.video_dir).mkdir(parents=True, exist_ok=True)

        self.video_download_dir = os.path.join(
            VideoFingerprint.storage_path, (f"downloadedvideo{os_path_sep}")
        )
        Path(self.video_download_dir).mkdir(parents=True, exist_ok=True)

        self.frames_dir = os.path.join(
            VideoFingerprint.storage_path, (f"frames{os_path_sep}")
        )
        Path(self.frames_dir).mkdir(parents=True, exist_ok=True)

    def image_luminance(self, image_path, width=1, height=1):
        return list(
            Image.open(image_path)
            .convert("L")
            .resize((width, height), Image.ANTIALIAS)
            .getdata()
        )[0]

    def color_case(self, image_path):
        current_color = self.image_luminance(image_path)
        if VideoFingerprint.previous_color <= current_color:
            case = 0
        else:
            case = 1
        VideoFingerprint.previous_color = current_color
        return case

    def generate_fingerprint(self):

        for frame in self.frames:
            dc = VideoFingerprint.dominant_color(image_path=frame).dominant_color
            self.chrominance_fingerprint += dc
            case = self.color_case(frame)
            self.luminance_fingerprint += str(case)
            case_dc = dc.upper() if case == 1 else dc
            self.fingerprint += case_dc
        return self

    def get_task_uid() -> str:
        sys_random = random.SystemRandom()

        return "".join(
            sys_random.choice(
                "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
            )
            for _ in range(20)
        )
