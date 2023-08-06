<h1 align="center">Relative Luminance gradient and Dominant Color of Frames (RLGDCF) based Digital Video Fingerprinting</h2>


## Introduction

Relative Luminance gradient and Dominant Color of Frames (RLGDCF) based Digital Video Fingerprinting is ...

I'll explain the code in words here but later, for now just read the code. Sorry!

### Installation

```bash
pip install videofingerprint -U
```

### Usage

```python
>>> import videofingerprint
>>> 
>>> url1 = "https://www.youtube.com/watch?v=PapBjpzRhnA"
>>> url2 = "https://raw.githubusercontent.com/akamhy/videohash/main/assets/rocket.mkv"
>>> 
>>> vp1 = videofingerprint.VideoFingerprint(url=url1)
>>> vp2 = videofingerprint.VideoFingerprint(url=url2)
>>> vp1.fingerprint
'rrbBbbBLlrrRrRrnNBbbbnnrBBbbBLlrrrRRnnnnLLLLLllllllllL'
>>> vp2.fingerprint
'rrbBbbBLlrrRrRrrNBbbbnnrBBbbBLlrrrRRnnNnBLLLLllllllllL'
>>> 
```


### 🛡 License

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/akamhy/videofingerprint/blob/main/LICENSE)

Copyright (c) 2022 Akash Mahanty. See
[license](https://github.com/akamhy/videofingerprint/blob/master/LICENSE) for details.




