# IMGdown

`IMGdown` is for reducing the pixel dimensions of an image. The interpolation algorithms used in this class are for making images smaller, and not larger. 

In my experience, downscaling is an especially [lossy process](lossless-lossy.md). The only reason I use downscaling is to produce thumbnails and deliberately low-res images for product listings - an anti-scraping tactic. 

## The Algorithms

`IMGdown` uses the LANCZOS (1) algorithm by default. Use the `--algo` flag with the numeric ID to change algorithms. 

```
0 = NEAREST
1 = LANCZOS (best, default)
2 = BILINEAR
3 = BICUBIC
4 = BOX
5 = HAMMING
```

## Width, Height, or Both

To downscale an image, you must supply either a `--width` or a `--height` or both.

* If given just a width or height, images will scale to that dimension.
* If given both width and height, images will scale to fit both dimensions. Meaning one dimension will equal its max and the other dimension will be equal to or smaller than its max. 
* Note this is different than scaling based on portrait or landscape. 

## ZLIB Compression

By default, when an image is downscaled or copied, it is also [compressed with Zlib](zlib.md). Use the `--zlib 0` option to disable compression. 

## Copied Images

If an image is already smaller than the downsize dimensions, it is optionally compressed with Zlib and copied to the save directory. This makes for a much better workflow. 

## Tech Notes

These notes are specific to Pillows's `resize()` method for **downscaling** images - and not enlarging. 

* All resample filters use a high quality convolutions-based algorithm with antialias.
* Broadly, the better the algorithm, the longer the processing time. 
* Broadly, the better the algorithm, the larger the resulting file. 
* Older method: De-gamma. Scale down by 2x until next scale would be smaller than target. Finish scaling down with BILINEAR. Re-gamma. According to [Pillow](https://pillow.readthedocs.io/en/stable/releasenotes/2.7.0.html?highlight=filters#bicubic-and-bilinear-downscaling), this multi-step process isn't necessary.

```
new_image = image.resize((width, height), resample=1)
new_image = image.resize((width, height), Image.LANCZOS)

resample=1 or Image.LANCZOS   # Highest visual quality
resample=3 or Image.BICUBIC   # Similar quality to NEAREST, but worse performance
resample=5 or Image.HAMMING   # Same performance as BILINEAR with a quality similar to BICUBIC
resample=2 or Image.BILINEAR  # Similar quality to NEAREST, but worse performance
resample=4 or Image.BOX       # High performance. Shorter window + sharper result than BILINEAR
resample=0 or Image.NEAREST   # Lowest visual quality
```

## Resources

* https://pillow.readthedocs.io/en/stable/handbook/concepts.html#filters
* https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Resampling
* https://pillow.readthedocs.io/en/stable/releasenotes/3.4.0.html#new-resizing-filters
* [Cambridge in Color: Image Interpolation](https://www.cambridgeincolour.com/tutorials/image-interpolation.htm)
* [Cambridge in Color: Image Resizing for the Web](https://www.cambridgeincolour.com/tutorials/image-resize-for-web.htm)
* fxguide: [Keeping Your Renders Clean](https://www.cambridgeincolour.com/tutorials/image-resize-for-web.htm)
* ImageMagick v6 Examples: [Resampling Filters](https://legacy.imagemagick.org/Usage/filter/)

