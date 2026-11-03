"""Ensamble completo de la Trampa de Trips Inteligente (sin tornillos, modular)."""

import cadgen
from cadgen import build123d as bd
from cadgen import glb, step, threemf

from bisel_ventana import bisel_ventana
from chasis_bandeja import chasis_bandeja
from componentes_internos import componentes_internos
from lib import specs as sp
from marco_tarjeta import marco_tarjeta
from parasol_capucha import parasol_capucha
from soporte_base import soporte_base
from tapa_carcasa import tapa_carcasa
from tarjeta_azul import tarjeta_azul
from ventana_pc import ventana_pc

KINEMATICS = {
    "mates": [
        cadgen.slider(
            "abrir_tapa",
            parent="#chasis_bandeja",
            child="#tapa_carcasa",
            origin=(0.0, sp.POD_WORLD_Y, sp.POD_WORLD_Z + 38.0),
            direction=(0.0, 0.0, 1.0),
            limits=(0.0, 95.0),
        ),
        cadgen.slider(
            "extraer_bateria_12v",
            parent="#chasis_bandeja",
            child="#bateria_12v_4000mah",
            origin=(sp.BATT_CENTER_X, sp.POD_WORLD_Y + sp.BATT_CENTER_Y, sp.POD_WORLD_Z + 10.0),
            direction=(0.0, 0.0, 1.0),
            limits=(0.0, 60.0),
        ),
        cadgen.slider(
            "deslizar_parasol",
            parent="#chasis_bandeja",
            child="#parasol_capucha",
            origin=(0.0, sp.POD_WORLD_Y + 68.0, sp.POD_WORLD_Z + 20.0),
            direction=(0.0, 0.0, 1.0),
            limits=(0.0, 70.0),
        ),
        cadgen.slider(
            "separar_bisel",
            parent="#chasis_bandeja",
            child="#bisel_ventana",
            origin=(0.0, sp.POD_WORLD_Y + 68.0, sp.POD_WORLD_Z + 15.5),
            direction=(0.0, 1.0, 0.0),
            limits=(0.0, 35.0),
        ),
        cadgen.slider(
            "separar_ventana",
            parent="#chasis_bandeja",
            child="#ventana_pc",
            origin=(0.0, sp.POD_WORLD_Y + 66.0, sp.POD_WORLD_Z + 15.5),
            direction=(0.0, 1.0, 0.0),
            limits=(0.0, 18.0),
        ),
        cadgen.slider(
            "extraer_tarjeta_azul",
            parent="#marco_tarjeta",
            child="#tarjeta_azul",
            origin=(0.0, sp.CARD_WORLD_Y, 138.0),
            direction=(0.0, 0.0, 1.0),
            limits=(0.0, 120.0),
        ),
    ],
    "poses": {
        "ensamblado": {
            "abrir_tapa": 0.0,
            "extraer_bateria_12v": 0.0,
            "deslizar_parasol": 0.0,
            "separar_bisel": 0.0,
            "separar_ventana": 0.0,
            "extraer_tarjeta_azul": 0.0,
        },
        "abierto_inspeccion": {
            "abrir_tapa": 85.0,
            "extraer_bateria_12v": 42.0,
            "deslizar_parasol": 55.0,
            "separar_bisel": 28.0,
            "separar_ventana": 14.0,
            "extraer_tarjeta_azul": 80.0,
        },
    },
}


@step(out="../STEP/assembly.step", kinematics=KINEMATICS)
@threemf(out="../3MF/assembly.3mf")
@glb(out="../GLB/assembly.glb")
def assembly():
    pod_loc = bd.Location((0.0, sp.POD_WORLD_Y, sp.POD_WORLD_Z))

    chasis = pod_loc * chasis_bandeja()
    chasis.label = "chasis_bandeja"

    tapa = pod_loc * tapa_carcasa()
    tapa.label = "tapa_carcasa"

    ventana = pod_loc * ventana_pc()
    ventana.label = "ventana_pc"

    bisel = pod_loc * bisel_ventana()
    bisel.label = "bisel_ventana"

    parasol = pod_loc * parasol_capucha()
    parasol.label = "parasol_capucha"

    elec = pod_loc * componentes_internos()
    elec.label = "componentes_internos"

    base = soporte_base()
    base.label = "soporte_base"

    marco = marco_tarjeta()
    marco.label = "marco_tarjeta"

    tarjeta = tarjeta_azul()
    tarjeta.label = "tarjeta_azul"

    return bd.Compound(
        children=[
            base,
            chasis,
            elec,
            ventana,
            bisel,
            parasol,
            tapa,
            marco,
            tarjeta,
        ],
        label="trampa_trips_assembly",
    )


if __name__ == "__main__":
    assembly()
