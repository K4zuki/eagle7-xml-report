import svgwrite
from svgwrite import mm


def basic_shapes(name):
    dwg = svgwrite.Drawing(filename="svg.svg", debug=True)
    dwg.viewbox(-500, -500, 1000, 1000)
    # dwg.stretch()
    q1x = 45.72
    q1y = 50.8

    q2x = 76.2
    q2y = 50.8
    symbols = dwg.defs
    origin = dwg.g(id="origin")
    origin.add(dwg.line(start=(-1*mm, 0), end=(1*mm, 0), stroke="maroon", stroke_linecap="round"))
    origin.add(dwg.line(start=(0, -1*mm), end=(0, 1*mm), stroke="maroon", stroke_linecap="round"))
    symbols.add(origin)

    sch = dwg.g(id="schematic")
    sch.add(dwg.use(href="#origin", insert=(0, 0)))
    sch.scale(1, -1)

    # dwg.add(dwg.line(start=(-2*mm, -2*mm), end=(2*mm, 2*mm), stroke="red", stroke_linecap="round"))
    # dwg.add(dwg.line(start=(-2*mm, 2*mm), end=(2*mm, -2*mm), stroke="red", stroke_linecap="round"))
    # dwg.add(dwg.line(start=(0, -2*mm), end=(0, 2*mm), stroke="red", stroke_linecap="round"))
    # dwg.add(dwg.line(start=(-2*mm, 0), end=(2*mm, 0), stroke="red", stroke_linecap="round"))
    # dwg.add(dwg.rect(insert=(-150, -150), size=(300, 300), stroke="black", fill="none", stroke_linecap="round"))

    dwg.add(sch)

    npn = dwg.g(id="NPN")
    npn.add(dwg.use(href="#origin", insert=(0, 0)))
    npn.add(dwg.line(start=(2.54*mm, 2.54*mm), end=(0.508*mm, 1.524*mm), stroke="black", stroke_linecap="round"))
    npn.add(dwg.line(start=(1.778*mm, -1.524*mm), end=(2.54*mm, -2.54*mm), stroke="black", stroke_linecap="round"))
    npn.add(dwg.line(start=(2.54*mm, -2.54*mm), end=(1.27*mm, -2.54*mm), stroke="black", stroke_linecap="round"))
    npn.add(dwg.line(start=(1.27*mm, -2.54*mm), end=(1.778*mm, -1.524*mm), stroke="black", stroke_linecap="round"))
    npn.add(dwg.line(start=(1.54*mm, -2.04*mm), end=(0.308*mm, -1.424*mm), stroke="black", stroke_linecap="round"))
    npn.add(dwg.line(start=(1.524*mm, -2.413*mm), end=(2.286*mm, -2.413*mm), stroke="black", stroke_linecap="round"))
    npn.add(dwg.line(start=(2.286*mm, -2.413*mm), end=(1.778*mm, -1.778*mm), stroke="black", stroke_linecap="round"))
    npn.add(dwg.line(start=(1.778*mm, -1.778*mm), end=(1.524*mm, -2.286*mm), stroke="black", stroke_linecap="round"))
    npn.add(dwg.line(start=(1.524*mm, -2.286*mm), end=(1.905*mm, -2.286*mm), stroke="black", stroke_linecap="round"))
    npn.add(dwg.line(start=(1.905*mm, -2.286*mm), end=(1.778*mm, -2.032*mm), stroke="black", stroke_linecap="round"))
    npn.add(dwg.rect(insert=(-0.254*mm, -2.54*mm), size=((0.508-(-0.254))*mm, (2.54-(-2.54))*mm)))

    npn.add(dwg.line(start=(-2.54*mm, 0), end=(0, 0), stroke="black", stroke_linecap="round"))
    npn.add(dwg.line(start=(2.54*mm, -5.08*mm), end=(2.54*mm, -2.54*mm), stroke="black", stroke_linecap="round"))
    npn.add(dwg.line(start=(2.54*mm, 5.08*mm), end=(2.54*mm, 2.54*mm), stroke="black", stroke_linecap="round"))
    # <pin name="B" x="-2.54" y="0" visible="off" length="short" direction="pas" swaplevel="1"/>
    # <pin name="E" x="2.54" y="-5.08" visible="off" length="short" direction="pas" swaplevel="3" rot="R90"/>
    # <pin name="C" x="2.54" y="5.08" visible="off" length="short" direction="pas" swaplevel="2" rot="R270"/>

    symbols.add(npn)

    npnf = dwg.g(id="NPNF")
    npnf.add(dwg.use(href="#NPN"))
    npnf.scale(-1, 1)
    symbols.add(npnf)

    q1 = dwg.use(href="#NPNF", insert=(q1x*mm, q1y*mm))
    q2 = dwg.use(href="#NPN", insert=(q2x*mm, q2y*mm))

    sch.add(q1)
    sch.add(q2)
    dwg.save(pretty=True)


if __name__ == "__main__":
    basic_shapes("basic_shapes.svg")
