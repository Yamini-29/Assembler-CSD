class ELFObjectLoader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.memory = {}
    
    def load_elf(self):
        with open(self.file_path, "rb") as f:
            elf_header = f.read(64)
            magic = elf_header[:4]
            if magic != b'\x7fELF':
                raise ValueError("Not a valid ELF file")
            
            e_shoff, e_shnum, e_shentsize = struct.unpack("QQH", elf_header[40:56])
            self.e_shoff = e_shoff
            self.e_shnum = e_shnum
            self.e_shentsize = e_shentsize

            # Load section headers
            self.load_section_headers(f)

            # Assuming you want to load symbol table and relocations after
            self.load_symbol_table(f)
            self.load_relocations(f)

    def load_section_headers(self, f):
        f.seek(self.e_shoff)
        for _ in range(self.e_shnum):
            section_header = f.read(self.e_shentsize)
            sh_name, sh_type, sh_flags, sh_addr, sh_offset, sh_size = struct.unpack("IIQQQQ", section_header[:40])

            if sh_type == 1:  # SHT_PROGBITS
                self.load_section(f, sh_offset, sh_addr, sh_size)
    
    def load_section(self, f, offset, addr, size):
        f.seek(offset)
        section_data = f.read(size)
        self.memory[addr] = section_data
        print(f"Loaded section at address {hex(addr)} with size {size} bytes")

    def load_symbol_table(self, f):
        # Parse the symbol table (example offset)
        f.seek(0x300)  # Replace with actual offset
        for _ in range(10):
            symbol_entry = f.read(24)
            st_name, st_info, st_other, st_shndx, st_value, st_size = struct.unpack("IBBHQQ", symbol_entry)
            print(f"Symbol value: {st_value}")

    def load_relocations(self, f):
        f.seek(0x400)  # Example offset for relocations
        for _ in range(10):
            r_offset, r_info = struct.unpack("QQ", f.read(16))
            print(f"Relocation entry: offset {r_offset}, info {r_info}")

# Example usage
loader = ELFObjectLoader("example.o")
loader.load_elf()
