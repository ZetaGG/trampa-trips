"""Part 3b (Ligero): Bisel retenedor de ventana aligerado."""

from cadgen import step, stl, threemf
from lib.parts_ligero import make_bisel_ventana_ligero


@step(out="../../STEP/ligero/bisel_ventana.step")
@stl(out="../../STL/ligero/bisel_ventana.stl")
@threemf(out="../../3MF/ligero/bisel_ventana.3mf")
def bisel_ventana():
    return make_bisel_ventana_ligero()


if __name__ == "__main__":
    bisel_ventana()
