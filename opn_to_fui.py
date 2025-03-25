# yet again, sorry for the shitty code. i think i improved a bit.
# if you say there's already something like this, suck my dick. this is an programmer's exercise.

import sys, gzip

print(f"A REALLY SHITTY OPN INSTRUMENT RIPPER!!! v1.01\n===========================================================")

if len(sys.argv) < 2:
	print("WARNING: There was no specified file path!\n\nUsage: python opn_to_fui.py [filename_here]")
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
ver = int.from_bytes(f.read(4), 'little')
if ver < 272:
	print("ERROR: Version of .vgm file is older than version 1.10!")
	exit(1)

f.seek(0x2C)
if int.from_bytes(f.read(4), 'little') != 0:
	opnT = "YM2612"
else: f.seek(0x44)

if ver >= 337:
	if int.from_bytes(f.read(4), 'little') != 0:
		opnT = "YM2203"
	if int.from_bytes(f.read(4), 'little') != 0:
		opnT = "YM2608"
	if int.from_bytes(f.read(4), 'little') != 0:
		opnT = "YM2610(B)"
if not opnT: 
	print("ERROR: No OPN chip detected in .vgm file!")
	exit(1)

print(f"File Name: {fp}\nOPN Type: Yamaha {opnT}")

f.seek(0x34) # Goes to offset
f.seek(f.tell()+int.from_bytes(f.read(4), 'little'))

states = []
insts = []
regs = {
	0: {"fb":0,"alg":0,"lfof":0,"lfoa":0,"l":0,"r":0,"ops":{}},
	1: {"fb":0,"alg":0,"lfof":0,"lfoa":0,"l":0,"r":0,"ops":{}},
	2: {"fb":0,"alg":0,"lfof":0,"lfoa":0,"l":0,"r":0,"ops":{}},
	3: {"fb":0,"alg":0,"lfof":0,"lfoa":0,"l":0,"r":0,"ops":{}},
	4: {"fb":0,"alg":0,"lfof":0,"lfoa":0,"l":0,"r":0,"ops":{}},
	5: {"fb":0,"alg":0,"lfof":0,"lfoa":0,"l":0,"r":0,"ops":{}},
}

for i in regs:
	nops = {1: None, 2: None, 3: None, 4: None}
	for j in nops:
		nops[j] = {
			"dt":0,
			"ml":0,
			"tl":0,
			"ks":0,
			"ar":0,
			"am":0,
			"dr":0,
			"sr":0,
			"sl":0,
			"rr":0,
			"ssg_togg":0,
			"ssg_type":0,
		}
	regs[i]["ops"] = nops


print("===========================================================\nReading file...")

while True:
	c = int.from_bytes(f.read(1), 'big')

	if (c == 0x52) or (c == 0x53):
		a = int.from_bytes(f.read(1), 'big')
		d = int.from_bytes(f.read(1), 'big')
		abin = bin(a)[2:].zfill(8)
		dbin = bin(d)[2:].zfill(8)

		if (c == 0x52) or (c == 0x55) or (c == 0x56) or (c == 0x58): ch = a%4 # yamaha never learned their lesson on registers, havent they?... luckily, i came up with some big solutions
		else: ch = a%4+3

		if (int(abin[4:8],2) >= 0) and (int(abin[4:8],2) <= 3): op = 1
		elif (int(abin[4:8],2) >= 4) and (int(abin[4:8],2) <= 7): op = 3
		elif (int(abin[4:8],2) >= 8) and (int(abin[4:8],2) <= 11): op = 2
		elif (int(abin[4:8],2) >= 12) and (int(abin[4:8],2) <= 15): op = 4

		if (a >= 0xA0) and (a <= 0xAE): 
			states.append(regs)
		elif (a >= 0x30) and (a <= 0x3E): 
			dt = int(dbin[1:4],2)
			if dt > 4:
				dt = -dt # stolen from zumi and then changed up a notch. zumi, if you're reading this. i am really fucking sorry. i'm shit at coding.
				dt += 4

			regs[ch]["ops"][op]["dt"] = dt
			regs[ch]["ops"][op]["ml"] = int(dbin[4:8],2)
		elif (a >= 0x40) and (a <= 0x4E): 
			regs[ch]["ops"][op]["tl"] = int(dbin[1:8],2)
		elif (a >= 0x50) and (a <= 0x5E): 
			regs[ch]["ops"][op]["ks"] = int(dbin[0:2],2) # thank god the bits aren't backwards
			regs[ch]["ops"][op]["ar"] = int(dbin[3:8],2)
		elif (a >= 0x60) and (a <= 0x6E): 
			regs[ch]["ops"][op]["am"] = int(dbin[0],2)
			regs[ch]["ops"][op]["dr"] = int(dbin[3:8],2)
		elif (a >= 0x70) and (a <= 0x7E): 
			regs[ch]["ops"][op]["sr"] = int(dbin[3:8],2)
		elif (a >= 0x80) and (a <= 0x8E): 
			regs[ch]["ops"][op]["sl"] = int(dbin[0:4],2)
			regs[ch]["ops"][op]["rr"] = int(dbin[4:8],2)
		elif (a >= 0x90) and (a <= 0x9E): 
			regs[ch]["ops"][op]["ssg_togg"] = int(dbin[4],2)
			regs[ch]["ops"][op]["ssg_type"] = int(dbin[5:8],2)
		elif (a >= 0xB0) and (a <= 0xB2): 
			regs[ch]["fb"] = int(dbin[2:5],2)
			regs[ch]["alg"] = int(dbin[5:8],2)
		elif (a >= 0xB4) and (a <= 0xB5): 
			regs[ch]["l"] = int(dbin[0],2)
			regs[ch]["r"] = int(dbin[1],2)
			regs[ch]["lfoa"] = int(dbin[2:4],2)
			regs[ch]["lfof"] = int(dbin[5:8],2)
	elif (c == 0x62) or (c == 0x63) or (c >= 0x70) and (c <= 0x7F):
		pass
	elif (c == 0x61) or (c == 0x53):
		f.seek(f.tell()+2)
	elif c == 0x66:
		break

print("List of instrument data created!")
print("Cleaning up list...")

for i in states:  
    for j in i:  
        if i[j] in insts:
            continue
        else:
            insts.append(i[j])

print("List cleaned!\n===========================================================")
print("Creating .fui files...")

a = 0
for i in insts:
	a += 1
	with open(f"{fp.split(ext)[0]}_inst{a}.fui", 'wb+') as inf:
		inf.write(b"FINS\xDB\x00\x01\x00FM\x24\x00\xF4")
		inf.write(bytes([int(f'{i["alg"]:04b}{i["fb"]:04b}', 2)]))
		inf.write(bytes([int(f'{0:03b}{i["lfoa"]:02b}{i["lfof"]:03b}', 2)]))
		inf.write(b"\x00")

		for j in [1,3,2,4]:
			dt = i["ops"][j]["dt"] # very sorry again, zumi
			dt += 3
			inf.write(bytes([int(f'{0:01b}{dt:03b}{i["ops"][j]["ml"]:04b}', 2)]))
			inf.write(bytes([int(f'{i["ops"][j]["tl"]:08b}', 2)]))
			inf.write(bytes([int(f'{i["ops"][j]["ks"]:02b}{i["ops"][j]["ar"]:06b}', 2)]))
			inf.write(bytes([int(f'{i["ops"][j]["am"]:01b}{0:03b}{i["ops"][j]["dr"]:04b}', 2)]))
			inf.write(bytes([int(f'{4:04b}{i["ops"][j]["sr"]:04b}', 2)]))
			inf.write(bytes([int(f'{i["ops"][j]["sl"]:04b}{i["ops"][j]["rr"]:04b}', 2)]))
			inf.write(bytes([int(f'{0:03b}{i["ops"][j]["ssg_togg"]:03b}{i["ops"][j]["ssg_type"]:04b}', 2)]))
			inf.write(b"\x00")
	print(f"Exported {fp.split(ext)[0]}_inst{a}.fui!")
print("===========================================================")