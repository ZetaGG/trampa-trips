"""Part 4: Parasol / Capucha antirreflejos y visera de lluvia (deslizante en guías L)."""

from cadgen import step, stl, threemf
from lib.parts_factory import make_parasol_capucha


@step(out="../STEP/parasol_capucha.step")
@stl(out="../STL/parasol_capucha.stl")
@threemf(out="../3MF/parasol_capucha.3mf")
def parasol_capucha():
    return make_parasol_capucha()


if __name__ == "__main__":
    parasol_capucha()
