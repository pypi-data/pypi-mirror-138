import os.path

from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), "README.md"), encoding="utf-8") as f:
    long_description = f.read()

about = {}
with open(
    os.path.join(os.path.dirname(__file__), "videofingerprint", "__version__.py")
) as f:
    exec(f.read(), about)

version = str(about["__version__"])

download_url = f"https://github.com/akamhy/videofingerprint/archive/{version}.tar.gz"

setup(
    name=about["__title__"],
    packages=["videofingerprint"],
    version=version,
    description=about["__description__"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    license=about["__license__"],
    author=about["__author__"],
    author_email=about["__author_email__"],
    url=about["__url__"],
    download_url=download_url,
    keywords=[
        "Digital video fingerprinting",
        "videofingerprint",
        "duplicate video detection",
        "RLGDCF",
        "find duplicate video",
        "compare videos",
        "video",
        "video diff",
        "Relative Luminance gradient",
        "Dominant Color of Frames",
    ],
    install_requires=["Pillow", "yt-dlp"],
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Information Technology",
        "Topic :: Multimedia :: Video",
        "Natural Language :: English",
        "Topic :: Scientific/Engineering :: Image Recognition",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    project_urls={
        "Source": "https://github.com/akamhy/videofingerprint",
        "Tracker": "https://github.com/akamhy/videofingerprint/issues",
    },
)
