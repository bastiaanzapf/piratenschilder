# -*- coding: utf-8 -*-

import cairo
import pango
import pangocairo
import sys
import numpy.random
import io
import re
from copy import copy

def webcolortosource(context,webcolor):
    RE_HEX=re.compile("([0-9a-fA-F]{2})([0-9a-fA-F]{2})([0-9a-fA-F]{2})")

    r=int(RE_HEX.search(webcolor).group(1),16)
    g=int(RE_HEX.search(webcolor).group(2),16)
    b=int(RE_HEX.search(webcolor).group(3),16)

    context.set_source_rgb(r/255.0, g/255.0, b/255.0) 

# Entgegen der Tradition ist diese Funktion sehr lang
# Ich akzeptiere jedes vernünftige "Refactoring" als gültige Kritik

def render(text,seed,align,fillbackground,linespacing,
           rotation,backgroundcolors):

    # Texte ausmessen, um Bildbreite zu bestimmen

    presurf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1, 1)
    precontext = cairo.Context(presurf)
    prepangocairo_context = pangocairo.CairoContext(precontext)
    prelayout = prepangocairo_context.create_layout()

    lines=text.split("\n")
    i=0
    maxw=0
    dxtick=10
    
    font="Politics Head "
    fontsizes=[15,20,25,30,35]

    linesattributes=[]

    RE_CONTROL=re.compile("^.*|")
    RE_FONTSIZE=re.compile("[1-5]")
    RE_BGCOL=re.compile("[a-e]")

    bgcolmap={}
    bgcolmap['a']=0
    bgcolmap['b']=1
    bgcolmap['c']=2
    bgcolmap['d']=3
    bgcolmap['e']=4

    linedefaults={}
    linedefaults['fontsize']=fontsizes[3]
    linedefaults['dx']=0
    linedefaults['backgroundcolor']='000000';

    backgroundcolors.insert(0,'000000') # schwarz als erste hintergrundfarbe

    # Erster Durchlauf durch alle Zeilen: Dimensionen bestimmen,
    # Steuerzeichen auswerten

    for line in lines:
        if len(line)==0:
            i=i+1
            continue
        line=line.strip(' \t\n\r')

        lineattributes=copy(linedefaults)

        control=RE_CONTROL.search(line).group(0)
        if (control):
            fontsize=RE_FONTSIZE.search(control)
            if (fontsize):
                lineattributes['fontsize']=fontsizes[int(fontsize.group(0))]

            backgroundcolor=RE_BGCOL.search(control)
            if (backgroundcolor):
#                print backgroundcolors
#                print backgroundcolor.group(0)
#                print bgcolmap[backgroundcolor.group(0)]
                lineattributes['backgroundcolor']=backgroundcolors[bgcolmap[backgroundcolor.group(0)]]
            else:
                if (i % 2 == 0):
                    lineattributes['backgroundcolor']=backgroundcolors[0]
                else:
                    lineattributes['backgroundcolor']=backgroundcolors[1]

            lineattributes['dx']=(control.count('>')-control.count('<'))*dxtick

        linesattributes.append(lineattributes)

        # Text abmessen

        prelayout.set_text(line)
        font = pango.FontDescription("Politics Head "+str(lineattributes['fontsize']))

        prelayout.set_font_description(font)

        prepangocairo_context.update_layout(prelayout)
        w,h = prelayout.get_size()

        if (w>maxw):
            maxw=w



    # maxw enthält jetzt größte gemessene Breite

    fontsize=25

    # Format des Bilds bestimmen

    HEIGHT=int(linespacing*(len(lines))+60)
    WIDTH=maxw/pango.SCALE+150

    # Bild vorbereiten

    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)

    context = cairo.Context(surf)

    pangocairo_context = pangocairo.CairoContext(context)
    pangocairo_context.set_antialias(cairo.ANTIALIAS_GRAY)

    if (fillbackground):
        context.rectangle(0,0,WIDTH,HEIGHT)
        context.set_source_rgb(0, 0, 0)
        context.fill()


    font_map = pangocairo.cairo_font_map_get_default()
    families = font_map.list_families()

    context.set_antialias(cairo.ANTIALIAS_GRAY)

    layout = pangocairo_context.create_layout()

    # noch ein paar Variablen für Abstände

    i=0

    dx=5
    dyu=0
    dyl=4

    dd=1
    dd1=1

    # Zufallszahlengenerator setzen

    numpy.random.seed(int(seed))

    # Zweiter Durchlauf durch alle Zeilen: Text setzen

    for line in lines:
        
        # zeile vorbereiten, leere Zeilen überspringen

        line=line.strip(' \t\n\r')
        line=re.sub(r'^([^\|]*\|)?(.*)','\\2',line)

#        print i
#        print linespacing

        if len(line)==0:
            i=i+1
            continue

        font = pango.FontDescription("Politics Head "+str(linesattributes[i]['fontsize']))

        layout.set_font_description(font)

        # text laden

        layout.set_text(line)
        pangocairo_context.update_layout(layout)
        w,h = layout.get_size()

        context.save()
        
        # Position bestimmen

        shiftx=linesattributes[i]['dx']

#        print "Align: "+align

        if align=="left":
            context.translate(50+shiftx,25+i*linespacing)
        elif align=="center":
            context.translate(WIDTH/2-w/(pango.SCALE*2)+shiftx,25+i*linespacing)
        elif align=="right":
            context.translate(WIDTH-50-w/pango.SCALE+shiftx,25+i*linespacing)

        # Rotation

        linerot=numpy.random.random()*2*rotation-rotation
        context.rotate(linerot)

        # Weißer Hintergrund

        context.set_source_rgb(1, 1, 1) 
        context.rectangle(-dx-dd*numpy.random.random()-dd1,
                           dyu-dd*numpy.random.random()-dd1,
                           w/pango.SCALE+dx*2+2*dd*numpy.random.random()+dd1*2, 
                           h/pango.SCALE+dyl-dyu+2*dd*numpy.random.random()+dd1*2)
        context.fill()

        # Farbiger Hintergrund

        webcolortosource(context,linesattributes[i]['backgroundcolor'])

        context.rectangle(-dx,dyu,w/pango.SCALE+dx*2, h/pango.SCALE+dyl-dyu)
        context.fill()

        # Text in Weiß

        context.set_source_rgb(255, 255, 255)
        pangocairo_context.show_layout(layout)

        context.restore()

        i=i+1

    # Bild als String zurückgeben
        
    image_string=io.BytesIO()
    surf.write_to_png(image_string)
    val=image_string.getvalue()
    image_string.close()

    return val
