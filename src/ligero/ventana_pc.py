"""Part 3a (Ligero): Ventana óptica transparente (25 x 25 x 2 mm)."""

from cadgen import step, stl, threemf
from lib.parts_ligero import make_ventana_pc_ligero


@step(out="../../STEP/ligero/ventana_pc.step")
@stl(out="../../STL/ligero/ventana_pc.stl")
@threemf(out="../../3MF/ligero/ventana_pc.3mf")
def ventana_pc():
    return make_ventana_pc_ligero()


if __name__ == "__main__":
    ventana_pc()
