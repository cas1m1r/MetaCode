import string
import json
import sys
import os

ABI = {
		0x00 :	'System V',
		0x01 :	'HP-UX',
		0x02 :	'NetBSD',
		0x03 :	'Linux',
		0x04 :	'GNU Hurd',
		0x06 :	'Solaris',
		0x07 :	'AIX (Monterey)',
		0x08 :	'IRIX',
		0x09 :	'FreeBSD',
		0x0A :	'Tru64',
		0x0B :	'Novell Modesto',
		0x0C :	'OpenBSD',
		0x0D :	'OpenVMS',
		0x0E :	'NonStop Kernel',
		0x0F :	'AROS',
		0x10 :	'FenixOS',
		0x11 :	'Nuxi CloudABI',
		0x12 :	'Stratus Technologies OpenVOS'}

VER = {
	0x00: 	'ET_NONE 	Unknown.',
	0x01  : 	'ET_REL 	Relocatable file.',
	0x02  :		'ET_EXEC 	Executable file.',
	0x03  :		'ET_DYN 	Shared object.',
	0x04  :		'ET_CORE 	Core file.',
	0xFE00: 	'ET_LOOS 	Reserved inclusive range. Operating system specific.',
	0xFEFF: 	'ET_HIOS',
	0xFF00: 	'ET_LOPROC 	Reserved inclusive range. Processor specific.',
	0xFFFF: 	'ET_HIPROC'
}

ISA = {
	0x00 :	'No specific instruction set',
	0x01 :	'AT&T WE 32100',
	0x02 :	'SPARC',
	0x03 :	'x86',
	0x04 :	'Motorola 68000 (M68k)',
	0x05 :	'Motorola 88000 (M88k)',
	0x06 :	'Intel MCU',
	0x07 :	'Intel 80860',
	0x08 :	'MIPS',
	0x09 :	'IBM System/370',
	0x0A :	'MIPS RS3000 Little-endian',
	0x0E :	'Hewlett-Packard PA-RISC',
	0x0F :	'Reserved for future use',
	0x13 :	'Intel 80960',
	0x14 :	'PowerPC',
	0x15 :	'PowerPC (64-bit)',
	0x16 :	'S390, including S390x',
	0x17 :	'IBM SPU/SPC',
	0x24 :	'NEC V800',
	0x25 :	'Fujitsu FR20',
	0x26 :	'TRW RH-32',
	0x27 :	'Motorola RCE',
	0x28 :	'Arm (up to Armv7/AArch32)',
	0x29 :	'Digital Alpha',
	0x2A :	'SuperH',
	0x2B :	'SPARC Version 9',
	0x2C :	'Siemens TriCore embedded processor',
	0x2D :	'Argonaut RISC Core',
	0x2E :	'Hitachi H8/300',
	0x2F :	'Hitachi H8/300H',
	0x30 :	'Hitachi H8S',
	0x31 :	'Hitachi H8/500',
	0x32 :	'IA-64',
	0x33 :	'Stanford MIPS-X',
	0x34 :	'Motorola ColdFire',
	0x35 :	'Motorola M68HC12',
	0x36 :	'Fujitsu MMA Multimedia Accelerator',
	0x37 :	'Siemens PCP',
	0x38 :	'Sony nCPU embedded RISC processor',
	0x39 :	'Denso NDR1 microprocessor',
	0x3A :	'Motorola Star*Core processor',
	0x3B :	'Toyota ME16 processor',
	0x3C :	'STMicroelectronics ST100 processor',
	0x3D :	'Advanced Logic Corp. TinyJ embedded processor family',
	0x3E :	'AMD x86-64',
	0x3F :	'Sony DSP Processor',
	0x40 :	'Digital Equipment Corp. PDP-10',
	0x41 :	'Digital Equipment Corp. PDP-11',
	0x42 :	'Siemens FX66 microcontroller',
	0x43 :	'STMicroelectronics ST9+ 8/16 bit microcontroller',
	0x44 :	'STMicroelectronics ST7 8-bit microcontroller',
	0x45 :	'Motorola MC68HC16 Microcontroller',
	0x46 :	'Motorola MC68HC11 Microcontroller',
	0x47 :	'Motorola MC68HC08 Microcontroller',
	0x48 :	'Motorola MC68HC05 Microcontroller',
	0x49 :	'Silicon Graphics SVx',
	0x4A :	'STMicroelectronics ST19 8-bit microcontroller',
	0x4B :	'Digital VAX',
	0x4C :	'Axis Communications 32-bit embedded processor',
	0x4D :	'Infineon Technologies 32-bit embedded processor',
	0x4E :	'Element 14 64-bit DSP Processor',
	0x4F :	'LSI Logic 16-bit DSP Processor',
	0x8C :	'TMS320C6000 Family',
	0xAF :	'MCST Elbrus e2k',
	0xB7 :	'Arm 64-bits (Armv8/AArch64)',
	0xDC :	'Zilog Z80',
	0xF3 :	'RISC-V',
	0xF7 :	'Berkeley Packet Filter',
	0x101: 	'WDC 65C816',
}


def litte_endian_format(bytedata):
	return f"{''.join([hex(h)[2:] for h in bytedata][::-1])}"

def big_endian_format(bytedata):
	return f"{''.join([hex(h)[2:] for h in bytedata][::1])}"


class ELF():
	def __init__(self,filename:str):
		# Read in the data
		self.name = filename 
		self.binary = open(filename,'rb').read()
		self.header = self.parse_header()
		self.program_header = self.parse_program_header()

	def parse_header(self):
		header = {'Architecture':'', 'Endianness': '',
				  'OS/ABI': ''}

		entryfn = {1: litte_endian_format,
				   2: big_endian_format}
		arch = {1: '32bit', 2:'64bit'}
		ends = {1: 'litte', 2:'big'}
		fsize = {1:4, 2:8}
		
		emagic = self.binary[0:4]
		eclass = self.binary[4]
		endian = self.binary[5]
		eosabi = self.binary[7]
		abiver = self.binary[8]
		padsn1 = self.binary[9:16]  # should be zeros
		eotype = self.binary[16:18] 
		isarch = self.binary[18]
		eversn = self.binary[20:24]
		entryoffset = {1:28,2:32}
		phoffset = {1:28, 2:32}
		peshoff  = {1:32, 2:40}
		shtstop =  {1:36, 2:48}
		pheadsize = {1:40, 2:52}
		phentsize = {1:42, 2:54}
		phnumentry = {1:44, 2:56}
		shtensize = {1:46, 2:58}
		shnnumentry = {1:48, 2:60}
		tableoffset = {1:50, 2:62}
		endofheader = {1:52, 2:64}
		
		entryp = entryfn[endian](self.binary[24:entryoffset[eclass]])
		proghoff = entryfn[endian](self.binary[phoffset[eclass]:phoffset[eclass]+fsize[eclass]])
		sectoff = entryfn[endian](self.binary[peshoff[eclass]:shtstop[eclass]])
		headsize = entryfn[endian](self.binary[pheadsize[eclass]:pheadsize[eclass]+2])
		headesize = entryfn[endian](self.binary[phentsize[eclass]:phentsize[eclass]+2])
		pheadsize = entryfn[endian](self.binary[pheadsize[eclass]:pheadsize[eclass]+2])
		
		numentries = entryfn[endian](self.binary[phnumentry[eclass]:phnumentry[eclass]+2])
		sectheadentsize = entryfn[endian](self.binary[shtensize[eclass]:shtensize[eclass]+2])
		secheadnumentry = entryfn[endian](self.binary[shnnumentry[eclass]:shnnumentry[eclass]+2])
		strtableindex   = entryfn[endian](self.binary[tableoffset[eclass]:tableoffset[eclass]+2]) 

		header['Architecture'] = arch[eclass]			# Architecture
		header['Endianness'] = ends[endian]				# endianess
		header['OS/ABI'] = ABI[int(eosabi)]	# OS Application Binary Interface
		header['FileType'] = VER[int(entryfn[endian](eotype))]	# File Type [Executable, Dynamic, etc.]
		header['Machine'] = ISA[isarch]					# Instruction set Architecture
		header['Flags'] = f'0x{entryfn[endian](self.binary[shtstop[eclass]+1:shtstop[eclass]+4])}'
		header['HeaderSize'] 					= f'{int(headsize, 16)} Bytes'
		header['EntrypointAddress'] 			= f'0x{entryp}'
		header['SectionHeaderOffset:']			= f'0x{sectoff}'
		header['Program Header Size'] 			= int(pheadsize, 16)
		header['Program Header Offset'] 		= f'0x{proghoff}'
		header['Size of Program Header'] 		= int(headesize, 16)
		header['Number of Headers'] 			= int(numentries,  16)
		header['Size of Section Headers'] 		= int(sectheadentsize, 16)
		header['Number Section Headers'] 		= int(secheadnumentry, 16)
		header['Section header String Index'] 	= int(strtableindex, 16)
		print(f'[DEBUG] Program Header Offset: 0x{proghoff}')
		return header


	def parse_program_header(self):
		eclass = {'litte':1, 'big':2}
		program_header = {}

		

		return program_header




	def show(self):
		print(json.dumps(self.header,indent=2))

	def __repr__(self):
		return json.dumps(self.header,indent=2)


def main():
	# Get input file
	if len(sys.argv) > 1:
		binary = sys.argv[1]
		elf = ELF(binary)
		elf.show()
	else:
		print(f'Usage: python {sys.argv[0]} [file]')
		exit()





if __name__ == '__main__':
	main()
