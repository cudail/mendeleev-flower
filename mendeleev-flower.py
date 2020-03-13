#!/usr/bin/env python

import drawSvg as svg
import csv
import math

d = svg.Drawing(math.sqrt(2)*1000,1000, origin='center')

bw, bh = 60, 60 #box width and height

hh = 12 #header height

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

d.append(svg.Text("Print-out Spiral Mendeleev Flower",30,30,350,font_family='sans-serif',fill='black'))
d.append(svg.Text("Caoimhe Ní Chaoimh",20,30,320,font_family='sans-serif',fill='black'))
d.append(svg.Text("https://github.com/oakreef/mendeleev-flower",12,30,300,font_family='sans-serif',fill='black'))
d.append(svg.Text("Released under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International license",12,30,285,font_family='sans-serif',fill='black'))

d.append(svg.Text("Inspiration: https://chilliant.blogspot.com/2013/06/helical-periodic-table.html",12,670,-440,font_family='sans-serif',fill='black',text_anchor='end'))
d.append(svg.Text("Element data from: https://gist.github.com/GoodmanSciences/c2dd862cd38f21b0ad36b8f96b4bf1ee",12,670,-457,font_family='sans-serif',fill='black',text_anchor='end'))

spblock = svg.Group(transform=f"translate(-650,-400)")
fblock = svg.Group(transform=f"translate(-150,-400)")
dblock = svg.Group(transform=f"translate(-600,-100)")


d.append(spblock)
d.append(fblock)
d.append(dblock)

n=8 #number of elements in a p block row

#slant offset to make the spiral work
angle=math.asin(bh/math.sqrt(bh*bh+n*n*bw*bw))

#offset for sp-block slant
o=bw*math.tan(angle)

# you might wonder about the maths here
# it was entirely by trial and error
spblock.append(svg.Rectangle(bw,-bh*8-o,bw*8,bh*2,stroke_width=2, stroke='black', fill=unknwn))
fblock.append(svg.Rectangle(bw*3,-bh*8-o,bw*10,bh*2,stroke_width=2, stroke='black', fill=unknwn))
dblock.append(svg.Rectangle(bw,-bh*8+2*o,bw*14,bh*2,stroke_width=2, stroke='black', fill=unknwn))

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
        mass_str = data[massIdx]
        if not mass_str:
            mass_str = '?'
        else:
            mass = float(data[massIdx])
            mass_str = mass.is_integer() and f'[{int(mass)}]' or str(mass)

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
            if group==1:
                x=7
            elif group>2:
                x=group-10
            else:
                x=group
            element = svg.Group(transform=f"translate({x*bw},{y*bh+x*o})")
            spblock.append(element)
            element.append(svg.Lines(0,0, 0,bh, bw,bh-o, bw,-o, close=True,stroke_width=2, stroke='black', fill=colour))
            element.append(svg.Text(data[symbolIdx],24,bw/2,bh/3.5,font_family='sans-serif',text_anchor='middle', dominant_baseline='middle',fill='black'))
            element.append(svg.Text(data[atomicNIdx],12,bw/2,bh/3.5+23,text_anchor='middle',font_family='sans-serif',fill='black'))
            element.append(svg.Text(mass_str,8,2,4,transform=f'rotate({math.degrees(angle)})',font_family='sans-serif',fill='black'))

        elif group > 0: #Transition Metals
            if a>108:
                colour = unknwn
            elif group==12:
                colour = posttr #post-transition metals
            else:
                colour = transm
            x=group
            element = svg.Group(transform=f"translate({x*bw},{y*bh+3*o})")
            fblock.append(element)
            element.append(svg.Lines(0,0,0,bh,bw,bh,bw,0,close=True,stroke_width=2, stroke='black', fill=colour))
            element.append(svg.Text(data[symbolIdx],24,bw/2,bh/2.7,font_family='sans-serif',text_anchor='middle', dominant_baseline='middle',fill='black'))
            element.append(svg.Text(data[atomicNIdx],12,bw/2,bh/2.7+23,text_anchor='middle',font_family='sans-serif',fill='black'))
            element.append(svg.Text(mass_str,8,4,4,font_family='sans-serif',fill='black'))

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
            element.append(svg.Text(data[symbolIdx],24,bw/2,bh/2.7,font_family='sans-serif',text_anchor='middle', dominant_baseline='middle',fill='black'))
            element.append(svg.Text(data[atomicNIdx],12,bw/2,bh/2.7+23,text_anchor='middle',font_family='sans-serif',fill='black'))
            element.append(svg.Text(mass_str,8,4,4,font_family='sans-serif',fill='black'))

d.saveSvg('mendeleev-flower.svg')
