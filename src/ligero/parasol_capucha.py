"""Part 4 (Ligero): Parasol / Capucha de pared delgada (1.6 mm)."""

from cadgen import step, stl, threemf
from lib.parts_ligero import make_parasol_capucha_ligero


@step(out="../../STEP/ligero/parasol_capucha.step")
@stl(out="../../STL/ligero/parasol_capucha.stl")
@threemf(out="../../3MF/ligero/parasol_capucha.3mf")
def parasol_capucha():
    return make_parasol_capucha_ligero()


if __name__ == "__main__":
    parasol_capucha()
