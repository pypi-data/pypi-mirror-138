"""
Relative Luminance gradient and Dominant Color of Frames (RLGDCF)
based Digital Video Fingerprinting
"""

from .__version__ import (
    __author__,
    __author_email__,
    __copyright__,
    __description__,
    __license__,
    __status__,
    __title__,
    __url__,
    __version__,
)
from .exceptions import (
    DownloadFailed,
    DownloadOutPutDirDoesNotExist,
    FFmpegError,
    FFmpegFailedToExtractFrames,
    FFmpegNotFound,
    FramesExtractorOutPutDirDoesNotExist,
)
from .rlgdcf_videofingerprint import VideoFingerprint
from .videoduration import video_duration
