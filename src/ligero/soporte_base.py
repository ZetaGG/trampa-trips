"""Part 6 (Ligero): Soporte base ahuecado por debajo y columnas tipo celosía (>55% menos filamento)."""

from cadgen import step, stl, threemf
from lib.parts_ligero import make_soporte_base_ligero


@step(out="../../STEP/ligero/soporte_base.step")
@stl(out="../../STL/ligero/soporte_base.stl")
@threemf(out="../../3MF/ligero/soporte_base.3mf")
def soporte_base():
    return make_soporte_base_ligero()


if __name__ == "__main__":
    soporte_base()
