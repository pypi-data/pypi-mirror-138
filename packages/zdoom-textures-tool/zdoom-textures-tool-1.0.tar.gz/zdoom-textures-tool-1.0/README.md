# Zdoom-TexturesWriter
Small tool to write a valid textures text file for the zdoom engine, inteded to be used for automated scripts.

## Installation
### pip
You can simply use the pip command

```pip install zd-textures-tool```

Then you can import in your script whit:

```import zd-textures-tool```

## Use
Here a small example, the script itself has some more examples inside of it.
```
import zdtwriter # zdoom-textures-writer

# Make a new texture block
wall = TextureData("WALLBRICK",type = "walltexture", optional = True, scaleY = 1.2)

# Make a path block
p = PatchData("textures/brick.png")

# Add the patch in the texture
wall.add_patch(p)

# Show on screen a texture block.
print(wall.write())
```

### manual
all of the code is inside of ```zdtwriter.py``` in the ```src``` folder, you can get the file and manually import it in your script.

## Content
The script define 2 classes, 3 functions, 1 global value and some example code.

### Classes
- PatchData
- - Contain all properties for a patch and can write a valid patch block.
- TextureData
- - Contain all properties of a texture block, patches can be added whit add_patch and can write a valid texture block.

### Methods
- write_textures(blocks)
- - Will write a list of TextureData into a single string, basically just execute a loop and handle errors.
- read_textures(parse)
- - Will read a string and parse into TextureData and TexturePatch, currently it work but can be improved.
- - If you want to read a file you need to use open() and read() first, this method require a string to parse, not a file path.
- to_sprite_name(name, index, rotation)
- - Will convert a string into a valid Sprite name, can be usefull for rotation sprites and sprites that uses more than 25 frames for animations. (later i will document more)

### Globals
- compact_mode = True
- - if enabled all default properties are ignored when writing patches and textures, the output can become smaller.
- - if disabled all default properties will be written.
