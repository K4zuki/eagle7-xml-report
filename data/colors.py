import svgwrite
from svgwrite import mm


def basic_shapes(name):
    dwg = svgwrite.Drawing(filename=name, debug=True)
    dwg.stretch()

    symbols = dwg.defs
    symbols.add(dwg.rect(id="white", insert=(0, 0), size=(100, 100), fill="white"))
    symbols.add(dwg.rect(id="navy", insert=(0, 0), size=(100, 100), fill="navy"))
    symbols.add(dwg.rect(id="green", insert=(0, 0), size=(100, 100), fill="green"))
    symbols.add(dwg.rect(id="teal", insert=(0, 0), size=(100, 100), fill="teal"))
    symbols.add(dwg.rect(id="maroon", insert=(0, 0), size=(100, 100), fill="maroon"))
    symbols.add(dwg.rect(id="purple", insert=(0, 0), size=(100, 100), fill="purple"))
    symbols.add(dwg.rect(id="olive", insert=(0, 0), size=(100, 100), fill="olive"))
    symbols.add(dwg.rect(id="gray", insert=(0, 0), size=(100, 100), fill="gray"))
    symbols.add(dwg.rect(id="silver", insert=(0, 0), size=(100, 100), fill="silver"))
    symbols.add(dwg.rect(id="blue", insert=(0, 0), size=(100, 100), fill="blue"))
    symbols.add(dwg.rect(id="lime", insert=(0, 0), size=(100, 100), fill="lime"))
    symbols.add(dwg.rect(id="aqua", insert=(0, 0), size=(100, 100), fill="aqua"))
    symbols.add(dwg.rect(id="red", insert=(0, 0), size=(100, 100), fill="red"))
    symbols.add(dwg.rect(id="fuchsia", insert=(0, 0), size=(100, 100), fill="fuchsia"))
    symbols.add(dwg.rect(id="yellow", insert=(0, 0), size=(100, 100), fill="yellow"))
    symbols.add(dwg.rect(id="black", insert=(0, 0), size=(100, 100), fill="black"))

    table = dwg.g()
    dwg.add(table)
    colors = [
        "white", "navy", "green", "teal", "maroon", "purple", "olive", "gray",
        "silver", "blue", "lime", "aqua", "red", "fuchsia", "yellow", "black",
    ]
    [table.add(dwg.use(href="#"+colors[i], insert=((i % 8)*100, (i//8)*100))) for i in range(16)]
    [table.add(dwg.text("{}".format(i), insert=(50+(i % 8)*100, 50+(i//8)*100), fill=colors[len(colors)-1-i],
                        text_anchor="middle", dominant_baseline="middle")) for i in range(len(colors))]
    [table.add(dwg.line(start=(48+(i % 8)*100, 50+(i//8)*100), end=(52+(i % 8)*100, 50+(i//8)*100),
                        stroke=colors[len(colors)-1-i])) for i in range(len(colors))]
    [table.add(dwg.line(start=(50+(i % 8)*100, 48+(i//8)*100), end=(50+(i % 8)*100, 52+(i//8)*100),
                        stroke=colors[len(colors)-1-i])) for i in range(len(colors))]
    dwg.save(pretty=True)


if __name__ == "__main__":
    basic_shapes("color_table.svg")
