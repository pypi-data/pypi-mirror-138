<h1 align="center">Relative Luminance gradient and Dominant Color of Frames (RLGDCF) based Digital Video Fingerprinting</h1>


## Introduction

Relative Luminance gradient and Dominant Color of Frames (RLGDCF) based Digital Video Fingerprinting is a novel but straightforward video fingerprinting technique that generates the fingerprint for any video by extracting one frame per second and reducing these frames to a single latin alphabet.

First, find the dominant color of the frame using the [imagedominantcolor](https://github.com/akamhy/imagedominantcolor) python package, it outputs one character out of r, g, b, l, and n whenever an image is passed to it.

Output dominant color and their meanings:

- r - Red is the dominant color in the image.
- g - Green is the dominant color for the image.
- b - Blue is the dominant color.
- l - It is lowercase L and it implies that the image is mostly grayscale. L for luminance and most of the image lacks color.
- n - None of the colors out of r, g, and b are dominant but the image is also not grayscale. It implies that the image has equal regions where 2 or 3 colors dominate, [for example here](https://user-images.githubusercontent.com/64683866/151845374-dd1a83e5-3265-491e-830d-39be120af65b.png).

Then calculate the luminance value of the frame and compare it with the luminance value of the frame preceding the current frame. As the first frame can not have a preceding frame we set its value to 0. For all the remaining frames, set their value to 0 if the current frame is brighter or at least equally bright when compared to the preeceding frame. If the preceding frame is brighter compared to the current frame then set the value of the current frame to 1.

If the number is 0, make the dominant color alphabet lowercase
and if the number is 1 then make the dominant color alphabet uppercase.

Examples:

- If the dominant color is r and the number is 1, then the character that should represent the frame should be R.

- If the dominant color value is n and the number is 0, then the character that should represent the frame should be n.


And remember that you don't have to stick to these original rules, you can flip them but just stay consistent and it's guaranteed that your implementation will work. Also, any other dominant color of the image detection library will do great as long as the output is deterministic.

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
[license](https://github.com/akamhy/videofingerprint/blob/main/LICENSE) for details.
