"""Part 1: Chasis / Bandeja principal del POD (PETG, sin tornillos)."""

from cadgen import step, stl, threemf
from lib.parts_factory import make_chasis_bandeja


@step(out="../STEP/chasis_bandeja.step")
@stl(out="../STL/chasis_bandeja.stl")
@threemf(out="../3MF/chasis_bandeja.3mf")
def chasis_bandeja():
    return make_chasis_bandeja()


if __name__ == "__main__":
    chasis_bandeja()
