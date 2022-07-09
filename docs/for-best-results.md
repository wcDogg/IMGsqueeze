# For Best Results

I wrote IMGsqueeze with two opposing tasks in mind:

* To reduce file size while maintaining high visual quality.
* To produce intentionally low-res images for things like product listings (anti-scraping tactic). 

The goal is to strike some balance of file size and visual quality that's suitable for a given purpose. For best results, set clear goals and experiment - which PNGSqueeze makes easy to do. 

## Lossless vs Lossy

In very broad, layman terms:

* A lossless process means an image retains all of its visual data. Zlib compression is lossless - it organizes data into more efficient structures. 
* A lossy process means data is removed and the image looses some amount of detail. Downscaling is an especially lossy process - it maps more pixels to less pixels. Quantize maps more colors to less colors. 

## Group Visually Similar Images

A given process & settings can have very different effects depending on the image - say a photo vs simple geometric art. For best results, group visually similar images into their own directories. Think:

* Level of detail
* Number of colors
* Use of gradients
* Line and edge qualities ...

## Effect on File Size

For file size, the key things to know are: 

* Any process can result in a larger file size - which defeats some reasons for processing. This is especially true with downscaling.  
* A process can reduce file size, but the decrease may not justify the effort or loss of visual quality. Again, this is especially true with downscaling.
* To reduce file size without loss of quality, try [ZLIB compression](zlib.md) first. 

## Effect on Visual Quality

When it comes to evaluating visual quality, the best advice is:

* View images at the size & distance users will see them at. Avoid viewing images too large or zooming in - you'll get stuck on details that don't matter. 
* View images against a background that's similar to what users will see - you'd be amazed at the difference a light vs dark background can make. 
* Don't get hung up on which algorithm is best - if the image looks the way you want and the file size is acceptable, it's all good. 

## `configure.py`

`configure.py` contains the defaults used by each tool. While you probably don't need to edit this file, there are times when it can be helpful.

First is if you find you're constantly using options to change the defaults. 

Second is to change the `MAX_MB` or `MAX_PX` to process. These are set quite high as I often work with large file sizes and dimensions. 

`MAX_MB` relates to your computer's abilities. You may want to lower this if you have large files you need to skip. 

 `MAX_PX` replaces Pillow's baked-in decompression bomb warning. It's an image's width * height in pixels. You may want to lower this to a value more appropriate to the size images you work with. 

