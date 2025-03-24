# SORRY FOR THE SHITTY CODE!!!

import sys, gzip

print(f"A REALLY SHITTY OPL2 INSTRUMENT RIPPER!!! v1.02\n===========================================================")

if len(sys.argv) < 2:
	print("WARNING: There was no specified file path!\n\nUsage: python opl2_to_fui.py [filename_here]")
	exit(1)
fp = sys.argv[1]
ext = fp[-4:]

if not (fp.endswith('.vgm') or fp.endswith('.vgz')):
    print("ERROR: Specified file was not a .vgm or .vgz file")
    exit(1)

if '.vgm' in fp: f = open(fp, 'rb+')
elif '.vgz' in fp: f = gzip.open(fp, 'rb+')

if f.read(4).decode() != 'Vgm ':
	print("ERROR: Not a valid .vgm file!")
	exit(1)
f.seek(0x08)
if int.from_bytes(f.read(4), 'little') < 337:
	print("ERROR: Version of .vgm file is older than version 1.51!")
	exit(1)
f.seek(0x50)
if int.from_bytes(f.read(4), 'little') == 0:
	print("ERROR: There is no OPL2 detected in the .vgm file!")
	exit(1)

f.seek(0x34) # Goes to offset
f.seek(f.tell()+int.from_bytes(f.read(4), 'little'))

states = []
insts = []
regs = {
	0: {"fb":0,"alg":0,"ops":{}},
	1: {"fb":0,"alg":0,"ops":{}},
	2: {"fb":0,"alg":0,"ops":{}},
	3: {"fb":0,"alg":0,"ops":{}},
	4: {"fb":0,"alg":0,"ops":{}},
	5: {"fb":0,"alg":0,"ops":{}},
	6: {"fb":0,"alg":0,"ops":{}},
	7: {"fb":0,"alg":0,"ops":{}},
	8: {"fb":0,"alg":0,"ops":{}},
}

for i in regs:
	nops = {1: None, 2: None}
	for j in nops:
		nops[j] = {
			"am":0,
			"vib":0,
			"sus":0,
			"ksr":0,
			"ml":0,
			"ksl":0,
			"tl":0,
			"a":0,
			"d":0,
			"s":0,
			"r":0,
			"wav":0,
		}
	regs[i]["ops"] = nops

print("Reading file...")

while True:
	c = int.from_bytes(f.read(1), 'big')

	if c == 0x5A:
		a = int.from_bytes(f.read(1), 'big')
		d = int.from_bytes(f.read(1), 'big')
		dbin = bin(d)[2:].zfill(8)

		# thanks a lot yahama. you placed the registers all weird, and i wrote a lot of fucking lines just for this part.
		if (a >= 0x20) and (a <= 0x35):
			if (a >= 0x20) and (a <= 0x22):
				regs[(a-0x20)]["ops"][1]["am"] = int(dbin[0],2)
				regs[(a-0x20)]["ops"][1]["vib"] = int(dbin[1],2)
				regs[(a-0x20)]["ops"][1]["sus"] = int(dbin[2],2)
				regs[(a-0x20)]["ops"][1]["ksr"] = int(dbin[3],2)
				regs[(a-0x20)]["ops"][1]["ml"] = int(dbin[4:8],2)
			elif (a >= 0x23) and (a <= 0x25):
				regs[(a-0x23)]["ops"][2]["am"] = int(dbin[0],2)
				regs[(a-0x23)]["ops"][2]["vib"] = int(dbin[1],2)
				regs[(a-0x23)]["ops"][2]["sus"] = int(dbin[2],2)
				regs[(a-0x23)]["ops"][2]["ksr"] = int(dbin[3],2)
				regs[(a-0x23)]["ops"][2]["ml"] = int(dbin[4:8],2)
			elif (a >= 0x28) and (a <= 0x2A):
				regs[(a-0x25)]["ops"][1]["am"] = int(dbin[0],2)
				regs[(a-0x25)]["ops"][1]["vib"] = int(dbin[1],2)
				regs[(a-0x25)]["ops"][1]["sus"] = int(dbin[2],2)
				regs[(a-0x25)]["ops"][1]["ksr"] = int(dbin[3],2)
				regs[(a-0x25)]["ops"][1]["ml"] = int(dbin[4:8],2)
			elif (a >= 0x2B) and (a <= 0x2D):
				regs[(a-0x28)]["ops"][2]["am"] = int(dbin[0],2)
				regs[(a-0x28)]["ops"][2]["vib"] = int(dbin[1],2)
				regs[(a-0x28)]["ops"][2]["sus"] = int(dbin[2],2)
				regs[(a-0x28)]["ops"][2]["ksr"] = int(dbin[3],2)
				regs[(a-0x28)]["ops"][2]["ml"] = int(dbin[4:8],2)
			elif (a >= 0x30) and (a <= 0x32):
				regs[(a-0x2A)]["ops"][1]["am"] = int(dbin[0],2)
				regs[(a-0x2A)]["ops"][1]["vib"] = int(dbin[1],2)
				regs[(a-0x2A)]["ops"][1]["sus"] = int(dbin[2],2)
				regs[(a-0x2A)]["ops"][1]["ksr"] = int(dbin[3],2)
				regs[(a-0x2A)]["ops"][1]["ml"] = int(dbin[4:8],2)
			elif (a >= 0x33) and (a <= 0x35):
				regs[(a-0x2D)]["ops"][2]["am"] = int(dbin[0],2)
				regs[(a-0x2D)]["ops"][2]["vib"] = int(dbin[1],2)
				regs[(a-0x2D)]["ops"][2]["sus"] = int(dbin[2],2)
				regs[(a-0x2D)]["ops"][2]["ksr"] = int(dbin[3],2)
				regs[(a-0x2D)]["ops"][2]["ml"] = int(dbin[4:8],2)
		elif (a >= 0x40) and (a <= 0x55):
			if (a >= 0x40) and (a <= 0x42): # ksl values sure are confusing.. :P (reversing the binary bits was one solution) yahama, you so cray cray.
				regs[(a-0x40)]["ops"][1]["ksl"] = int(dbin[0:2][::-1],2)
				regs[(a-0x40)]["ops"][1]["tl"] = int(dbin[2:8],2)
			if (a >= 0x43) and (a <= 0x45):
				regs[(a-0x43)]["ops"][2]["ksl"] = int(dbin[0:2][::-1],2)
				regs[(a-0x43)]["ops"][2]["tl"] = int(dbin[2:8],2)
			if (a >= 0x48) and (a <= 0x4A):
				regs[(a-0x45)]["ops"][1]["ksl"] = int(dbin[0:2][::-1],2)
				regs[(a-0x45)]["ops"][1]["tl"] = int(dbin[2:8],2)
			if (a >= 0x4B) and (a <= 0x4D):
				regs[(a-0x48)]["ops"][2]["ksl"] = int(dbin[0:2][::-1],2)
				regs[(a-0x48)]["ops"][2]["tl"] = int(dbin[2:8],2)
			if (a >= 0x50) and (a <= 0x52):
				regs[(a-0x4A)]["ops"][1]["ksl"] = int(dbin[0:2][::-1],2)
				regs[(a-0x4A)]["ops"][1]["tl"] = int(dbin[2:8],2)
			if (a >= 0x53) and (a <= 0x55):
				regs[(a-0x4D)]["ops"][2]["ksl"] = int(dbin[0:2][::-1],2)
				regs[(a-0x4D)]["ops"][2]["tl"] = int(dbin[2:8],2)
		elif (a >= 0x60) and (a <= 0x75):
			if (a >= 0x60) and (a <= 0x62):
				regs[(a-0x60)]["ops"][1]["a"] = int(dbin[0:4],2)
				regs[(a-0x60)]["ops"][1]["d"] = int(dbin[4:8],2)
			if (a >= 0x63) and (a <= 0x65):
				regs[(a-0x63)]["ops"][2]["a"] = int(dbin[0:4],2)
				regs[(a-0x63)]["ops"][2]["d"] = int(dbin[4:8],2)
			if (a >= 0x68) and (a <= 0x6A):
				regs[(a-0x65)]["ops"][1]["a"] = int(dbin[0:4],2)
				regs[(a-0x65)]["ops"][1]["d"] = int(dbin[4:8],2)
			if (a >= 0x6B) and (a <= 0x6D):
				regs[(a-0x68)]["ops"][2]["a"] = int(dbin[0:4],2)
				regs[(a-0x68)]["ops"][2]["d"] = int(dbin[4:8],2)
			if (a >= 0x70) and (a <= 0x72):
				regs[(a-0x6A)]["ops"][1]["a"] = int(dbin[0:4],2)
				regs[(a-0x6A)]["ops"][1]["d"] = int(dbin[4:8],2)
			if (a >= 0x73) and (a <= 0x75):
				regs[(a-0x6D)]["ops"][2]["a"] = int(dbin[0:4],2)
				regs[(a-0x6D)]["ops"][2]["d"] = int(dbin[4:8],2)
		elif (a >= 0x80) and (a <= 0x95):
			if (a >= 0x80) and (a <= 0x82):
				regs[(a-0x80)]["ops"][1]["s"] = int(dbin[0:4],2)
				regs[(a-0x80)]["ops"][1]["r"] = int(dbin[4:8],2)
			if (a >= 0x83) and (a <= 0x85):
				regs[(a-0x83)]["ops"][2]["s"] = int(dbin[0:4],2)
				regs[(a-0x83)]["ops"][2]["r"] = int(dbin[4:8],2)
			if (a >= 0x88) and (a <= 0x8A):
				regs[(a-0x85)]["ops"][1]["s"] = int(dbin[0:4],2)
				regs[(a-0x85)]["ops"][1]["r"] = int(dbin[4:8],2)
			if (a >= 0x8B) and (a <= 0x8D):
				regs[(a-0x88)]["ops"][2]["s"] = int(dbin[0:4],2)
				regs[(a-0x88)]["ops"][2]["r"] = int(dbin[4:8],2)
			if (a >= 0x90) and (a <= 0x92):
				regs[(a-0x8A)]["ops"][1]["s"] = int(dbin[0:4],2)
				regs[(a-0x8A)]["ops"][1]["r"] = int(dbin[4:8],2)
			if (a >= 0x93) and (a <= 0x95):
				regs[(a-0x8D)]["ops"][2]["s"] = int(dbin[0:4],2)
				regs[(a-0x8D)]["ops"][2]["r"] = int(dbin[4:8],2)
		elif (a >= 0xE0) and (a <= 0xF5):
			if (a >= 0xE0) and (a <= 0xE2):
				regs[(a-0xE0)]["ops"][1]["wav"] = int(dbin[6:8],2)
			if (a >= 0xE3) and (a <= 0xE5):
				regs[(a-0xE3)]["ops"][2]["wav"] = int(dbin[6:8],2)
			if (a >= 0xE8) and (a <= 0xEA):
				regs[(a-0xE5)]["ops"][1]["wav"] = int(dbin[6:8],2)
			if (a >= 0xEB) and (a <= 0xED):
				regs[(a-0xE8)]["ops"][2]["wav"] = int(dbin[6:8],2)
			if (a >= 0xF0) and (a <= 0xF2):
				regs[(a-0xEA)]["ops"][1]["wav"] = int(dbin[6:8],2)
			if (a >= 0xF3) and (a <= 0xF5):
				regs[(a-0xED)]["ops"][2]["wav"] = int(dbin[6:8],2)
		elif (a >= 0xA0) and (a <= 0xBD):
			states.append(regs)
		elif (a >= 0xC0) and (a <= 0xC8):
			regs[(a - 0xC0)]["fb"] = int(dbin[4:7],2)
			regs[(a - 0xC0)]["alg"] = int(dbin[7],2)
		else:
			pass
	elif ((c >= 0x70) and (c <= 0x7F)) or c == 0x62 or c == 0x63:
		pass
	elif c == 0x61:
		f.seek(f.tell()+2)
	elif c == 0x66:
		break

print("List of instrument data created!")

print("Cleaning up list...")

# CHECKS FOR DUPLICATED DATA!!!
for i in states:  
    for j in i:  
        if i[j] in insts:
            continue
        else:
            insts.append(i[j])

print("List cleaned!\n===========================================================")

print("Creating .fui files...")

# SAVES INSTRUMENT DATA TO .FUI FILES!!!
a = 0
for i in insts:
	a += 1
	with open(f"{fp.split(ext)[0]}_inst{a}.fui", 'wb+') as inf:
		inf.write(b"FINS\xDB\x00\x0E\x00FM\x14\x00\xF2")
		inf.write(bytes([int(f'{i["alg"]:04b}{i["fb"]:04b}', 2)]))
		inf.write(b"\x00\x00")
		for j in range(2):
			inf.write(bytes([int(f'{i["ops"][j+1]["ksr"]:01b}{0:03b}{i["ops"][j+1]["ml"]:04b}', 2)]))
			inf.write(bytes([int(f'{i["ops"][j+1]["sus"]:01b}{i["ops"][j+1]["tl"]:07b}', 2)]))
			inf.write(bytes([int(f'{0:03b}{i["ops"][j+1]["vib"]:01b}{i["ops"][j+1]["a"]:04b}', 2)]))
			inf.write(bytes([int(f'{i["ops"][j+1]["am"]:01b}{f"{i["ops"][j+1]["ksl"]:02b}"[::-1]}{i["ops"][j+1]["d"]:05b}', 2)])) # did tilde take cues from yamaha, on the ksl part?
			inf.write(b"\x00")
			inf.write(bytes([int(f'{i["ops"][j+1]["s"]:04b}{i["ops"][j+1]["r"]:04b}', 2)]))
			inf.write(b"\x00")
			inf.write(bytes([int(f'{0:06b}{i["ops"][j+1]["wav"]:02b}', 2)]))
	print(f"Exported {fp.split(ext)[0]}_inst{a}.fui!")
print("===========================================================")