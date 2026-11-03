# Trampa de Trips Inteligente 🐛📸

> Detección automática del momento de fumigación contra **trips** mediante una trampa adhesiva azul fotografiada por una cámara, sin WiFi y sin tornillos.

![Estado](https://img.shields.io/badge/estado-prototipo-orange) ![Licencia](https://img.shields.io/badge/licencia-MIT-blue) ![CAD](https://img.shields.io/badge/CAD-cadgen%2Fbuild123d-9cf)

> **Dos versiones del modelo:** `src/` es el diseño **original** y `src/ligero/` es la versión
> **optimizada para imprimir** (mismas medidas externas y mismos encajes, **−46 % de material**).
> Ver [§7](#7-versión-ligera--optimizada-para-imprimir).

---

## 1. El problema

Los **trips** (orden *Thysanoptera*, ~1 mm de largo) son plagas agrícolas graves: perforan y succionan las células de las plantas (dejando manchas plateadas), y el trips de las flores (*Frankliniella occidentalis*) es vector del virus del bronceado del tomate (TSWV). Se reproducen por partenogénesis y, en invernadero, su población explota en días.

Hoy, el agricultor decide fumigar **contando trips a mano** en trampas adhesivas. Ese conteo es lento, subjetivo y dependiente de que alguien recorra el cultivo.

## 2. Nuestra solución

Una **trampa adhesiva azul** (color más atractivo para los trips) monitoreada por una **cámara OV5640 (5 MP)** controlada por una **ESP32-S3**. La cámara fotografía la tarjeta periódicamente y guarda las imágenes en **microSD**; la **densidad/cobertura** de trips sobre la tarjeta (no el conteo individuo a individuo) define si ya toca fumigar.

- **Sin WiFi:** no requiere infraestructura en el campo; las fotos se revisan luego en el PC.
- **Sin tornillos:** toda la carcasa ensambla a presión (clips snap-fit, correderas y fricción).
- **Batería recargable 12 V extraíble:** se carga fuera de la trampa.
- **Electrónica encerrada, tarjeta al aire:** la tarjeta azul queda expuesta (los trips deben posarse); la electrónica vive en un POD sellado aparte.

## 3. Funcionamiento (flujo)

```
Deep sleep (timer 2–4 h)
   │ despierta
   ▼
Capturar foto (OV5640)
   ▼
Guardar JPEG en microSD  ──►  análisis de densidad/cobertura con OpenCV
   ▼
Si la cobertura de trips supera el umbral  ──►  "FUMIGAR"
   ▼
Volver a deep sleep
```

## 4. Circuito de alimentación

```
Batería 12 V (3S1P 18650, 4000 mAh, ~70×60×20 mm)
   │  conector DC de barril 2.1×5.5 mm (extraíble para cargar)
   ▼
Buck DC-DC (70×30×20 mm, 12 V → 3.3 V)
   ▼
ESP32-S3 (28×58 mm, pines hacia arriba sobre rieles ranurados)
   ├── Cámara OV5640 (cinta FPC de 24 pines, frente estrecho de 86 mm)
   └── microSD (fotos)
```

No hay interruptor, ni LED de estado, ni bolsa de sílice: el equipo va sellado y se
enciende/apaga quitando la batería.

## 5. Lista de materiales (BOM)

| Componente | Cant. | Especificación |
|---|---|---|
| ESP32-S3 (placa de desarrollo) | 1 | 28 × 58 mm, orientada hacia la cámara con pines hacia arriba |
| Cámara OV5640 | 1 | 5 MP, cinta FPC 24 pines |
| Batería recargable de litio | 1 | 12 V, 4000 mAh, 3S1P 18650, ~70×60×20 mm (acostada detrás de la ESP) |
| Convertidor Buck | 1 | 70 × 30 × 20 mm (12 V → 3.3 V, al fondo detrás de la batería) |
| Tarjeta adhesiva azul | 1 | 10 × 25 cm (comercial, reemplazable) |
| Ventana óptica | 1 | policarbonato/acrílico 25 × 25 × 2 mm (cortada) |
| Filamento | — | PETG para todo el cuerpo (no TPU, sin tornillos) |

## 6. Piezas impresas (sin tornillos, PETG — POD nominal `86×172×60` mm)

| Pieza | Archivo STL / 3MF | Dimensiones (mm) | Función |
|---|---|---|---|
| **1. Chasis / Bandeja** | `chasis_bandeja` | 90.0 × 177.5 × 69.0 | Cámara en cara estrecha frontal, 2 rieles ranurados de 20 mm para los pines de la ESP32-S3 (con túnel de cables debajo), bahía de batería 70×60×20 y cuna para buck 70×30×20 al fondo, canaleta lateral de cables y riel inferior en T |
| **2. Tapa / Carcasa** | `tapa_carcasa` | 97.8 × 180.4 × 32.5 | Tapa con sellado laberinto + labio flexible PETG y 6 clips snap-fit |
| **3. Bisel de ventana** | `bisel_ventana` | 43.3 × 5.7 × 32.0 | Retiene la ventana óptica a presión en la cara estrecha frontal |
| **4. Parasol / Capucha** | `parasol_capucha` | 68.0 × 38.7 × 33.6 | Antirreflejos + visera de lluvia, deslizante |
| **5. Marco de tarjeta** | `marco_tarjeta` | 112.0 × 75.5 × 244.0 | Sostiene la tarjeta azul expuesta + gancho para colgar |
| **6. Soporte base** | `soporte_base` | 128.0 × 247.0 × 109.6 | Base de mesa (presentación) + puente óptico a distancia fija |

> `ventana_pc` (25×25×2 mm) se **corta** en PC/acrílico y `tarjeta_azul` (100×250×1 mm) es la **tarjeta comercial**; ambos se incluyen en los modelos como referencia geométrica.

## 7. Versión ligera — optimizada para imprimir

Copia independiente del diseño en `src/ligero/` (salidas en `STL/ligero/` y `3MF/ligero/`).
**Conserva todas las medidas externas, encajes, clips, laberinto y distancias ópticas**,
pero adelgaza muros y vacía los macizos que no aportan nada:

| Pieza | Volumen CAD original | Volumen CAD ligero | Ahorro |
|---|---:|---:|---:|
| Chasis / Bandeja | 167.9 cm³ | 110.2 cm³ | −34 % |
| Tapa / Carcasa | 133.1 cm³ | 68.4 cm³ | −49 % |
| Marco de tarjeta | 48.1 cm³ | 30.4 cm³ | −37 % |
| Soporte base | 354.7 cm³ | 168.1 cm³ | −53 % |
| Parasol | 12.1 cm³ | 8.5 cm³ | −30 % |
| Bisel | 2.6 cm³ | 2.1 cm³ | −19 % |
| **Total 6 piezas PETG** | **718.5 cm³** | **387.7 cm³** | **−46 %** |

Qué cambia (y qué no):

- **Chasis:** muros 3.1 → **1.8 mm**, piso 3.0 → **1.6 mm** (aligerado con ranuras
  inferiores de 12–16 mm, puentes cortos y seguros), rieles de pines macizos → **puente
  de 3 apoyos**, tabiques y canaleta 1.6 → **1.2 mm**. Mismos datums de cámara, ESP,
  batería y buck.
- **Tapa:** techo macizo → **cáscara de 2 mm**; los dos escalones decorativos se
  convierten en **borde elevado + placa central** (misma silueta, 44 cm³ menos). El
  laberinto, el labio PETG y los 6 clips quedan **idénticos**.
- **Soporte base:** los travesaños y patines se ahuecan **por debajo** (invisible desde
  arriba) y las columnas pasan a **celosía con ventanas en arco** (autoportantes).
  La huella de mesa (128 × 247 mm) y los encajes POD/marco no cambian.
- **Marco:** canales en C 9.5 × 9.0 → **6.5 × 6.0 mm**; el arco y el gancho superior
  (donde cuelga todo el peso) se mantienen a 8 mm.

> ⚠️ El **volumen CAD no es el filamento real**: al laminar, el interior se rellena con
> *infill*. Para exprimir la versión ligera usa también estos ajustes.

### Ajustes de laminado recomendados (Bambu Studio / OrcaSlicer)

| Ajuste | Valor | Por qué |
|---|---|---|
| Densidad de relleno | **5–8 %** | El mayor ahorro; no es una pieza estructural |
| Patrón de relleno | **Lightning** (o Gyroid) | Rellena solo donde la capa superior lo necesita |
| Paredes / perímetros | **2** | Los muros de 1.8 mm ya son paredes puras |
| Capas sólidas arriba / abajo | **2–3** | Menos material en el piso y el techo |
| Altura de capa | **0.28 mm** (o adaptativa) | Imprime más rápido |
| Soportes | **Ninguno** | Todas las piezas están diseñadas autoportantes |
| Brim | 5 mm solo en `soporte_base` | Columnas altas y delgadas |

Con esto, la base y la tapa bajan a la mitad de tiempo y peso frente a la versión original.

## 8. Ensamble (sin herramientas)

1. Colocar la **cámara OV5640** en la cuna frontal (desliza desde arriba hasta hacer clic).
2. Asentar la **ESP32-S3** sobre los dos rieles ranurados (los pines quedan hacia arriba).
3. Insertar la **batería 12 V** en su bahía (2 clips la retienen; se extrae con los dedos).
4. Colocar el **buck** en su cuna al fondo.
5. **Cablear:** 12 V por la canaleta lateral derecha (batería → buck) y 3.3 V por el túnel
   bajo la ESP (buck → pines del header). Los retenedores dejan el cable tendido.
6. Colocar la **ventana** sobre su labio y presionar el **bisel** hasta enganchar.
7. Deslizar el **parasol** por las guías L frontales.
8. Presionar la **tapa** desde arriba: laberinto + labio PETG + 6 clips perimetrales.
9. Deslizar el POD por el riel en T sobre la base y encajar el **marco** con la **tarjeta azul** deslizada desde arriba.

## 9. Sellado (Opción B, sin TPU)

- **Laberinto macho-hembra:** solape perimetral que hace tortuosa la entrada de agua.
- **Labio flexible PETG:** pestaña continua de ~0.7 mm que sella por contacto bajo la precarga de los clips.

Nivel realista: **resistente a lluvia/salpicaduras** (cercano a impermeable), no inmersión.

## 10. Estructura del repositorio

```
trampa-trips/
├── README.md                    # este archivo
├── src/                         # modelos CAD paramétricos (build123d + cadgen)
│   ├── README.md                # catálogo de modelos
│   ├── lib/specs.py             # dimensiones, tolerancias y datums compartidos
│   ├── lib/parts_factory.py     # geometría de cada pieza (versión original)
│   ├── chasis_bandeja.py        # … una entrada por pieza
│   ├── componentes_internos.py
│   ├── assembly.py              # ensamble completo + poses cinemáticas
│   └── ligero/                  # ⇦ versión optimizada para imprimir
│       ├── README.md            # qué se aligeró y ajustes de slicer
│       ├── lib/specs_ligero.py  # specs idénticas (mismos datums)
│       ├── lib/parts_ligero.py  # geometría aligerada
│       └── assembly.py
├── checks/
│   ├── verify_assembly.py       # verificación del modelo original
│   └── verify_ligero.py         # verificación + comparación de volumen y medidas
├── STL/  · STL/ligero/          # mallas listas para imprimir
└── 3MF/  · 3MF/ligero/          # archivos 3MF para Bambu Studio / OrcaSlicer
```

## 11. Regenerar los modelos 3D

Los archivos de impresión (STL/3MF) ya están incluidos. Si quieres **regenerarlos o
modificar dimensiones**, edita las specs y ejecuta (requiere `uv`):

```bash
cd trampa-trips

# Versión original
PYTHONPATH=src uvx --no-config --managed-python --python 3.13 --from cadgen==0.7.21 python src/assembly.py
uvx --no-config --managed-python --python 3.13 --from cadgen==0.7.21 python checks/verify_assembly.py

# Versión ligera (optimizada para imprimir)
PYTHONPATH=src/ligero uvx --no-config --managed-python --python 3.13 --from cadgen==0.7.21 python src/ligero/assembly.py
uvx --no-config --managed-python --python 3.13 --from cadgen==0.7.21 python checks/verify_ligero.py
```

Todas las cotas clave (tamaño de batería, cámara, placa, tolerancias de snap-fit) viven en
`src/lib/specs.py` (o `src/ligero/lib/specs_ligero.py`), de modo que ajustar el diseño a un
componente real es cuestión de editar constantes y volver a correr.

## 12. Estado y próximos pasos

- [x] Diseño mecánico completo (6 piezas impresas + ventana + tarjeta).
- [x] Verificación geométrica, topológica y de interferencias (0 colisiones en 190 pares).
- [x] Versión ligera para impresión (−46 % de material, mismas medidas).
- [ ] Impresión PETG y ensamble físico.
- [ ] Firmware ESP32-S3: captura a microSD, deep-sleep, estimación de densidad.
- [ ] Análisis de imágenes (OpenCV) en PC para calibrar el umbral de fumigación.

## Licencia

MIT — siéntete libre de usar, modificar y compartir.
