#!/usr/bin/env python

import drawSvg as svg
import itertools
import csv
import math

d = svg.Drawing(math.sqrt(2)*1000,1000, origin='center')

bw, bh = 60, 60

#Paul Tol's colour palettes - https://personal.sron.nl/~pault/
alkali='#ffaabb'
aearth='#ee8866'
transm='#eedd88'
posttr='#44bb99'
lanthd='#bbcc33'
actind='#aaaa00'
mtloid='#77aadd'
nonmet='#99ddff'
nobleg='#ad6c9f'
unknwn='#dddddd'

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
        a=int(data[atomicNIdx])

        colour = unknwn

        if (group>=1 and group<=2) or (group>=13): #S-Block & P-Block
            if a>108:
                colour = unknwn #unknown
            elif group==1 and period>1: #alkali metal
                colour = alkali
            elif group==18 or (group==2 and period==1): #noble gases
                colour = nobleg
            elif group==2: #alkaline earth metals
                colour = aearth
            elif a in [13,31,49,50,81,82,83,84]:
                colour = posttr #post-transition metals
            elif a in [5,14,32,33,51,52,85]:
                colour = mtloid #metalloids
            elif period==7:
                colour = unknwn #unknown
            else:
                colour = nonmet #nonmetals
            x=group > 2 and group-10 or group
            element = svg.Group(transform=f"translate({x*bw},{y*bh+x*o})")
            spblock.append(element)
            element.append(svg.Lines(0,0, 0,bh, bw,bh-o, bw,-o, close=True,stroke_width=2, stroke='black', fill=colour))
        elif group > 0: #Transition Metals
            if a>108:
                colour = unknwn
            elif group==12:
                colour = posttr #post-transition metals
            else:
                colour = transm
            x=group
            element = svg.Group(transform=f"translate({x*bw},{y*bh})")
            fblock.append(element)
            element.append(svg.Lines(0,0,0,bh,bw,bh,bw,0,close=True,stroke_width=2, stroke='black', fill=colour))
        else: #Lanthanide & Actinides
            if period==6: #lanthanide
                colour = lanthd
                x=a-57
            elif period==7: #actinides
                colour = actind
                x=a-89
            element = svg.Group(transform=f"translate({x*bw},{y*bh})")
            dblock.append(element)
            element.append(svg.Lines(0,0,0,bh,bw,bh,bw,0,close=True,stroke_width=2, stroke='black', fill=colour))
        element.append(svg.Text(data[symbolIdx],10,bw/2,bh/2.5,font_family='sans-serif',text_anchor='middle',fill='black'))
        element.append(svg.Text(data[atomicNIdx],5,2,bh-5,font_family='sans-serif',fill='black'))
        element.append(svg.Text(data[massIdx],5,2,2,font_family='sans-serif',fill='black'))

d.saveSvg('out.svg')
