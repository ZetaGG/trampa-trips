"""Componentes electrónicos internos de referencia (ESP32-S3, OV5640, Portapilas 4xAA, Buck, Switch, LED, Sílice)."""

from cadgen import step
from lib.parts_factory import make_componentes_internos


@step(out="../STEP/componentes_internos.step")
def componentes_internos():
    return make_componentes_internos()


if __name__ == "__main__":
    componentes_internos()
