
import cairo
import pango
import pangocairo
import sys
import numpy.random
import io

def render(text,seed):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 400, 140)
    context = cairo.Context(surf)

    #draw a background rectangle:

    context.rectangle(0,0,500,500)
    context.set_source_rgb(0, 0, 0)
    context.fill()

    #get font families:

    font_map = pangocairo.cairo_font_map_get_default()
    families = font_map.list_families()

    # to see family names:
    for f in font_map.list_families():
        print f.get_name()

    context.set_antialias(cairo.ANTIALIAS_GRAY)

    # Positions drawing origin so that the text desired top-let corner is at 0,0

    pangocairo_context = pangocairo.CairoContext(context)
    pangocairo_context.set_antialias(cairo.ANTIALIAS_GRAY)

    layout = pangocairo_context.create_layout()

#    text="piratenpartei\nflausch oder was!"
    #fontname = sys.argv[1] if len(sys.argv) >= 2 else "Sans"
    font = pango.FontDescription("Politics Head 25")
#    font = pango.FontDescription("Dirty Headline 25")
    layout.set_font_description(font)

    lines=text.split("\n")

    i=0

    dx=5
    dyu=0
    dyl=4

    dd=1
    dd1=1

    numpy.random.seed(int(seed))

    for line in lines:
        if len(line)==0:
            i=i+1
            continue
        line=line.strip(' \t\n\r')
        context.save()
        context.translate(50,25+i*30)

        rotation=numpy.random.random()*0.2-0.1
        context.rotate(rotation)
        i=i+1
        layout.set_text(line)
        print line

        pangocairo_context.update_layout(layout)
        w,h = layout.get_size()
#        print w/pango.SCALE, h/pango.SCALE

        context.set_source_rgb(1, 1, 1) 
        context.rectangle(-dx-dd*numpy.random.random()-dd1,
                           dyu-dd*numpy.random.random()-dd1,
                           w/pango.SCALE+dx*2+2*dd*numpy.random.random()+dd1*2, 
                           h/pango.SCALE+dyl-dyu+2*dd*numpy.random.random()+dd1*2)
        context.fill()

        if (i%2 == 1):
            context.set_source_rgb(52/255.0, 152/255.0, 219/255.0) 
        else:
            context.set_source_rgb(0, 0, 0) 

        context.rectangle(-dx,dyu,w/pango.SCALE+dx*2, h/pango.SCALE+dyl-dyu)
        context.fill()


        context.set_source_rgb(255, 255, 255)
        pangocairo_context.show_layout(layout)
        context.restore()

        
    image_string=io.BytesIO()
    surf.write_to_png(image_string)
    val=image_string.getvalue()
    image_string.close()
    return val
