# rawpipe

[![Build Status](https://travis-ci.com/toaarnio/rawpipe.svg?branch=master)](https://travis-ci.com/github/toaarnio/rawpipe)

A collection of reference ISP algorithms, sufficient for producing a reasonably
good looking image from raw sensor data. Each algorithm takes in a frame in RGB
or raw format and returns a modified copy of the frame. The frame is expected to
be a NumPy float array with either 2 or 3 dimensions, depending on the function.
Some of the algorithms can be applied in different orders (demosaicing before or
after linearization, for example), but the reference ordering is as shown below.

**Example:**
```
import rawpipe
...
raw = rawpipe.downsample(raw, iterations=2)
raw = rawpipe.linearize(raw, blacklevel=64, whitelevel=1023)
rgb = rawpipe.wb(rgb, [1.5, 2.0], "RGGB")
rgb = rawpipe.demosaic(raw, "RGGB")
rgb = rawpipe.lsc(rgb, my_vignetting_map)
rgb = rawpipe.lsc(rgb, my_color_shading_map)
rgb = rawpipe.resize(rgb, 400, 300)
rgb = rawpipe.ccm(rgb, my_3x3_color_matrix)
rgb = rawpipe.gamut(rgb, "ACES")
rgb = rawpipe.tonemap(rgb, "Reinhard")
rgb = rawpipe.chroma_denoise(rgb)
rgb = pipe.saturate(rgb, lambda x: x ** 0.75)
rgb = rawpipe.gamma(rgb, "sRGB")
rgb = rawpipe.quantize8(rgb)
```

**Installing on Linux:**
```
pip install rawpipe
```

**Documentation:**
```
pydoc rawpipe
```

**Building & installing from source:**
```
make install
```

**Building & releasing to PyPI:**
```
make release
```
