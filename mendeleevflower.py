#!/usr/bin/env python

import drawSvg as svg
import itertools
import csv

d = svg.Drawing(1000,1000, origin='center')


sx, sy = -400, -400

bw, bh = 30, 30


spblock = svg.Group(transform=f"translate(-400,-400)")
fblock = svg.Group(transform=f"translate(-400,0)")
dblock = svg.Group(transform=f"translate(400,-400)")

d.append(spblock)
d.append(fblock)
d.append(dblock)

with open ('elements.csv') as elementscsv:
    rows = csv.reader(elementscsv)
    symbolIdx = None
    atomicNIdx = None
    massIdx = None
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
            element.append(svg.Rectangle(0,0,bw,bh,stroke_width=1,stroke='black', fill='yellow'))
            symbol = svg.Text(data[symbolIdx],10,bw/2,bh/2.5,font_family='sans-serif',text_anchor='middle',fill='black')
            atomicN = svg.Text(data[atomicNIdx],5,2,bh-5,font_family='sans-serif',fill='black')
            mass = svg.Text(data[massIdx],5,2,2,font_family='sans-serif',fill='black')
            element.append(symbol)
            element.append(atomicN)
            element.append(mass)
            spblock.append(element)

d.saveSvg('out.svg')
