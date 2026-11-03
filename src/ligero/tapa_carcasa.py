"""Part 2 (Ligero): Tapa superior ahuecada (cáscara de 1.8 mm) con sello laberinto + labio PETG."""

from cadgen import step, stl, threemf
from lib.parts_ligero import make_tapa_carcasa_ligero


@step(out="../../STEP/ligero/tapa_carcasa.step")
@stl(out="../../STL/ligero/tapa_carcasa.stl")
@threemf(out="../../3MF/ligero/tapa_carcasa.3mf")
def tapa_carcasa():
    return make_tapa_carcasa_ligero()


if __name__ == "__main__":
    tapa_carcasa()
