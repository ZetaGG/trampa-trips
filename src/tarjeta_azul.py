"""Tarjeta adhesiva azul estándar (100 x 250 x 1.0 mm) expuesta al aire."""

from cadgen import step, stl, threemf
from lib.parts_factory import make_tarjeta_azul


@step(out="../STEP/tarjeta_azul.step")
@stl(out="../STL/tarjeta_azul.stl")
@threemf(out="../3MF/tarjeta_azul.3mf")
def tarjeta_azul():
    return make_tarjeta_azul()


if __name__ == "__main__":
    tarjeta_azul()
