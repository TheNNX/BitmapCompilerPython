import struct

class FileHelper:

    def __init__(this, file):
        this.file = file

    def ReadInt32u(this):
        return struct.unpack("<L", this.file.read(4))[0]

    def ReadInt32s(this):
        return struct.unpack("<l", this.file.read(4))[0]

    def ReadInt16u(this):
        return struct.unpack("<H", this.file.read(2))[0]

    def ReadInt16s(this):
        return struct.unpack("<h", this.file.read(2))[0]

    def ReadChar(this):
        return struct.unpack("<c", this.file.read(1))[0].encode("ASCII")

    def ReadData(this, size):
        return this.file.read(size)

    def ReadByte(this, byte):
        return struct.unpack("<B", this.file.read(1))[0]

    def WriteInt32u(this, data):
        this.file.write(struct.pack("<L", data))

    def WriteInt32s(this, data):
        this.file.write(struct.pack("<l", data))

    def WriteInt16u(this, data):
        this.file.write(struct.pack("<H", data))

    def WriteInt16s(this, data):
        this.file.write(struct.pack("<h", data))

    def WriteChar(this, data):
        this.file.write(struct.pack("<c", data.encode("ASCII")))

    def WriteData(this, data):
        this.file.write(data)

    def WriteByte(this, byte):
        this.file.write(struct.pack("<B", byte))

class PseudoFile:
    data = bytearray(0)

    def __init__(this):
        this.data = bytearray(0)

    def read(this, size):

        result = []

        for i in range(0,size):
            result.append(this.data.pop())
        result.reverse()

        return result

    def write(this, data):
        for b in data:
            assert (b <= 255), f"Byte too large {b}"
            this.data.append(b)

    def count(this):
        return len(this.data)

    def Dump(this, file):
        file.write(this.data)

# not really used other than to just dump all this into the executable
class MZHeaderHelper:
    extraBytes = 0x0000
    pages = 0x0004
    relocationItems = 0x0000
    headerSize = 0x0004
    minimumAllocation = 0x0000
    maximumAllocation = 0xFFFF
    stackSegment = 0x0000
    stackPointer = 0x00B8
    instructionPointer = 0x0000
    codeSegment = 0x0000
    relocationTable = 0x0040
    overlay = 0x0000
    e_lfanew = 0x80

    # 'This program cannot be run in DOS mode' stub
    dosStub = [0x0E, 0x1F, 0xBA, 0x0E, 0x00, 0xB4, 0x09, 0xCD, 0x21, 0xB8, 0x01, 0x4C, 0xCD, 0x21, 0x54, 0x68,
               0x69, 0x73, 0x20, 0x70, 0x72, 0x6F, 0x67, 0x72, 0x61, 0x6D, 0x20, 0x63, 0x61, 0x6E, 0x6E, 0x6F,
               0x74, 0x20, 0x62, 0x65, 0x20, 0x72, 0x75, 0x6E, 0x20, 0x69, 0x6E, 0x20, 0x44, 0x4F, 0x53, 0x20,
               0x6D, 0x6F, 0x64, 0x65, 0x2E, 0x0D, 0x0D, 0x0A, 0x24, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]

    def Dump(this, file):
        helper = FileHelper(file)
        helper.WriteChar('M')
        helper.WriteChar('Z')
        helper.WriteInt16u(this.extraBytes)
        helper.WriteInt16u(this.pages)
        helper.WriteInt16u(this.relocationItems)
        helper.WriteInt16u(this.headerSize)
        helper.WriteInt16u(this.minimumAllocation)
        helper.WriteInt16u(this.maximumAllocation)
        helper.WriteInt16u(this.stackSegment)
        helper.WriteInt16u(this.stackPointer)
        helper.WriteInt16u(0x0000)
        helper.WriteInt16u(this.instructionPointer)
        helper.WriteInt16u(this.codeSegment)
        helper.WriteInt16u(this.relocationTable)
        helper.WriteInt16u(this.overlay)
        for i in range(0, 32):
            helper.WriteByte(0)
        helper.WriteInt32u(this.e_lfanew)

        for byte in this.dosStub:
            helper.WriteByte(byte)

class PEHeaderHelper:

    cpuType = 0x014C
    numberOfSections = 0x0003
    timeDateStamp = 0x00000000
    symbolTableRVA = 0x00000000
    numberOfSymbols = 0x00000000
    sizeOfOptionalHeader = 0x0000
    characteristics = 0x0102

    optMagic = 0x010b # 0x020b - (64 bit)
    optMajorLinkerVersion = 0x01
    optMinorLinkerVersion = 0x00
    optSizeOfCode = 0x00000000
    optSizeOfInitializedData = 0x00000000
    optSizeOfUninitializedData = 0x0000010
    optAddressOfEntryPoint = 0x00000000
    optBaseOfCode = 0x00000000
    optBaseOfData = 0x00000000
    optImageBase = 0x00400000
    optSectionAlignment = 0x00001000
    optFileAlignment = 0x00000200
    optMajorOperatingSystemVersion = 0x0006
    optMinorOperatingSystemVersion = 0x0000
    optMajorImageVersion = 0x0001
    optMinorImageVersion = 0x0000
    optMajorSubsystemVersion = 0x0006
    optMinorSubsystemVersion = 0x0000
    optWin32VersionValue = 0x00000000
    optSizeOfImage = 0x00000000
    optSizeOfHeaders = 0x00000400
    optCheckSum = 0x00000000
    optSubsystem = 0x0002
    optDllCharacteristics = 0x8540
    optSizeOfStackReserve = 0x00200000
    optSizeOfStackCommit = 0x00001000
    optSizeOfHeapReserve = 0x00100000
    optSizeOfHeapCommit = 0x00001000
    optLoaderFlags = 0x00000000
    optNumberOfRvaAndSizes = 0x00000000

    def Dump(this, file):
        helper = FileHelper(file)
        helper.WriteInt32u(0x00004550)
        helper.WriteInt16u(this.cpuType)
        helper.WriteInt16u(this.numberOfSections)
        helper.WriteInt32u(this.timeDateStamp)
        helper.WriteInt32u(this.symbolTableRVA)
        helper.WriteInt32u(this.numberOfSymbols)
        helper.WriteInt16u(this.sizeOfOptionalHeader)
        helper.WriteInt16u(this.characteristics)
        helper.WriteInt16u(this.optMagic)
        helper.WriteByte(this.optMajorLinkerVersion)
        helper.WriteByte(this.optMinorLinkerVersion)
        helper.WriteInt32u(this.optSizeOfCode)
        helper.WriteInt32u(this.optSizeOfInitializedData)
        helper.WriteInt32u(this.optSizeOfUninitializedData)
        helper.WriteInt32u(this.optAddressOfEntryPoint)
        helper.WriteInt32u(this.optBaseOfCode)
        helper.WriteInt32u(this.optBaseOfData)
        helper.WriteInt32u(this.optImageBase)
        helper.WriteInt32u(this.optSectionAlignment)
        helper.WriteInt32u(this.optFileAlignment)
        helper.WriteInt16u(this.optMajorOperatingSystemVersion)
        helper.WriteInt16u(this.optMinorOperatingSystemVersion)
        helper.WriteInt16u(this.optMajorImageVersion)
        helper.WriteInt16u(this.optMinorImageVersion)
        helper.WriteInt16u(this.optMajorSubsystemVersion)
        helper.WriteInt16u(this.optMinorSubsystemVersion)
        helper.WriteInt32u(this.optWin32VersionValue)
        helper.WriteInt32u(this.optSizeOfImage)
        helper.WriteInt32u(this.optSizeOfHeaders)
        helper.WriteInt32u(this.optCheckSum)
        helper.WriteInt16u(this.optSubsystem)
        helper.WriteInt16u(this.optDllCharacteristics)
        helper.WriteInt32u(this.optSizeOfStackReserve)
        helper.WriteInt32u(this.optSizeOfStackCommit)
        helper.WriteInt32u(this.optSizeOfHeapReserve)
        helper.WriteInt32u(this.optSizeOfHeapCommit)
        helper.WriteInt32u(this.optLoaderFlags)
        helper.WriteInt32u(this.optNumberOfRvaAndSizes)

class DataDirectoryEntry:
    RVA = 0
    size = 0

    def __init__(this, _RVA, _size):
        this.RVA = _RVA
        this.size = _size

    def Dump(this, file):
        helper = FileHelper(file)
        helper.WriteInt32u(this.RVA)
        helper.WriteInt32u(this.size)

class DataDirectoriesHelper:

    entries = []

    def Dump(this, file):
        for entry in this.entries:
            entry.Dump(file)

class Section:
    name = "        "
    virtualSize = 0x00000000
    virtualAddress = 0x00000000
    sizeOfRawData = 0x00000000
    pointerToRawData = 0x00000000
    pointerToRelocations = 0x00000000
    pointerToLinenumbers = 0x00000000
    numberOfRelocations = 0x0000
    numberOfLinenumbers = 0x0000
    characteristics = 0x00000000

    def __init__(this, _name, _virt_size, _virt_address, _real_size, _real_address, _characteristics):
        this.name = str(_name).encode("ASCII")
        this.virtualSize = _virt_size
        this.virtualAddress = _virt_address
        this.sizeOfRawData = _real_size
        this.pointerToRawData = _real_address
        this.characteristics = _characteristics

    def Dump(this, file):
        helper = FileHelper(file)
        tempName = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]

        for i in range(0, min(len(this.name), 8)):
            tempName[i] = this.name[i]

        for i in range(0, 8):
            helper.WriteByte(tempName[i])

        helper.WriteInt32u(this.virtualSize)
        helper.WriteInt32u(this.virtualAddress)
        helper.WriteInt32u(this.sizeOfRawData)
        helper.WriteInt32u(this.pointerToRawData)
        helper.WriteInt32u(this.pointerToRelocations)
        helper.WriteInt32u(this.pointerToLinenumbers)
        helper.WriteInt16u(this.numberOfRelocations)
        helper.WriteInt16u(this.numberOfLinenumbers)
        helper.WriteInt32u(this.characteristics)

class SectionTableHelper:
    sections = []

    def Dump(this, file):
        for section in this.sections:
            section.Dump(file)

class ExeFile:

    virtualAlign = 0x1000
    fileAlign = 0x200
    reserved = fileAlign * 2

    def __init__(this, filename):
        this.filename = filename

    def GenerateExecutableFile(this, code, data, imports):
        textSectionSize = len(code)
        dataSectionSize = len(data)
        importSectionSize = len(imports)

        textRoundedSectionSize = ((textSectionSize - 1) // this.fileAlign + 1) * this.fileAlign
        dataRoundedSectionSize = ((dataSectionSize - 1) // this.fileAlign + 1) * this.fileAlign
        importRoundedSectionSize = ((importSectionSize - 1) // this.fileAlign + 1) * this.fileAlign

        importVirtualStart = 0x1000
        textVirtualStart = importVirtualStart + ((importSectionSize - 1) // this.virtualAlign + 1) * this.virtualAlign
        dataVirtualStart = textVirtualStart + ((textSectionSize - 1) // this.virtualAlign + 1) * this.virtualAlign
        nextVirtualStart = dataVirtualStart + ((dataSectionSize - 1) // this.virtualAlign + 1) * this.virtualAlign


        # TODO: solve relocations

        importRealStart = this.reserved
        textRealStart = importRealStart + importRoundedSectionSize
        dataRealStart = textRealStart + textRoundedSectionSize
        nextVirtualEnd = dataRealStart + dataRoundedSectionSize

        exe = open(this.filename, 'wb+')
        tempBuffer = PseudoFile()
        print(tempBuffer.count())

        helper = FileHelper(tempBuffer)

        mzheader = MZHeaderHelper()
        peheader = PEHeaderHelper()

        peheader.optFileAlignment = this.fileAlign
        peheader.optSectionAlignment = this.virtualAlign

        datadirs = DataDirectoriesHelper()
        sectionTable = SectionTableHelper()

        datadirs.entries.append(DataDirectoryEntry(0x00000000, 0x00000000))
        datadirs.entries.append(DataDirectoryEntry(importVirtualStart, importSectionSize))
        datadirs.entries.append(DataDirectoryEntry(0x00000000, 0x00000000))
        datadirs.entries.append(DataDirectoryEntry(0x00000000, 0x00000000))
        datadirs.entries.append(DataDirectoryEntry(0x00000000, 0x00000000))
        datadirs.entries.append(DataDirectoryEntry(0x00000000, 0x00000000))
        datadirs.entries.append(DataDirectoryEntry(0x00000000, 0x00000000))
        datadirs.entries.append(DataDirectoryEntry(0x00000000, 0x00000000))
        datadirs.entries.append(DataDirectoryEntry(0x00000000, 0x00000000))
        datadirs.entries.append(DataDirectoryEntry(0x00000000, 0x00000000))
        datadirs.entries.append(DataDirectoryEntry(0x00000000, 0x00000000))
        datadirs.entries.append(DataDirectoryEntry(0x00000000, 0x00000000))
        datadirs.entries.append(DataDirectoryEntry(0x00000000, 0x00000000))
        datadirs.entries.append(DataDirectoryEntry(0x00000000, 0x00000000))
        datadirs.entries.append(DataDirectoryEntry(0x00000000, 0x00000000))
        datadirs.entries.append(DataDirectoryEntry(0x00000000, 0x00000000))

        sectionTable.sections.append(Section(".idata", 4096, importVirtualStart, importRoundedSectionSize, importRealStart, 0x60000020))
        sectionTable.sections.append(Section(".text", 4096, textVirtualStart, textRoundedSectionSize, textRealStart, 0x60000020))
        sectionTable.sections.append(Section(".data", 4096, textVirtualStart+4096, dataRoundedSectionSize, dataRealStart, 0x60000040))

        peheader.optAddressOfEntryPoint = textVirtualStart
        peheader.optNumberOfRvaAndSizes = 16
        peheader.numberOfSections = len(sectionTable.sections)
        peheader.sizeOfOptionalHeader = 96 + peheader.optNumberOfRvaAndSizes * 4 * 2
        peheader.optSizeOfCode = textRoundedSectionSize
        peheader.optSizeOfInitializedData = dataRoundedSectionSize + importRoundedSectionSize
        peheader.optSizeOfHeaders = this.reserved
        peheader.optBaseOfData = dataVirtualStart
        peheader.optBaseOfCode = textVirtualStart
        peheader.optSizeOfImage = 4096 * 8

        mzheader.Dump(tempBuffer)
        peheader.Dump(tempBuffer)
        datadirs.Dump(tempBuffer)
        sectionTable.Dump(tempBuffer)

        currentLength = tempBuffer.count()
        padBytesCount = this.reserved - currentLength

        print(currentLength, this.reserved, padBytesCount)

        assert(padBytesCount >= 0), f"Padding too small to fit all headers: {-padBytesCount} more padding bytes needed"

        for i in range(0, padBytesCount):
            helper.WriteByte(0x00)

        print(importRoundedSectionSize, importSectionSize)

        for i in range(0, importRoundedSectionSize):
            if i < importSectionSize:
                helper.WriteByte(imports[i])
            else:
                helper.WriteByte(0x00)

        for i in range(0, textRoundedSectionSize):
            if i < textSectionSize:
                helper.WriteByte(code[i])
            else:
                helper.WriteByte(0x00)

        for i in range(0, dataRoundedSectionSize):
            if i < dataSectionSize:
                helper.WriteByte(data[i])
            else:
                helper.WriteByte(0x00)

        tempBuffer.Dump(exe)
        exe.close()

file = ExeFile("a.exe")

imports = PseudoFile()
helper = FileHelper(imports)

helper.WriteInt32u(0x00001000+40)
helper.WriteInt32u(0x00000000)
helper.WriteInt32u(0x00000000)
helper.WriteInt32u(0x00001026+40)
helper.WriteInt32u(0x0000100C+40)
helper.WriteInt32u(0x00000000)
helper.WriteInt32u(0x00000000)
helper.WriteInt32u(0x00000000)
helper.WriteInt32u(0x00000000)
helper.WriteInt32u(0x00000000)


# 3000:
helper.WriteInt32u(0x00001016+40) # AllocConsole, 13 + 2 bytes + 1 pad byte
# 3004:
helper.WriteInt32u(0x00000000)
# 3008:
helper.WriteInt32u(0x00001026+40) # KERNEL32.DLL, 12
# 300C:
helper.WriteInt16u(0x0000)
helper.WriteInt32u(0x00001016+40)
# 2012
helper.WriteInt32u(0x00000000)
# 3016: (hint)
helper.WriteInt16s(0x0000)
# 3018:
helper.WriteData("AllocConsole".encode("ASCII"))
helper.WriteInt16u(0x0000)
# 3026:
helper.WriteData("KERNEL32.DLL".encode("ASCII"))
helper.WriteByte(0x00)
helper.WriteByte(0x00)

data = PseudoFile()
helper2 = FileHelper(data)
helper2.WriteInt32u(0x00)
helper2.WriteInt32u(0x00)
helper2.WriteInt32u(0x00)
helper2.WriteInt32u(0x00)


code = PseudoFile()
helper3 = FileHelper(code)

helper3.WriteByte(0xEB)
helper3.WriteByte(0xFE)

helper3.WriteByte(0xBF)
helper3.WriteInt32s(0x0000100C+40)
helper3.WriteByte(0xFF)
helper3.WriteByte(0x17)


file.GenerateExecutableFile(code.data, data.data, imports.data)
