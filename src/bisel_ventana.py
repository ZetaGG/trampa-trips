"""Part 3b: Bisel retenedor a presión para la ventana óptica (PETG)."""

from cadgen import step, stl, threemf
from lib.parts_factory import make_bisel_ventana


@step(out="../STEP/bisel_ventana.step")
@stl(out="../STL/bisel_ventana.stl")
@threemf(out="../3MF/bisel_ventana.3mf")
def bisel_ventana():
    return make_bisel_ventana()


if __name__ == "__main__":
    bisel_ventana()
