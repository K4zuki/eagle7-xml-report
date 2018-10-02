import svgwrite


def basic_shapes(name):
    mm = 10
    dwg = svgwrite.Drawing(filename=name, debug=True)
    dwg.viewbox(0, -1200, 1500, 1500)
    q1x = 45.72
    q1y = 50.8

    q2x = 76.2
    q2y = 50.8
    symbols = dwg.defs

    sch = dwg.g(id="schematic")
    sch.add(dwg.use(href="#origin", insert=(0, 0)))
    dwg.add(sch)

    shape = dwg.g(id="NPN-shape")
    symbols.add(shape)
    # Wire
    shape.add(dwg.line(start=(2.54 * mm, 2.54 * mm), end=(0.508 * mm, 1.524 * mm), stroke="black"))
    shape.add(dwg.line(start=(1.778 * mm, -1.524 * mm), end=(2.54 * mm, -2.54 * mm), stroke="black"))
    shape.add(dwg.line(start=(2.54 * mm, -2.54 * mm), end=(1.27 * mm, -2.54 * mm), stroke="black"))
    shape.add(dwg.line(start=(1.27 * mm, -2.54 * mm), end=(1.778 * mm, -1.524 * mm), stroke="black"))
    shape.add(dwg.line(start=(1.54 * mm, -2.04 * mm), end=(0.308 * mm, -1.424 * mm), stroke="black"))
    shape.add(dwg.line(start=(1.524 * mm, -2.413 * mm), end=(2.286 * mm, -2.413 * mm), stroke="black"))
    shape.add(dwg.line(start=(2.286 * mm, -2.413 * mm), end=(1.778 * mm, -1.778 * mm), stroke="black"))
    shape.add(dwg.line(start=(1.778 * mm, -1.778 * mm), end=(1.524 * mm, -2.286 * mm), stroke="black"))
    shape.add(dwg.line(start=(1.524 * mm, -2.286 * mm), end=(1.905 * mm, -2.286 * mm), stroke="black"))
    shape.add(dwg.line(start=(1.905 * mm, -2.286 * mm), end=(1.778 * mm, -2.032 * mm), stroke="black"))
    # Rectangle
    shape.add(dwg.rect(insert=(-0.254 * mm, -2.54 * mm), size=((0.508 - (-0.254)) * mm, (2.54 - (-2.54)) * mm)))
    # Pin
    shape.add(dwg.line(start=(-2.54 * mm, 0), end=(0, 0), stroke="black"))
    shape.add(dwg.line(start=(2.54 * mm, -5.08 * mm), end=(2.54 * mm, -2.54 * mm), stroke="black"))
    shape.add(dwg.line(start=(2.54 * mm, 5.08 * mm), end=(2.54 * mm, 2.54 * mm), stroke="black"))
    # Flip
    shape.scale(1, -1)

    symbols.add(dwg.text(id="NPN-text1", text=">NAME", insert=(0, 0), font_size=1.778 * mm))
    symbols.add(dwg.text(id="NPN-text2", text=">VALUE", insert=(0, 0), font_size=1.778 * mm))

    npn = dwg.g(id="NPN")
    npn.add(dwg.use(href="#origin", insert=(0, 0)))
    npn.add(dwg.use(href="#NPN-shape"))
    npn.add(dwg.use(href="#NPN-text1", insert=(-10.16 * mm, -7.62 * mm)))
    npn.add(dwg.use(href="#NPN-text2", insert=(-10.16 * mm, -5.08 * mm)))
    symbols.add(npn)

    npnf = dwg.g(id="NPNF")
    npnf.add(dwg.use(href="#origin", insert=(0, 0)))
    npnf_shape = dwg.use(href="#NPN-shape", transform="scale(-1,1)")

    npnf.add(npnf_shape)
    npnf.add(dwg.use(href="#NPN-text1", insert=(10.16 * mm, -7.62 * mm), text_anchor="end"))
    npnf.add(dwg.use(href="#NPN-text2", insert=(10.16 * mm, -5.08 * mm), text_anchor="end"))
    symbols.add(npnf)

    q1 = dwg.use(href="#NPNF", insert=(q1x * mm, -q1y * mm),
                 transform="rotate(90 {cx} {cy})".format(cx=q1x * mm, cy=-q1y * mm))
    dwg.add(dwg.use(href="#origin", insert=(q1x * mm, -q1y * mm)))

    q2 = dwg.use(href="#NPN", insert=(q2x * mm, -q2y * mm),
                 transform="rotate(90 {cx} {cy})".format(cx=q2x * mm, cy=-q2y * mm))

    origin = dwg.g(id="origin")
    origin.add(dwg.line(start=(-1 * mm, 0), end=(1 * mm, 0), stroke="maroon"))
    origin.add(dwg.line(start=(0, -1 * mm), end=(0, 1 * mm), stroke="maroon"))
    symbols.add(origin)

    sch.add(q1)
    sch.add(q2)
    dwg.save(pretty=True)


if __name__ == "__main__":
    basic_shapes("basic_shapes.svg")
