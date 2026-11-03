"""Part 6: Soporte base de mesa para presentación y puente óptico a distancia fija (PETG)."""

from cadgen import step, stl, threemf
from lib.parts_factory import make_soporte_base


@step(out="../STEP/soporte_base.step")
@stl(out="../STL/soporte_base.stl")
@threemf(out="../3MF/soporte_base.3mf")
def soporte_base():
    return make_soporte_base()


if __name__ == "__main__":
    soporte_base()
