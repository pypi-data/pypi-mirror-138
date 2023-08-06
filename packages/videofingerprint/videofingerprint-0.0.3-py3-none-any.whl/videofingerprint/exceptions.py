class FramesExtractorOutPutDirDoesNotExist(Exception):
    """The frames output directory passed to the frame extractor does not exist."""


class FFmpegError(Exception):
    """Base error for the FFmpeg software."""


class FFmpegNotFound(FFmpegError):
    """FFmpeg is either not installed or not in the executable path of the system."""


class FFmpegFailedToExtractFrames(FFmpegError):
    """FFmpeg failed to extract any frame at all. Maybe the input video is damaged or corrupt."""


class DownloadOutPutDirDoesNotExist(Exception):
    """Download output directory does not exist"""


class DownloadFailed(Exception):
    """Download failed"""
