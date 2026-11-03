"""Tarjeta adhesiva azul estándar (100 x 250 x 1.0 mm)."""

from cadgen import step, stl, threemf
from lib.parts_ligero import make_tarjeta_azul_ligero


@step(out="../../STEP/ligero/tarjeta_azul.step")
@stl(out="../../STL/ligero/tarjeta_azul.stl")
@threemf(out="../../3MF/ligero/tarjeta_azul.3mf")
def tarjeta_azul():
    return make_tarjeta_azul_ligero()


if __name__ == "__main__":
    tarjeta_azul()
