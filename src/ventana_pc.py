"""Part 3a: Ventana óptica transparente de policarbonato / acrílico (32 x 32 x 2 mm)."""

from cadgen import step, stl, threemf
from lib.parts_factory import make_ventana_pc


@step(out="../STEP/ventana_pc.step")
@stl(out="../STL/ventana_pc.stl")
@threemf(out="../3MF/ventana_pc.3mf")
def ventana_pc():
    return make_ventana_pc()


if __name__ == "__main__":
    ventana_pc()
