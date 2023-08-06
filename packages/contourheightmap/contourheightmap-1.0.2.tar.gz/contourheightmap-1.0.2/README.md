# Contour Heightmap

A fast python library for generating contour maps from heightmaps and images.

Given an image file (preferably RGB PNG), it will output a PNG with topographic contour lines 
and an SVG file of the contour lines. 

![Heightmap with contour lines](examples/heightmap_500x800.png "Contoured")
![Heightmap with contour lines](examples/heightmap_500x800_contour.png "Contoured")



![Heightmap with contour lines](examples/snowdon.png "Contoured")
![Heightmap with contour lines](examples/snowdon_contour.png "Contoured")


Questions? Contributions? Bug reports? Open an issue on the [gitlab page for the project](https://gitlab.com/dodgyville/contourheightmap).
We are very interested in hearing your use cases for `contourheightmap` to help drive the roadmap.

### Roadmap
* More control on the output image
* More control on the output svg

### Contributors
* Luke Miller

## Installing
```
pip install contourheightmap
```
or
```
py -m pip install contourheightmap
```

## Source

```
git clone https://gitlab.com/dodgyville/contourheightmap
```

# Quick Start

## How do I...

### contour an image?

```python
from contourheightmap import ContourHeightmap

c = ContourHeightmap()
c.contour("path/to/heightmap.png")
```

Result will be in output.png and output.svg


### provide an output filename?
```python
from contourheightmap import ContourHeightmap

c = ContourHeightmap()
c.contour("path/to/heightmap.png", "path/to/output.png")
```

Output will also be in path/to/output.svg

### output a contoured image from the command line?

```bash
contourheightmap.sh examples/heightmap.png 
```


