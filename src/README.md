# Modelos CAD — Trampa de Trips Inteligente (Ensamble Sin Tornillos)

Existen **dos familias** del mismo diseño:

| Carpeta | Qué es | Salidas |
| --- | --- | --- |
| `src/` | Diseño **original** (muros de 3.1 mm, macizos llenos) | `STEP/`, `STL/`, `3MF/` |
| `src/ligero/` | **Copia optimizada para imprimir** (mismas medidas y encajes, −46 % material) | `STEP/ligero/`, `STL/ligero/`, `3MF/ligero/` |

## Versión original (`src/`)

| Script | Salidas | Propósito |
| --- | --- | --- |
| `chasis_bandeja.py` | `STEP/chasis_bandeja.step`, `STL/chasis_bandeja.stl`, `3MF/chasis_bandeja.3mf` | Pieza 1: Bandeja principal del POD (`86×172×60` mm nominal) con cámara OV5640 en la cara estrecha frontal, 2 rieles ranurados de `20` mm de alto para las patas inferiores de los pines de la ESP32-S3 (`28×58` mm, pines hacia arriba), túnel de cables bajo la ESP, bahía para batería 12 V 4000 mAh (`70×60×20` mm) detrás de la ESP, cuna para buck (`70×30×20` mm) al fondo, canaleta lateral de cables, cresta macho laberinto y riel inferior en T |
| `tapa_carcasa.py` | `STEP/tapa_carcasa.step`, `STL/tapa_carcasa.stl`, `3MF/tapa_carcasa.3mf` | Pieza 2: Tapa superior con canal hembra laberinto, labio flexible PETG (0.7 mm, Opción B) y 6 clips cantiléver a presión |
| `ventana_pc.py` | `STEP/ventana_pc.step`, ... | Pieza 3a: Ventana óptica transparente (25 × 25 × 2 mm, policarbonato/acrílico) |
| `bisel_ventana.py` | `STEP/bisel_ventana.step`, ... | Pieza 3b: Bisel frontal a presión con 2 clips laterales que prensa la ventana contra el labio PETG |
| `parasol_capucha.py` | `STEP/parasol_capucha.step`, ... | Pieza 4: Parasol antirreflejos y visera de lluvia deslizante sobre guías L |
| `marco_tarjeta.py` | `STEP/marco_tarjeta.step`, ... | Pieza 5: Marco abierto para tarjeta adhesiva azul estándar (10 × 25 cm) con arco y gancho superior balanceado |
| `tarjeta_azul.py` | `STEP/tarjeta_azul.step`, ... | Tarjeta adhesiva azul comercial (100 × 250 × 1.0 mm) expuesta al aire |
| `soporte_base.py` | `STEP/soporte_base.step`, ... | Pieza 6: Soporte base de mesa para presentación y puente óptico a distancia fija (encaje T al POD + encaje a presión al marco) |
| `componentes_internos.py` | `STEP/componentes_internos.step` | Componentes electrónicos de referencia y cables de potencia ruteados |
| `assembly.py` | `STEP/assembly.step`, `3MF/assembly.3mf`, `GLB/assembly.glb` | Ensamble completo con poses cinemáticas (`ensamblado` y `abierto_inspeccion`) |

## Versión ligera (`src/ligero/`)

Mismos nombres de archivo y mismas interfaces; solo cambia el grosor de muros y el vaciado
de los macizos. Requiere `PYTHONPATH=src/ligero`.

| Script | Qué se aligeró |
| --- | --- |
| `chasis_bandeja.py` | Muros 1.8 mm, piso 1.6 mm con ranuras inferiores, rieles de pines tipo puente de 3 apoyos, tabiques y canaleta de 1.2 mm |
| `tapa_carcasa.py` | Techo como cáscara de 2 mm; escalones macizos → borde elevado + placa central; clips y laberinto idénticos |
| `marco_tarjeta.py` | Canales en C de 6.5 × 6.0 mm (el arco y el gancho se mantienen a 8 mm) |
| `soporte_base.py` | Travesaños y patines ahuecados por debajo; columnas en celosía con ventanas en arco |
| `parasol_capucha.py` | Paredes 1.6 mm |
| `bisel_ventana.py` | Placa frontal 1.6 mm |
| `ventana_pc.py`, `tarjeta_azul.py`, `componentes_internos.py` | Sin cambios (referencia geométrica) |
| `assembly.py` | Mismo ensamble y mismas poses cinemáticas |

Construcción: ejecutar `PYTHONPATH=src/ligero python src/ligero/assembly.py` desde la raíz
del proyecto construye el ensamble y todos sus hijos.
