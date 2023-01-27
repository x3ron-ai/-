from PIL import Image
import json
import time
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

with Image.open("Карта.png") as f:
	f = f.convert("RGB")
	width, height = f.size
	pixels = f.load()
	print(pixels[0,0])
def get_white(x,y,pol):
	mas = []
	mas.append(pol[x-1,y])
	mas.append(pol[x+1,y])
	mas.append(pol[x,y-1])
	mas.append(pol[x,y+1])
	return mas
def get_near(crd,pixels):
	x,y = crd
	vals = [(x-1,y),(x+1,y), (x,y-1), (x,y+1), ( x-1,y-1), (x+1,y+1), (x+1,y-1),(x-1,y+1)]
	resp = []
	for i in vals:
		if i in pixels:
			resp.append(i)

	return resp
color_names = {
	"Южный округ":[4, 145, 67],
	"Центральный округ":[0, 128, 192],
	"Северо-западный округ":[129, 129, 207],
	"Приволжский округ":[252, 139, 139],
	"Уральский округ":[199, 203, 143],
	"Сибирский округ":[192, 192, 192],
	"Дальневосточный округ":[254, 206, 44]
}

colors = {}
bruh = []
AREA = Image.new("RGB", (width, height), (255,255,255))
AREA_pix = []
for x in range(width):
	for y in range(height):
		gg = list(pixels[x,y])
		if gg == [255,255,255]: continue
		color_name = 'default'
		for name, i in color_names.items():
			if gg == i:
				color_name = name
				break

		if color_name not in colors:
			colors[color_name] = []
		if (255,255,255) in get_white(x,y,pixels):
			AREA.putpixel((x,y), tuple(gg))
			colors[color_name].append((x,y))

for name in colors:
	cords = colors[name]
	region = Image.new("RGB", (width, height), (255,255,255))
	for i in cords:
		region.putpixel(i, (0,0,0))
	region.save(f"{name}.png")
for color in colors:
	lands = []
	cords = colors[color]
	while len(cords) != 0:
		otr = []
		start_cord = cords[0]
		print(start_cord, color)
		cur_cord = cords[0]
		bruh = 0
		skipone = 1
		while bruh == 0:
			otr.append(cur_cord)
			try: cords.remove(cur_cord)
			except Exception as e:
				print(e)
				if skipone == 0:
					bruh = 1
				skipone = 0

			near = get_near(cur_cord, cords)
			for i in near:
				if i not in otr:
					cur_cord = i
					break
		for i in range(0,len(otr),20):
			try:
				otr.pop(i)
				otr.pop(i+1)
			except:
				pass
		lands.append(otr)
		print(otr)
	colors[color] = lands

del(colors['default'])
print([i for i in colors])
with open("tags.html", 'w', encoding="utf-8") as f:
	YEY = ""
	for name in colors:
		lands = colors[name]
		for cords in lands:
			new_cords = []
			for i in cords:
				new_cords+=[str(i[0]), str(i[1])]
			vl = ",".join(new_cords)
			YEY += f'<area shape="poly" coords="{vl}" href="{name}.html" title="{name}" alt="не найдено">\n'
			new_html = f"""<!DOCTYPE html>
				<html>
				<head>
					<meta charset="utf-8">
					<meta name="viewport" content="width=device-width, initial-scale=1">
					<title>{name}</title>
				</head>
				<body>
				    <img src="{name}.png" alt="Не найдено" usemap="#Navigation">
				</body>
				</html>"""
			with open(f"{name}.html", 'w', encoding="utf-8") as ht:
				ht.write(new_html)
	FINAL = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <img src="Карта.png" alt="Не найдено" usemap="#Navigation">
    <map name="Navigation">
        {}
    </map>
</body>
</html>""".format(YEY)
	f.write(FINAL)

with open("COLORS.json", 'w') as f:
	f.write(json.dumps(colors, sort_keys=True, indent=2))