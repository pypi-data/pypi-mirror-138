
"""
	# Zdoom Textures Writer (zdtw)
"""

__version__ = "1.0"
__author__ = "GianptDev"
__date__ = '14-2-2022'	# Revisioned.

# will not include default properties in PatchData and TextureData, output will become smaller.
compact_mode = True

# ----------------------------------------

class PatchData():
	
	"""
		Patch information for a patch element.
		Is used inside TextureData, but it can work indipendently.
	"""

	# ----------------------------------------

	# List of style types.
	STYLE_TYPE = [
		"add",
		"copy",
		"copyalpha",
		"copynewalpha",
		"modulate",
		"overlay",
		"reversesubtract",
		"subtract",
		"translucent",
	]

	# all possible rotates, i really whish the engine could use an actual rotation.
	ROTATE_TYPE = [
		0,
		90,
		180,
		270,
	]

	# blend mode definition in Textures is bullshit, just use one of these in blend_mode
	BLEND_NONE = 0
	BLEND_COLOR = 1
	BLEND_TINT = 2
	BLEND_TRANSLATION = 3
	
	# ----------------------------------------
	
	# all the properties of a single patch.
	# to change the blend to use, set blend_mode to one of the BLEND_ values.
	def __init__(self, path = "", positionX = 0, positionY = 0,
		flipX = False, flipY = False, use_offsets = False,
		style = "copy", rotate = 0, alpha = 1.0,
		blend_mode = BLEND_NONE, blend = (255,255,255), tint = 255, translation = ""
	) -> None:
		self.path = str(path)
		self.positionX = int(positionX)
		self.positionY = int(positionY)
		
		self.flipX = bool(flipX)
		self.flipY = bool(flipY)
		self.use_offsets = bool(use_offsets)
		
		self.style = str(style)
		self.rotate = int(rotate)
		self.alpha = float(alpha)
		
		self.blend_mode = int(blend_mode)
		self.blend = blend	# r,g,b
		self.tint = int(tint)
		self.translation = str(translation)
	
	def __repr__(self) -> str:
		return "PatchData[ \"" + str(self.path) + "\" ]"
	
	# ----------------------------------------
	
	# write the patch block and return it as a string, on problems it will print some messages but will continue whit execution.
	#	newline -> specifcy a string to use for new lines.
	#	tab -> specify a string to use as tabulation.
	def write(self, newline = "\n", tab = "\t") -> str:
		result = ""
		props = ""

		# ----------------------------------------

		if (not self.style.lower() in self.STYLE_TYPE):
			print(
				"Inside the patch \" " + str(self.path) + " \":\n" +
				" - The style \" " + str(self.style) + " \" is unknow.\n" +
				"   Possible values are: " + str(self.STYLE_TYPE)
			)
			return ""

		if (not int(self.rotate) in self.ROTATE_TYPE):
			print(
				"Inside the patch \" " + str(self.path) + " \":\n" +
				" - The rotate \" " + str(self.rotate) + " \" is unknow.\n" +
				"   Possible values are: " + str(self.ROTATE_TYPE)
			)
			return ""

		if ((self.blend_mode < self.BLEND_NONE) or (self.blend_mode > self.BLEND_TRANSLATION)):
			print(
				"Inside the patch \" " + str(self.path) + " \":\n" +
				" - The blend mode \" " + str(self.blend_mode) + " \" is unknow, please see BLEND_ values."
			)

		# ----------------------------------------

		# start of patch definition
		result += "patch \"" + str(self.path) + "\", " + str(int(self.positionX)) + ", " + str(int(self.positionY))
		
		# flags
		if (self.use_offsets == True):
			props += tab + "UseOffsets" + newline
		if (self.flipX == True):
			props += tab + "flipX" + newline
		if (self.flipY == True):
			props += tab + "flipY" + newline

		# properties
		if ((compact_mode == False) or (compact_mode == True) and (self.style != "copy")):
			props += tab + "style " + str(self.style) + newline
		if ((compact_mode == False) or (compact_mode == True) and (self.rotate != 0)):
			props += tab + "rotate " + str(self.rotate) + newline
		if ((compact_mode == False) or (compact_mode == True) and (self.alpha != 1.0)):
			props += tab + "alpha " + str(self.alpha) + newline

		# color blend and tint work the same way.
		if ((self.blend_mode == self.BLEND_COLOR) or (self.blend_mode == self.BLEND_TINT)):
			props += tab + "blend "
			
			# check if is a iterable type
			if ((type(self.blend) is tuple) or (type(self.blend) is list)):
				
				if (len(self.blend) < 3):
					print(
						"Inside the patch \" " + str(self.path) + " \":\n" +
						" - The blend property require at least 3 (r,g,b) values."
					)
				
				# if is a iterable type add all his value (even if only 3 are required...)
				for b in self.blend:
					props += str(b) + ", "
				
				props = props[:-2] # remove last ", "
			
			# if is a string it can be used as a hex color, nothing will check if is valid.
			elif (type(self.blend) is str):
				
				# add the quotes and the # if missing (slade automatically add it but gzdoom does not required it, so i'm not sure....)
				props += "\"" + ("#" if (self.blend[0] != "#") else "") + str(self.blend).upper() + "\""
			
			# add the tint argoument
			if (self.blend_mode == self.BLEND_TINT):
				props += ", " + str(self.tint)
			
			props += newline
		
		# color translation is just a string tk add
		elif (self.blend_mode == self.BLEND_TRANSLATION):
			props += tab + "blend \"" + str(self.translation) + "\"" + newline
		
		# add property shit only if property do actually exist.
		if (props != ""):
			result += newline + "{" + newline + props + "}" + newline

		# ----------------------------------------
		
		return result

	# ----------------------------------------
	
	# to do
	#def read(self,data) -> bool:
		#return False
	
	# ----------------------------------------

# ----------------------------------------

class TextureData():
	
	"""
		This class contain all the information about a texture definition.
		The result of write can be directly used as valid textures data.
	"""

	# ----------------------------------------

	# list of know textures types.
	TEXTURE_TYPE = [
		"sprite",
		"texture",
		"flat",
		"graphic",
		"walltexture",
	]
	
	# ----------------------------------------
	
	def __init__(self, name = "", type = "texture", sizeX = 64, sizeY = 128,
		optional = False, world_panning = False, no_decals = False, null_texture = False,
		offsetX = 0, offsetY = 0, scaleX = 1.0, scaleY = 1.0
	) -> None:
		self.name = str(name)
		self.type = str(type)
		self.sizeX = int(sizeX)
		self.sizeY = int(sizeY)
		self.offsetX = int(offsetX)
		self.offsetY = int(offsetY)
		self.scaleX = float(scaleX)
		self.scaleY = float(scaleY)
		
		self.optional = bool(optional)
		self.world_panning = bool(world_panning)
		self.no_decals = bool(no_decals)
		self.null_texture = bool(null_texture)

		self.patches = []	# This is the list of all patches inside this texture block

	def __repr__(self) -> str:
		return "<TextureData[ \"" + str(self.name) + "\" ]>"

	# ----------------------------------------

	# add a patch in the list of patches, but only if is a valid PatchData
	def add_patch(self, patch) -> None:
		
		if (not type(patch) is PatchData):
			print(
				"Inside the texture \" " + str(self.name) + " \":\n" +
				" - Non-PatchData cannot be added, it may result in errors"
			)
			return
		
		self.patches.append(patch)
	
	# return all patches that uses the specific path name.
	def get_patches(self, path) -> list:
		patches = self.patches
		result = []

		for p in patches:
			if (p.path == path):
				result.append(p)

		return result

	# ----------------------------------------

	# write the texture block and return it as a string, the result can be directly used for a textures file.
	#	newline -> specify a string to use for new lines.
	#	tab -> specify a string to use as tabulation.
	def write(self, newline = "\n", tab = "\t") -> str:
		result = ""
		
		# ----------------------------------------

		if (not self.type.lower() in self.TEXTURE_TYPE):
			print(
				"Inside the texture \" " + str(self.name) + " \":\n" +
				" - The type \" " + str(type) + " \" is unknow.\n" +
				"   Possible values are: " + str(self.TEXTURE_TYPE)
			)
			return ""
		
		if (len(self.patches) <= 0):
			print(
				"Inside the texture \" " + str(self.name) + " \":\n" +
				" - No patch are used, the texture will be empty."
			)

		# ----------------------------------------

		# set the texture type
		result += self.type
		
		# add the optional flag first
		if (self.optional == True):
			result += " optional"
		
		# start of texture definition
		result += " \"" + str(self.name) + "\", " + str(int(self.sizeX)) + ", " + str(int(self.sizeY)) + newline + "{" + newline
		
		# flags
		if (self.world_panning == True):
			result += tab + "WorldPanning" + newline
		if (self.no_decals == True):
			result += tab + "NoDecals" + newline
		if (self.null_texture == True):
			result += tab + "NullTexture" + newline
		
		# properties
		if ((compact_mode == False) or (compact_mode == True) and ((self.offsetX != 0) or (self.offsetY != 0))):
			result += tab + "offset " + str(int(self.offsetX)) + ", " + str(int(self.offsetY)) + newline
		if ((compact_mode == False) or (compact_mode == True) and (self.scaleX != 1.0)):
			result += tab + "Xscale " + str(float(self.scaleX)) + newline
		if ((compact_mode == False) or (compact_mode == True) and (self.scaleY != 1.0)):
			result += tab + "Yscale " + str(float(self.scaleY)) + newline
		
		# add each patch to the result and make sure to tabulate.
		for p in self.patches:
			b = p.write(newline,tab)
			
			# fix extra newline
			if (b[-1] == newline):
				b = b[:-1]
			
			# do not execute work if the string is empty.
			if (b == ""):
				continue
			else:
				result += tab + b.replace(newline, newline + tab) + newline
		
		# end of patch definition
		result += "}" + newline
		
		return result

	# ----------------------------------------

# ----------------------------------------

# write a list of TextureData into a single string as a valid textures lump, does not write any file.
# invalid data is ignored and will show a message.
def write_textures(blocks, newline = "\n", tab = "\t") -> str:
	result = ""
	
	invalid_count = 0	# count invalid data
	clone_found = False	# true if a texture is defined twince or more
	clone_count = {}	# count every cloned definition

	# ----------------------------------------

	# loop to every data in the input
	for b in blocks:

		# check if data is valid
		if (not type(b) is TextureData):
			invalid_count += 1
			continue

		# check if a clone exist
		if (b.name in clone_count):
			clone_found = True
			clone_count[b.name] += 1
		else:
			clone_count[b.name] = 1

		# just write the block and merge whit the result
		result += b.write(newline,tab) + newline

	# ----------------------------------------

	# display the amount of invalid data
	if (invalid_count > 0):
		print(
			"While writing the lump of size " + str(len(blocks)) + ":\n" +
			" - The input contain " + str(invalid_count) + " invalid data,\n" +
			"   maybe non-TextureData or None are inside."
		)

	# display the amount of clones
	if (clone_found == True):
		print(
			"While writing the lump of size " + str(len(blocks)) + ":\n" +
			" - Some textures are defined more than once:"
		)

		# display each clone by the name and amount of clones
		for c in clone_count:
			
			if (clone_count[c] <= 1):
				continue
			
			print(
				" - - \"" + str(c) + "\" is defined " + str(clone_count[c]) + " times."
			)

	# ----------------------------------------

	return result

# parse an actual textures definition into TextureData and PatchData instances, will not load a file.
# the function work, but does not handle all errors yet, will receive changes in future versions.
#	load_textures, does nothing.
#	load_patches, if enabled will load patches data, if disabled patches are not loaded (resulting in empty textures).
def read_textures(parse, endline = "\n", tab = "\t", load_textures = True, load_patches = True) -> list:
	result = []

	# ----------------------------------------

	# parse from string become an array.
	parse = parse.split(endline)
	
	# remove garbage
	for d in range(len(parse)):
		parse[d] = parse[d].replace(tab,"")
		parse[d] = parse[d].replace(",","")
	
	# clear useless stuff
	for d in range(len(parse)):
		if (d >= len(parse)):
			break
		
		if (parse[d] == ""):
			del parse[d]
		elif (parse[d] == "}"):
			parse[d] = None
		elif (parse[d] == "{"):
			del parse[d]
	
	# start to instance stuff
	current_patch = None
	current_texture = None
	for d in range(len(parse)):
		info = parse[d]
		
		if (info == None):
			
			if (current_patch != None):
				current_patch = None
				continue
			
			if (current_texture != None):
				current_texture = None
				continue
			
			# error to add
			print("what the? } used twince?")
			return []
		
		# this is all the info when need to read the textures lump!
		info = info.split(" ")
		
		# stuff to load a texture
		if (info[0] in TextureData.TEXTURE_TYPE):
			
			if (current_texture != None):
				print("what the? texture defined twince?")
				return []
			
			if (len(info) < 4):
				print("what the? not enough texture informations?")
				return []
			
			is_optional = False
			if (info[1].lower() == "optional"):
				is_optional = True
				del info[1]
			
			# remove quotes if they exist.
			if (info[1][0] == "\""):
				info[1] = info[1][1:]
			if (info[1][-1] == "\""):
				info[1] = info[1][:-1]
			
			current_texture = TextureData()
			current_texture.type = info[0]
			current_texture.name = info[1]
			current_texture.sizeX = float(info[2])
			current_texture.sizeY = float(info[3])
			current_texture.optional = is_optional
			
			result.append(current_texture)
		
		# stuff to load a patch
		if ((load_patches == True) and (info[0].lower() == "patch")):
			
			if (current_texture == None):
				print("what the? patch connected to nothing?")
				return []
			
			if (current_patch != None):
				print("what the? patch defined twince?")
				return []
			
			if (len(info) < 4):
				print("what the? not enough patch informations?")
				return []
			
			# remove quotes if they exist.
			if (info[1][0] == "\""):
				info[1] = info[1][1:]
			if (info[1][-1] == "\""):
				info[1] = info[1][:-1]
			
			current_patch = PatchData()
			current_patch.type = info[0]
			current_patch.path = info[1]
			current_patch.positionX = float(info[2])
			current_patch.positionY = float(info[3])
			
			current_texture.add_patch(current_patch)
		
		if (current_patch != None):
			p = info[0].lower()
			
			# properties
			if (len(info) >= 2):
				
				if (p == "style"):
					current_patch.style = info[1]
				elif (p == "rotate"):
					current_patch.rotate = int(info[1])
				elif (p == "alpha"):
					current_patch.alpha = float(info[1])
				elif (p == "blend"):
				
					# todo: blend mode is detected like shit
				
					if (len(info) >= 4):
						current_patch.blend = (int(info[1]),int(info[2]),int(info[3]))
						if (len(info) >= 5):
							current_patch.tint = int(info[4])
							current_patch.blend_mode = current_patch.BLEND_TINT
						else:
							current_patch.blend_mode = current_patch.BLEND_COLOR
				
					elif (len(info) >= 2):
						current_patch.blend = info[1]
						current_patch.translation = info[1] # yeah...
						if (len(info) >= 3):
							current_patch.tint = int(info[2])
							current_patch.blend_mode = current_patch.BLEND_TINT
						else:
							current_patch.blend_mode = current_patch.BLEND_COLOR
				
					else:
						print("what the? wrong blend data?")
			
			# flags
			else:
				if (p == "flipx"):
					current_patch.flipX = True
				elif (p == "flipy"):
					current_patch.flipY = True
				elif (p == "useoffsets"):
					current_patch.use_offsets = True
		
		if (current_texture != None):
			p = info[0].lower()
			
			# properties
			if (len(info) >= 2):
				if (p == "offset"):
					current_texture.offsetX = int(info[1])
					current_texture.offsetY = int(info[2])
				elif (p == "xscale"):
					current_texture.scaleX = float(info[1])
				elif (p == "yscale"):
					current_texture.scaleY = float(info[1])
			# flags
			else:
				if (p == "worldpanning"):
					current_texture.world_panning = True
				elif (p == "nodecals"):
					current_texture.no_decals = True
				elif (p == "nulltexture"):
					current_texture.null_texture = True
	
	# ----------------------------------------
	
	# return a beautiful amount of classes!
	return result

# ----------------------------------------

# Will convert a string into a valid sprite name, will add the frame character and angle by using a simple number.
# index is the range between A and Z, a greater number will wrap around and override the name.
# angle is the rotate of the sprite, 0 is no rotate and 1 to 8 are all rotate keys.
def to_sprite_name(name, index = 0, angle = 0) -> None:
	result = ""
	
	# get only 4 characters for the name, it will be used to wrap around.
	wrap = [ord(name[0]) - 65,ord(name[1]) - 65,ord(name[2]) - 65,ord(name[3]) - 65]
	base = 25 # from A to Z
	
	# convert to base 26
	while(True):
		
		# if the index is already under the limit, then no more shit is required.
		if (index >= base):
			index -= base
			
			# increase the next character every time the number is greater than the limit.
			for i in range(len(wrap)):
				i = len(wrap) - (i + 1)
				if (wrap[i] >= base):
					wrap[i] = 0
				else:
					wrap[i] += 1
					break
		else:
			break

	# build the new name.
	name = ""
	for i in wrap:
		name += chr(65 + i)
	frame = chr(65 + index)

	# add the frame string to the name.
	result += name + frame

	# add the rotate index.
	if (angle == 0):
		result += "0"
	elif (angle == 1):
		result += "1"
	elif (angle == 2):
		result += frame + "8"
	elif (angle == 3):
		result += frame + "7"
	elif (angle == 4):
		result += frame + "6"
	elif (angle == 5):
		result += "5"
	elif (angle == 6):
		result += frame + "4"
	elif (angle == 7):
		result += frame + "3"
	elif (angle == 8):
		result += frame + "2"

	return result

# ----------------------------------------

# Exampes
if __name__ == '__main__':
	
	# load test
	#ims = read_textures(open("test.txt","r").read())
	#print(write_textures(ims))	
	#input()
	
	print("Zdoom Textures Parser examples:\n")

	empty = TextureData(type = "sprite",sizeX = 32, sizeY = 16)
	empty.name = to_sprite_name("PIST",0)

	wall = TextureData("WALLBRICK",type = "walltexture", optional = True, scaleY = 1.2)
	p = PatchData("textures/brick.png")
	wall.add_patch(p)

	more_patches = TextureData("WALLSTONE","walltexture",sizeX = 64, sizeY = 64)
	for i in [
		PatchData("textures/stone1.png", flipX = True, rotate = 90),
		PatchData("textures/stone2.png",positionX = 32, blend_mode = PatchData.BLEND_TINT, blend = "ff0000"),
	]: more_patches.add_patch(i)

	print("Empty texture example:")
	print(empty.write())

	print("Texture whit a single patch:")
	print(wall.write())

	print("Texture whit more patches:")
	print(more_patches.write())
	
	# spam test
	#for i in range(26 ** 4):
	#	c = to_sprite_name("AAAA",i)
	#	print(c)
	
	# write test
	#print(write_textures([empty]))
	#open("test.txt","w").write(write_textures([more_patches,wall]))
