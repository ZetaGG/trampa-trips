"""Part 5: Marco abierto para tarjeta adhesiva azul (10 x 25 cm) con gancho superior balanceado."""

from cadgen import step, stl, threemf
from lib.parts_factory import make_marco_tarjeta


@step(out="../STEP/marco_tarjeta.step")
@stl(out="../STL/marco_tarjeta.stl")
@threemf(out="../3MF/marco_tarjeta.3mf")
def marco_tarjeta():
    return make_marco_tarjeta()


if __name__ == "__main__":
    marco_tarjeta()
