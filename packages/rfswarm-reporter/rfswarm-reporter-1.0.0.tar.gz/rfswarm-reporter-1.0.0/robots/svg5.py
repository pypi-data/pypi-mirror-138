# https://youtu.be/bIfNwgUVjV8

# https://github.com/cduck/drawSvg

import drawSvg as draw

import os
import sys
import time
import random


def drawtri(d, p0, p1, p2, c):
	# d.append(draw.Lines(p0[0], p0[1], p1[0], p1[1], p2[0], p2[1], close=False, fill=c, stroke='black'))
	d.append(draw.Lines(p0[0], p0[1], p1[0], p1[1], p2[0], p2[1], fill=c))

def tri_frm_pos(x, y, sz):
    hsz = sz/2
    top = (x, y-hsz)
    lft = (x-hsz, y+hsz)
    rgt = (x+hsz, y+hsz)
    return (top, lft, rgt)

def tri_frm_pos_inv(x, y, sz):
    hsz = sz/2
    top = (x, y+hsz)
    lft = (x-hsz, y-hsz)
    rgt = (x+hsz, y-hsz)
    return (top, lft, rgt)

def midpoint(p1, p2):
	x = (p1[0] + p2[0])/2
	y = (p1[1] + p2[1])/2
	return (x, y)

def sierpinski(d, p0, p1, p2, colr, level):
	pA = midpoint(p0, p1)
	pB = midpoint(p1, p2)
	pC = midpoint(p2, p0)

	if level>1:
		sierpinski(d, p0, pA, pC, colr, level-1)
		sierpinski(d, pC, pB, p2, colr, level-1)
		sierpinski(d, pA, p1, pB, colr, level-1)

	else:

		drawtri(d, p0, pA, pC, colr)
		drawtri(d, pC, pB, p2, colr)
		drawtri(d, pA, p1, pB, colr)


def mkcolour(a,b):
	c = int(a*b)
	while c < 0:
		c += 128
	while c > 255:
		c -= 128
	return c


def mkhexcolour(a,b):
	c1 = mkcolour(a,b)
	c2 = mkcolour(1,b)
	c3 = mkcolour(a,1)
	return '#{:02X}{:02X}{:02X}'.format(c1, c2, c3)


def mkcolourset(exch):
	colourset = []
	exchs = "{}".format(exch)
	# colourset.append("#{}".format(exchs.replace('.', '')))

	excha = exchs.split('.')
	exch1 = int(excha[0])
	exch2 = int(excha[1])
	exch3 = int(exchs.replace('.', ''))

	colourset.append(mkhexcolour(exch3,exch3))
	colourset.append(mkhexcolour(exch1,exch2))

	t = time.localtime()
	# print("t:", t)

	colourset.append(mkhexcolour(t[0],exch3))
	colourset.append(mkhexcolour(t[1],exch3))
	colourset.append(mkhexcolour(t[2],exch3))
	colourset.append(mkhexcolour(t[6],exch3))
	colourset.append(mkhexcolour(t[7]+1,exch3))
	colourset.append(mkhexcolour(t[8]+1,exch3))

	# print("colourset:", colourset)

	random.shuffle(colourset)
	print("colourset:", colourset)

	return colourset


def make_colour():
	hexchr = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
	r1 = hexchr[random.randrange(len(hexchr))]
	r2 = hexchr[random.randrange(len(hexchr))]
	g1 = hexchr[random.randrange(len(hexchr))]
	g2 = hexchr[random.randrange(len(hexchr))]
	b1 = hexchr[random.randrange(len(hexchr))]
	b2 = hexchr[random.randrange(len(hexchr))]
	return "#{}{}{}{}{}{}".format(r1,r2,g1,g2,b1,b2)

def create_drawing(w, h):
	d = draw.Drawing(w, h, origin='center', displayInline=False)
	return d

def save_drawing(drawing, dir):
	ts = time.time()
	filename = "{}_{}".format(dir, ts)

	svgname = "{}.svg".format(filename)
	print("saveSvg:", svgname)
	drawing.saveSvg(svgname)
	pngname = "{}.png".format(filename)
	print("savePng:", pngname)
	drawing.savePng(pngname)
	return (pngname, svgname)


def draw_sierpinski(drawing, colour, size, levels):
	x = 0
	y = 0
	# print("x:", x, "	y:", y, "	tsz:", tsz)
	points = tri_frm_pos(x, y, size)
	# print("points:", points)
	sierpinski(drawing, points[0], points[1], points[2], colour, levels)

def draw_inv_sierpinski(drawing, colour, size, levels):
	x = 0
	y = 0
	# print("x:", x, "	y:", y, "	tsz:", tsz)
	points = tri_frm_pos_inv(x, y, size)
	# print("points:", points)
	sierpinski(drawing, points[0], points[1], points[2], colour, levels)

def draw_dbl_sierpinski(drawing, colour, size, levels):
	draw_sierpinski(drawing, colour, size, levels)
	draw_inv_sierpinski(drawing, colour, size, levels)


def draw_sierpinski_fill(drawing, colour, size, levels):
	x = 0
	y = 0
	print("draw_sierpinski_fill 	x:", x, "	y:", y, "	tsz:", tsz)
	points = tri_frm_pos(x, y, size)
	# print("points:", points)
	sierpinski(drawing, points[0], points[1], points[2], colour, levels)

	# fill right
	offset = points[2][0]
	print("offset:", offset)
	while x < w/2:
		x += offset
		print("x:", x, "	w/2:", w/2)

		# print("x:", x, "	y:", y, "	tsz:", tsz)
		points = tri_frm_pos(x, y, size)
		# print("points:", points)
		sierpinski(drawing, points[0], points[1], points[2], colour, levels)

	# fill left
	x = 0
	while x > (w/2)*-1:
		x -= offset
		print("x:", x, "	(w/2)*-1:", (w/2)*-1)

		# print("x:", x, "	y:", y, "	tsz:", tsz)
		points = tri_frm_pos(x, y, size)
		# print("points:", points)
		sierpinski(drawing, points[0], points[1], points[2], colour, levels)

def draw_inv_sierpinski_fill(drawing, colour, size, levels):
	x = 0
	y = 0
	print("draw_inv_sierpinski_fill 	x:", x, "	y:", y, "	tsz:", tsz)
	points = tri_frm_pos_inv(x, y, size)
	# print("points:", points)
	sierpinski(drawing, points[0], points[1], points[2], colour, levels)

	# fill right
	offset = points[2][0]
	print("offset:", offset)
	while x < w/2:
		x += offset
		print("x:", x, "	w/2:", w/2)

		# print("x:", x, "	y:", y, "	tsz:", tsz)
		points = tri_frm_pos_inv(x, y, size)
		# print("points:", points)
		sierpinski(drawing, points[0], points[1], points[2], colour, levels)

	# fill left
	x = 0
	while x > (w/2)*-1:
		x -= offset
		print("x:", x, "	(w/2)*-1:", (w/2)*-1)

		# print("x:", x, "	y:", y, "	tsz:", tsz)
		points = tri_frm_pos_inv(x, y, size)
		# print("points:", points)
		sierpinski(drawing, points[0], points[1], points[2], colour, levels)


def draw_dbl_sierpinski_fill(drawing, colour, size, levels):
	draw_sierpinski_fill(drawing, colour, size, levels)
	draw_inv_sierpinski_fill(drawing, colour, size, levels)

def choose_pattern():
	patterns = []
	patterns.append([h*4, h*2, h, h/2, h/4, h/8])
	patterns.append([h, h/2, h/4, h/8])
	patterns.append([h*4, h, h/4])
	patterns.append([h*2, h, h/2])
	patterns.append([h/8, h*4, h*2, h, h/2, h/4, h/8])
	patterns.append([h/8, h*2, h, h/2, h/8])
	patterns.append([h/8, h*2, h/2, h/8])

	pattern = random.choice(patterns)
	return pattern


def chooseLevel():
	t = time.localtime()
	# print("t:", t)
	level = t[6]+3
	return level


#
#
#

# 4k
w = 1920 * 2
h = 1080 * 2

# 1080p
# w = 1920
# h = 1080

tsz = h/2

# x = w/2
# y = h/2
x = 0
y = 0


# level = 13
# level = 3
# level = 4
# level = 5
# level = 8
# level = 10
level = chooseLevel()
print("level:", level)


sdb2usd = 6.31
print("sdb2usd:", sdb2usd)




colours = mkcolourset(sdb2usd)

print("colours:", colours)


d = create_drawing(w, h)


pattern = choose_pattern()

print("pattern chosen:", pattern)

# # for tsz in [h/8, h/4, h/2, h, h*2, h*4]:
# for tsz in [h*4, h*2, h, h/2, h/4, h/8]:
i = 0
for tsz in pattern:
# for tsz in [h*4, h*2]:


	# r = mkcolour(random.randint(0,255),tsz)
	# g = mkcolour(random.randint(0,255),tsz)
	# b = mkcolour(random.randint(0,255),tsz)
	# clr = (r, g, b)

	# clr = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
	# clr = make_colour()

	clr = colours[i]
	i += 1

	print("clr:", clr)

	draw_dbl_sierpinski_fill(d, clr, tsz, level)

save_drawing(d, os.path.splitext(os.path.basename(sys.argv[0]))[0])
