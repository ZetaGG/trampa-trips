# Versión ligera (`ligero`) — optimizada para imprimir

Copia **independiente** del diseño original con los mismos datums, las mismas medidas
externas, los mismos encajes y las mismas distancias ópticas. Solo se adelgazan muros y se
vacían los macizos que no aportan función mecánica. El objetivo: presentar una pieza que se
vea bien, gaste el mínimo filamento y se imprima rápido.

> Esta carpeta **no modifica** el modelo original de `src/`; es una copia de trabajo.

## Resultado

| Pieza | Original | Ligero | Ahorro |
|---|---:|---:|---:|
| `chasis_bandeja` | 167.9 cm³ | 110.2 cm³ | −34 % |
| `tapa_carcasa` | 133.1 cm³ | 68.4 cm³ | −49 % |
| `marco_tarjeta` | 48.1 cm³ | 30.4 cm³ | −37 % |
| `soporte_base` | 354.7 cm³ | 168.1 cm³ | −53 % |
| `parasol_capucha` | 12.1 cm³ | 8.5 cm³ | −30 % |
| `bisel_ventana` | 2.6 cm³ | 2.1 cm³ | −19 % |
| **Total PETG** | **718.5 cm³** | **387.7 cm³** | **−46 %** |

`ventana_pc` y `tarjeta_azul` no cambian (son referencia geométrica, no se imprimen en PETG).

## Qué se tocó y qué no

### Chasis `chasis_bandeja`
- Muros laterales/frontal/trasero **3.1 → 1.8 mm** (debajo del borde de sellado, que sigue a 4.2 mm).
- Piso **3.0 → 1.6 mm**, aligerado con **ranuras de 12–16 mm** abiertas hacia abajo. Se usan
  ranuras (no un gran bolsillo) para que cada techo sea un puente corto que imprime sin soportes.
- Rieles de pines: de barra maciza a **puente con 3 apoyos** (deja el túnel de cables).
- Tabiques transversales, canaleta lateral y retenedores: **1.6 → 1.2 mm**.
- **Sin cambios:** posición de cámara, altura de los rieles (20 mm), datums de batería/buck,
  ranuras de pines (25.4 mm), clips de batería, riel en T y laberinto macho.

### Tapa `tapa_carcasa`
- Techo macizo → **cáscara de 2 mm** (rebaje interior de 76.6 × 162.6 mm).
- Los dos escalones macizos del techo (44 cm³) → **borde elevado de 5 mm + placa central
  con hueco de placa**; la silueta externa es la misma (tope en z = 69.5 mm).
- Faldón **2.2 → 1.6 mm**.
- **Sin cambios:** laberinto hembra, labio PETG de 0.7 mm y los 6 clips (misma uña, mismo
  enganche a 41–45 mm).

### Soporte base `soporte_base`
- Travesaños y patines ahuecados **por debajo** (canal en C): desde arriba se ve la misma
  superficie lisa, y el material que se quita queda apoyado en la mesa.
- Columnas del pedestal: de bloque macizo a **celosía con 4 ventanas en arco** por columna
  (arcos autoportantes, sin puentes planos largos).
- **Sin cambios:** huella de mesa 128 × 247 mm, torres de encaje del marco, encaje en T del
  POD y altura del puente óptico.

### Marco `marco_tarjeta`
- Canales en C **9.5 × 9.0 → 6.5 × 6.0 mm** (solo la parte alta; el zócalo inferior que
  entra en la base conserva 9.5 × 9.0 mm).
- El **arco y el gancho superior se mantienen a 8 mm** porque de ahí cuelga todo el peso.

## Ajustes de laminado (Bambu Studio / OrcaSlicer)

| Ajuste | Valor | Motivo |
|---|---|---|
| Relleno | **5–8 %** | No es una pieza estructural |
| Patrón | **Lightning** o Gyroid | Solo rellena donde hace falta soportar la capa superior |
| Paredes | **2** | Los muros de 1.8 mm ya son pared pura |
| Capas sólidas arriba/abajo | **2–3** | Ahorra en piso y techo |
| Altura de capa | **0.28 mm** o adaptativa | Velocidad |
| Soportes | **Ninguno** | Todo está diseñado autoportante |
| Brim | 5 mm solo en `soporte_base` | Columnas altas |

## Verificación

```bash
PYTHONPATH=src/ligero uvx --no-config --managed-python --python 3.13 --from cadgen==0.7.21 python src/ligero/assembly.py
uvx --no-config --managed-python --python 3.13 --from cadgen==0.7.21 python checks/verify_ligero.py
```

`checks/verify_ligero.py` comprueba, para las 8 piezas: sólido único, BRep válido, `is_sound`,
0 errores de topología, 0 aristas libres, caja ≤ 256 mm, y compara volumen y *bounding box*
contra el modelo original. Después verifica las 190 parejas del ensamble (0 interferencias).
