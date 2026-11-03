# Modelos CAD — Trampa de Trips Inteligente (Ensamble Sin Tornillos)

| Script | Salidas | Propósito |
| --- | --- | --- |
| `chasis_bandeja.py` | `STEP/chasis_bandeja.step`, `STL/chasis_bandeja.stl`, `3MF/chasis_bandeja.3mf` | Pieza 1: Bandeja principal del POD con bahía extraíble para batería 12V 4000mAh (`70×60×20` mm) + muescas de dedos + abrazadera universal de conector, cuna para buck LM2596 (`21×43` mm), ESP32-S3 (`58×28` mm), OV5640, interruptor, LED, sílice, canales de cableado, cresta macho laberinto y riel inferior T |
| `tapa_carcasa.py` | `STEP/tapa_carcasa.step`, `STL/tapa_carcasa.stl`, `3MF/tapa_carcasa.3mf` | Pieza 2: Tapa superior con canal hembra laberinto, labio flexible PETG (0.7 mm, Opción B) y 6 clips cantiléver a presión |
| `ventana_pc.py` | `STEP/ventana_pc.step`, `STL/ventana_pc.stl`, `3MF/ventana_pc.3mf` | Pieza 3a: Ventana óptica transparente (32 × 32 × 2 mm, policarbonato/acrílico) |
| `bisel_ventana.py` | `STEP/bisel_ventana.step`, `STL/bisel_ventana.stl`, `3MF/bisel_ventana.3mf` | Pieza 3b: Bisel frontal a presión con 2 clips laterales que prensa la ventana contra el labio PETG |
| `parasol_capucha.py` | `STEP/parasol_capucha.step`, `STL/parasol_capucha.stl`, `3MF/parasol_capucha.3mf` | Pieza 4: Parasol antirreflejos y visera de lluvia deslizante sobre guías L |
| `marco_tarjeta.py` | `STEP/marco_tarjeta.step`, `STL/marco_tarjeta.stl`, `3MF/marco_tarjeta.3mf` | Pieza 5: Marco abierto para tarjeta adhesiva azul estándar (10 × 25 cm) con arco y gancho superior balanceado |
| `tarjeta_azul.py` | `STEP/tarjeta_azul.step`, `STL/tarjeta_azul.stl`, `3MF/tarjeta_azul.3mf` | Tarjeta adhesiva azul comercial (100 × 250 × 1.0 mm) expuesta al aire |
| `soporte_base.py` | `STEP/soporte_base.step`, `STL/soporte_base.stl`, `3MF/soporte_base.3mf` | Pieza 6: Soporte base de mesa para presentación y puente óptico a distancia fija (encaje T al POD + encaje a presión al marco) |
| `componentes_internos.py` | `STEP/componentes_internos.step` | Componentes electrónicos de referencia en el interior del chasis |
| `assembly.py` | `STEP/assembly.step`, `3MF/assembly.3mf`, `GLB/assembly.glb` | Ensamble completo con poses cinemáticas (`ensamblado` y `abierto_inspeccion`) |

Construcción: ejecutar `PYTHONPATH=src python src/assembly.py` desde la raíz del proyecto construye el ensamble y todos sus hijos.
