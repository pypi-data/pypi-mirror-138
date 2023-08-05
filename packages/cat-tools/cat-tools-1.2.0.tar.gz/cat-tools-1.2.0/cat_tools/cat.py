import traceback, lzma, io, struct, platform, os, time, zstandard, lzham
from PIL import Image 
class memory:
	def __init__(self, data):
		self.mem = io.BytesIO(data)
	def readBuffer(self, v):
		return self.mem.read(v)
	def readAll(self):
		return self.mem.read()
	def readInt(self):
		return struct.unpack('4B', self.mem.read(4))
	def readUInt(self, length=1):
		return int.from_bytes(self.mem.read(length), 'little')
	def readString(self):
		length = self.readInt() 
		if length < 0:
			return "" 
		else:
			return self.readBuffer(length).decode()
	def readPixel(self, r):
		if r in [0,1]:
			return self.readInt() 
		elif r == 2:
			p, = struct.unpack('<H', self.mem.read(2))
			return p
		elif r == 3:
			p, = struct.unpack('<H', self.mem.read(2))
			return ((p >> 11 & 31) << 3, (p >> 6 & 31) << 3, (p >> 1 & 31) << 3, (p & 255) << 7)
		elif r == 4:
			p, = struct.unpack("<H", self.mem.read(2))
		elif r == 6:
			return struct.unpack("2B", self.mem.read(2))[::-1]
		elif r == 10:
			return struct.unpack("B", self.mem.read(1))
	def free(self):
		self.mem.close()
def join_image(img, p):
    _w, _h = img.size
    imgl = img.load()
    x = 0
    a = 32
    _ha = _h // a
    _wa = _w // a
    ha = _h % a
    for l in range(_ha):
        for k in range(_w // a):
            for j in range(a):
                for h in range(a):
                    imgl[h + k * a, j + l * a] = p[x]
                    x += 1
        for j in range(a):
            for h in range(_w % a):
                imgl[h + (_w - _w % a), j + l * a] = p[x]
                x += 1
    for k in range(_wa):
        for j in range(_h % a):
            for h in range(a):
                imgl[h + k * a, j + (_h - _h % a)] = p[x]
                x += 1
    for j in range(ha):
        for h in range(_w % a):
            imgl[h + (_w - _w % a), j + (_h - _h % a)] = p[x]
            x += 1
def bytes2image(config):
	pixels = []
	info = config["info"]
	name = config["name"]
	pixels = config["pixels"]
	del config 
	print(f"[*] extracting {name} | size: {info[1]} | width: {info[3]} | height: {info[4]}")
	img_type = "RGBA"
	if info[2] in range(4):
	   img_type = 'RGBA'
	if info[2] in (4,):
	   img_type = 'RGB'
	if info[2] in (6,):
	   img_type = 'LA'
	if info[2] in (10,):
		img_type =  'L'
	base = Image.new(img_type, (info[3], info[4]))
	try:
		base.putdata(pixels)
	except:
		return False
	if info[0] in [27,28]:
		print(f"[*] joining {name}")
		try:
			join_image(base, pixels)
		except:
			print(f"[*] failed to join {name}")
	del pixels 
	del info
	print(f"[*] saving {name}")
	base.save(name)
	del name
	del base
	return True
class pycat:
	def decodeSC(file, use_disk=False):
		m = memory(b'')
		m.mem = open(file, "rb")
		temp = open(file, "rb")
		use_lzham = False
		if b"SCLZ" in temp.read():
			use_lzham = True
		temp.close()
		try:
			header = m.readBuffer(6)
			i = 0
			final = b''
			if header.startswith(b'SC'):
				use_lzma = False
				use_zstd = False
				r = b''
				while(not use_lzham):
					r = m.readBuffer(1)
					i += 1
					if r == b"]" or r == b"^":
						if i > 20:
							del i
							use_lzma = True
							break
					elif r == b"(":
						if i > 20:
							del i
							use_zstd = True 
							break
				if use_lzma:
					print("[*] detected lzma compression") 
				elif use_zstd:
					print("[*] detected zstandard compression") 
				elif use_lzham:
					print("[*] detected lzham compression")
			else:
				raise Exception("not an sc file!")
			if not use_lzham:
				data = r + m.readAll()
			else:
				data = m.readAll()
			m.free()
			del m
			del header
			del r
			decompressed = None 
			final = None
			print(f"[*] decompressing {file}")
			if use_lzma:
				try:
					decompressed = lzma.LZMADecompressor().decompress(data[:9] + b'\x00' *4 + data[9:])
				except:
					if b"START" in data:
						final = []
						for offset in range(len(data)):
							final.append(data[offset])
							if b"START" in data[:offset+5]:
								break
						decompressed = lzma.LZMADecompressor(bytes(final)).decompress(final)
					else:
						decompressed = lzma.LZMADecompressor().decompress(data)
			elif use_zstd:
				decompressed = zstandard.ZstdDecompressor().decompress(data)
			elif use_lzham:
				shitty = bytearray(data)
				while(True):
					shitty.pop(0)
					if bytes([shitty[0],shitty[1],shitty[2], shitty[3]]) == b"SCLZ":
						break
				data = bytes(shitty)
				del shitty
				y, x = struct.unpack("<BI", data[4:9])
				decompressed = lzham.decompress(data[9:], x, {"dict_size_log2": y})
				del x
				del y
		except:
			print("[*] error when decompressing:\n", traceback.format_exc())
		if decompressed:
			del data
			del final
			try:
				if not use_disk:
					sc = memory(decompressed)
				else:
					s = open("temp.sb","wb")
					s.write(decompressed)
					s.close()
					s = open("temp.sb","rb")
					sc = memory(b'')
					sc.mem.close()
					sc.mem = s
				del decompressed
				index = 0
				while(True):
					try:
						info = struct.unpack("<BIBHH", sc.readBuffer(10))
						if info[0] > 255:
							break
						if info[3] > 0 and info[4] > 0:
							area = info[3] * info[4]
							temp = file.split("/")[len(file.split("/"))-1] 
							sub = "" 
							for x in range(index):
								sub += "_" 
							name = temp.replace(".sc","") + sub + ".png"
							pixels = []
							print(f"[*] collecting pixels of {name} | area: {area}")
							for unk in range(area):
								pixels.append(sc.readPixel(info[2]))
							img = {"info":info,"name":name,"pixels":pixels}
							try:
								if not bytes2image(img):
									index -= 1
								print()
							except:
								print(f"[*] failed to decode {name}")
								print()
							index += 1
					except:
						break
				sc.free()
				del sc
				if use_disk:
					os.remove("temp.sb")
			except:
				print(traceback.format_exc())
				pass