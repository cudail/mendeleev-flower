#!/usr/bin/env python

import drawSvg as svg
import itertools
import csv
import math

d = svg.Drawing(math.sqrt(2)*1000,1000, origin='center')

bw, bh = 60, 60

spblock = svg.Group(transform=f"translate(-650,-400)")
fblock = svg.Group(transform=f"translate(-150,-400)")
dblock = svg.Group(transform=f"translate(-600,-100)")

d.append(spblock)
d.append(fblock)
d.append(dblock)

n=8 #number of elements in a p block row

#slant offset to make the spiral work
o=bw*math.tan(math.asin(bh/math.sqrt(bh*bh+n*n*bw*bw)))

with open ('elements.csv') as elementscsv:
    rows = csv.reader(elementscsv)
    for i, data in enumerate(rows):
        if i == 0:
            symbolIdx = data.index("Symbol")
            atomicNIdx = data.index("Atomic Number")
            massIdx = data.index("Atomic Mass")
            periodIdx = data.index("Period")
            groupIdx = data.index("Group")
            continue

        group = int(data[groupIdx] or -1)
        period = int(data[periodIdx] or -1)
        y=period
        if (group>=1 and group<=2) or (group>=13):
            x=group > 2 and group-10 or group
            element = svg.Group(transform=f"translate({x*bw},{y*bh+x*o})")
            spblock.append(element)
            element.append(svg.Lines(0,0, 0,bh, bw,bh-o, bw,-o, close=True,stroke_width=2, stroke='black', fill='yellow'))
        elif group > 0:
            x=group
            element = svg.Group(transform=f"translate({x*bw},{y*bh})")
            fblock.append(element)
            element.append(svg.Lines(0,0,0,bh,bw,bh,bw,0,close=True,stroke_width=2, stroke='black', fill='yellow'))
        else:
            a=int(data[atomicNIdx])
            x=period==6 and a-57 or a-89
            element = svg.Group(transform=f"translate({x*bw},{y*bh})")
            dblock.append(element)
            element.append(svg.Lines(0,0,0,bh,bw,bh,bw,0,close=True,stroke_width=2, stroke='black', fill='yellow'))
        element.append(svg.Text(data[symbolIdx],10,bw/2,bh/2.5,font_family='sans-serif',text_anchor='middle',fill='black'))
        element.append(svg.Text(data[atomicNIdx],5,2,bh-5,font_family='sans-serif',fill='black'))
        element.append(svg.Text(data[massIdx],5,2,2,font_family='sans-serif',fill='black'))

d.saveSvg('out.svg')
