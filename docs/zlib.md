# IMGzlib

[Zlib](https://zlib.net) is a widely used, [lossless](for-best-results.md/#lossless-vs-lossy) file compression library. File size is reduced by representing data in a more efficient format, without changing the actual data.

Zlib compression is always a good step in preparing images. Zlib usually reduces file size - though by how much varies widely.

## Usage

```
py IMGzlib.py --help

# Default max 9 zlib
py IMGzlib.py "D:\CornDoggSoup\IMGsqueeze\test-images\jpeg"

# Options
py IMGzlib.py --zlib 7 "D:\CornDoggSoup\IMGsqueeze\test-images\jpeg" 
```

## Compression Levels

Zlib compression is expressed as levels 0 (none) to 9 (max). All IMGsqueeze tools use Zlib 9 by default. Use the `--zlib` option to change or disable Zlib. Based on experience: 

* 9 = A bit longer to process, but can more than double MBs saved
* 6 = Lowest effective level
* 5 = Little if any compression
* 4, 3, 2 = File size starts to increase rather than decrease
* 0 = No compression

## File Formats

While all IMGsqueeze tools run on JPEG, PNG, and TIFF:

* PNG tends to benefit the most from Zlib compression and often take the longest to process.
* JPEG results vary widely, but are super fast to process. 
* TIFF doesn't compress using Zlib - it requires ZIP or or LZW. 

## Resources

* https://en.wikipedia.org/wiki/Zlib
* https://zlib.net/

