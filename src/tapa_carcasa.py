"""Part 2: Tapa / Carcasa superior con sello laberinto + labio flexible PETG y 6 clips snap-fit."""

from cadgen import step, stl, threemf
from lib.parts_factory import make_tapa_carcasa


@step(out="../STEP/tapa_carcasa.step")
@stl(out="../STL/tapa_carcasa.stl")
@threemf(out="../3MF/tapa_carcasa.3mf")
def tapa_carcasa():
    return make_tapa_carcasa()


if __name__ == "__main__":
    tapa_carcasa()
