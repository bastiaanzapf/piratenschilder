# -*- coding: utf-8 -*-

import cairo
import pango
import pangocairo
import sys
import numpy.random
import io

def render(text,seed,align,fillbackground,linespacing,rotation):

    # Texte ausmessen, um Bildbreite zu bestimmen

    presurf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1, 1)
    precontext = cairo.Context(presurf)
    prepangocairo_context = pangocairo.CairoContext(precontext)
    prelayout = prepangocairo_context.create_layout()

    lines=text.split("\n")
    i=0
    maxw=0
    for line in lines:
        if len(line)==0:
            i=i+1
            continue
        line=line.strip(' \t\n\r')

        prelayout.set_text(line)

        prepangocairo_context.update_layout(prelayout)
        w,h = prelayout.get_size()
        if (w>maxw):
            maxw=w

    # maxw enthält jetzt größte gemessene Breite

    fontsize=25

    # Format des Bilds bestimmen

    HEIGHT=linespacing*(len(lines))+60
    WIDTH=maxw/pango.SCALE+150

    # Bild vorbereiten

    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, int(HEIGHT))

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

    font = pango.FontDescription("Politics Head "+str(fontsize))

    layout.set_font_description(font)

    # noch ein paar Variablen für Abstände

    i=0

    dx=5
    dyu=0
    dyl=4

    dd=1
    dd1=1

    # Zufallszahlengenerator setzen

    numpy.random.seed(int(seed))

    for line in lines:

        # zeile vorbereiten, leere Zeilen überspringen

        line=line.strip(' \t\n\r')

        if len(line)==0:
            i=i+1
            continue

        # text laden

        layout.set_text(line)
        pangocairo_context.update_layout(layout)
        w,h = layout.get_size()

        context.save()
        
        # Position bestimmen

        if align=="left":
            context.translate(50,25+i*linespacing)
        elif align=="center":
            context.translate(WIDTH/2-w/(pango.SCALE*2),25+i*linespacing)
        elif align=="right":
            context.translate(WIDTH-50-w/pango.SCALE,25+i*linespacing)

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

        if (i%2 == 1):
            context.set_source_rgb(52/255.0, 152/255.0, 219/255.0) 
        else:
            context.set_source_rgb(0, 0, 0) 

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
