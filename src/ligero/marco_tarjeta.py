"""Part 5 (Ligero): Marco para tarjeta azul aligerado con gancho superior."""

from cadgen import step, stl, threemf
from lib.parts_ligero import make_marco_tarjeta_ligero


@step(out="../../STEP/ligero/marco_tarjeta.step")
@stl(out="../../STL/ligero/marco_tarjeta.stl")
@threemf(out="../../3MF/ligero/marco_tarjeta.3mf")
def marco_tarjeta():
    return make_marco_tarjeta_ligero()


if __name__ == "__main__":
    marco_tarjeta()
