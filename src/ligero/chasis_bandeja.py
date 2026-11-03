"""Part 1 (Ligero): Chasis / Bandeja optimizada en peso y tiempo de impresión."""

from cadgen import step, stl, threemf
from lib.parts_ligero import make_chasis_bandeja_ligero


@step(out="../../STEP/ligero/chasis_bandeja.step")
@stl(out="../../STL/ligero/chasis_bandeja.stl")
@threemf(out="../../3MF/ligero/chasis_bandeja.3mf")
def chasis_bandeja():
    return make_chasis_bandeja_ligero()


if __name__ == "__main__":
    chasis_bandeja()
