"""Componentes electrónicos internos y cables de referencia (Ligero)."""

from cadgen import step
from lib.parts_ligero import make_componentes_internos_ligero


@step(out="../../STEP/ligero/componentes_internos.step")
def componentes_internos():
    return make_componentes_internos_ligero()


if __name__ == "__main__":
    componentes_internos()
