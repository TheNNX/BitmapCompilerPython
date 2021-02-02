bitmap = open('bitmap.bmp', 'rb')

bmpMagic = struct.unpack("<H",  bitmap.read(2))[0]
bmpSize = struct.unpack("<L", bitmap.read(4))[0]
bmpReserved = struct.unpack("<L", bitmap.read(4))[0]
bmpPixelArrayOffset = struct.unpack("<L", bitmap.read(4))[0]
bmpHeaderSize = struct.unpack("<L", bitmap.read(4))[0]
bmpWidth = struct.unpack("<L", bitmap.read(4))[0]
bmpHeight = struct.unpack("<L", bitmap.read(4))[0]
bmpColorPlanesN = struct.unpack("<H", bitmap.read(2))[0]
bmpBitsPerPixel = struct.unpack("<H", bitmap.read(2))[0]
assert(bmpBitsPerPixel == 24), f"Error: bmpBitsPerPixel not 24 ({bmpBitsPerPixel})"
bmpCompression = struct.unpack("<L", bitmap.read(4))[0]
assert(bmpCompression == 0), "Error: bitmap file not RGB"
bmpImageSize = struct.unpack("<L", bitmap.read(4))[0]
bmpHorizontalResolution = struct.unpack("<L", bitmap.read(4))[0]
bmpVerticalResolution = struct.unpack("<L", bitmap.read(4))[0]
bmpNumberOfColors = struct.unpack("<L", bitmap.read(4))[0]
bmpNumberOfImportantColors = struct.unpack("<L", bitmap.read(4))[0]

bitmap.seek(bmpPixelArrayOffset, 0)

# oh python, why can't you be normal?!
bytesPerRow = (((bmpWidth * 3) - 1) // 4 + 1) * 4

pixelData = bitmap.read(bmpHeight * bytesPerRow * 3)

for j in range(0, bmpHeight):
    for i in range(0, bmpWidth):
        pixel = struct.unpack_from("<BBB", pixelData, bytesPerRow * (bmpHeight - 1 - j) + i * 3)

        #if pixel == (0,255,0):
        #    print('#', end='')
        #else:
        #    print(' ', end='')
    #print('')

bitmap.close()
