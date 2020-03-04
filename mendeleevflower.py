#!/usr/bin/env python

import drawSvg as svg
import itertools
import csv
import math

d = svg.Drawing(math.sqrt(2)*1000,1000, origin='center')


sx, sy = -400, -400

bw, bh = 30, 30


spblock = svg.Group(transform=f"translate(-400,-400)")
fblock = svg.Group(transform=f"translate(0,-400)")
dblock = svg.Group(transform=f"translate(-400,0)")

d.append(spblock)
d.append(fblock)
d.append(dblock)

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
        if (group>=1 and group<=2) or (group>=13):
            x=group > 2 and group-10 or group
            y=period
            element = svg.Group(transform=f"translate({x*bw},{y*bh})")
            spblock.append(element)
        elif group > 0:
            x=group
            y=period
            element = svg.Group(transform=f"translate({x*bw},{y*bh})")
            fblock.append(element)
        else:
            a=int(data[atomicNIdx])
            x=period==6 and a-57 or a-89
            y=period
            element = svg.Group(transform=f"translate({x*bw},{y*bh})")
            dblock.append(element)
        element.append(svg.Rectangle(0,0,bw,bh,stroke_width=1,stroke='black', fill='yellow'))
        element.append(svg.Text(data[symbolIdx],10,bw/2,bh/2.5,font_family='sans-serif',text_anchor='middle',fill='black'))
        element.append(svg.Text(data[atomicNIdx],5,2,bh-5,font_family='sans-serif',fill='black'))
        element.append(svg.Text(data[massIdx],5,2,2,font_family='sans-serif',fill='black'))

d.saveSvg('out.svg')
