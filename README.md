# Trampa de Trips Inteligente 🐛📸

> Detección automática del momento de fumigación contra **trips** mediante una trampa adhesiva azul fotografiada por una cámara, sin WiFi y sin tornillos.

![Estado](https://img.shields.io/badge/estado-prototipo-orange) ![Licencia](https://img.shields.io/badge/licencia-MIT-blue) ![CAD](https://img.shields.io/badge/CAD-cadgen%2Fbuild123d-9cf)

---

## 1. El problema

Los **trips** (orden *Thysanoptera*, ~1 mm de largo) son plagas agrícolas graves: perforan y succionan las células de las plantas (dejando manchas plateadas), y el trips de las flores (*Frankliniella occidentalis*) es vector del virus del bronceado del tomate (TSWV). Se reproducen por partenogénesis y, en invernadero, su población explota en días.

Hoy, el agricultor decide fumigar **contando trips a mano** en trampas adhesivas. Ese conteo es lento, subjetivo y dependiente de que alguien recorra el cultivo.

## 2. Nuestra solución

Una **trampa adhesiva azul** (color más atractivo para los trips) monitoreada por una **cámara OV5640 (5 MP)** controlada por una **ESP32-S3**. La cámara fotografía la tarjeta periódicamente, guarda las imágenes en **microSD** y estima la **densidad/cobertura de trips** para decidir "es hora de fumigar", mostrando un **LED de estado verde/rojo** en el exterior.

- **Sin WiFi:** no requiere infraestructura en el campo (solo microSD).
- **Sin tornillos:** toda la carcasa ensambla a presión (clips snap-fit, deslizantes y fricción).
- **Batería recargable 12 V extraíble:** se carga fuera de la trampa.

## 3. Funcionamiento (flujo)

```
Deep sleep (timer 2–4 h)
   │ despierta
   ▼
Encender LED difuso de iluminación
   ▼
Capturar foto (OV5640)
   ▼
Guardar JPEG en microSD  ──►  análisis fino posterior en PC (OpenCV)
   ▼
Estimar densidad/cobertura de trips en la propia placa
   ▼
LED verde (OK) / LED rojo (FUMIGAR)
   ▼
Volver a deep sleep
```

## 4. Circuito de alimentación

```
Batería 12 V (3S1P 18650, 4000 mAh, ~70×60×20 mm)
   │  conector DC de barril 2.1×5.5 mm (modificable)
   ▼
Interruptor deslizante
   ▼
Buck DC-DC LM2596  (12 V → 3.3 V)
   ▼
ESP32-S3  (pin 3V3 + GND)
   ├── Cámara OV5640 (cinta FPC de 24 pines)
   ├── microSD (fotos)
   └── LED RGB de estado (GPIO)
```

## 5. Lista de materiales (BOM)

| Componente | Cant. | Especificación |
|---|---|---|
| ESP32-S3 (placa de desarrollo) | 1 | 58 × 28 mm, USB-C |
| Cámara OV5640 | 1 | 5 MP, cinta FPC 24 pines |
| Batería recargable de litio | 1 | 12 V, 4000 mAh, 3S1P 18650, ~70×60×20 mm |
| Convertidor Buck | 1 | LM2596 (12 V → 3.3 V), 21 × 43 mm |
| Interruptor deslizante | 1 | SPDT, 8 × 19 mm |
| LED RGB | 1 | 5 mm (estado verde/rojo) |
| LED de iluminación | 2–4 | blancos difusos + transistor |
| Tarjeta adhesiva azul | 1 | 10 × 25 cm (comercial, reemplazable) |
| Bolsa de sílice | 1 | desecante anticondensación |
| Ventana óptica | 1 | policarbonato/acrílico 25 × 25 × 2 mm (cortada) |
| Filamento | — | PETG para todo el cuerpo (no TPU) |

## 6. Piezas impresas (sin tornillos, PETG)

| Pieza | Archivo STL / 3MF | Dimensiones (mm) | Función |
|---|---|---|---|
| **1. Chasis / Bandeja** | `chasis_bandeja` | 122.0 × 133.5 × 50.0 | Bandeja con bahía de batería extraíble, cunas para ESP32-S3, OV5640, LM2596, interruptor, LED y sílice + canales de cableado |
| **2. Tapa / Carcasa** | `tapa_carcasa` | 129.8 × 136.4 × 32.5 | Tapa con sellado laberinto + labio flexible PETG y 6 clips snap-fit |
| **3. Bisel de ventana** | `bisel_ventana` | 43.3 × 5.7 × 32.0 | Retiene la ventana óptica a presión |
| **4. Parasol / Capucha** | `parasol_capucha` | 68.0 × 38.7 × 33.6 | Antirreflejos + visera de lluvia, deslizante |
| **5. Marco de tarjeta** | `marco_tarjeta` | 112.0 × 75.5 × 244.0 | Sostiene la tarjeta azul expuesta + gancho para colgar |
| **6. Soporte base** | `soporte_base` | 128.0 × 244.0 × 114.6 | Base de mesa (presentación) + puente óptico a distancia fija |

> `ventana_pc` (25×25×2 mm) se **corta** en PC/acrílico y `tarjeta_azul` (100×250×1 mm) es la **tarjeta comercial**; ambos se incluyen en los modelos como referencia geométrica.

## 7. Ensamble (sin herramientas)

1. Colocar **cámara OV5640** en la cuna frontal (desliza desde arriba hasta hacer clic).
2. Asentar **ESP32-S3** sobre sus 4 postes y enganchar las uñas de esquina.
3. Insertar la **batería 12 V** en su bahía (las muescas laterales permiten extraerla con índice y pulgar; 2 clips la retienen).
4. Colocar **LM2596, interruptor y LED** en sus bolsillos a presión.
5. **Cablear** siguiendo el corredor-guía central con retenedores.
6. Poner la **sílice** en su jaula ranurada.
7. Colocar **ventana** sobre el labio anular y presionar el **bisel** hasta enganchar.
8. Deslizar el **parasol** por las guías L frontales.
9. Presionar la **tapa** desde arriba: laberinto + labio PETG + 6 clips perimetrales.
10. Deslizar el POD por el riel inferior en T sobre la base y encajar el **marco** con la **tarjeta azul** deslizada desde arriba.

## 8. Sellado (Opción B, sin TPU)

- **Laberinto macho-hembra:** solape perimetral que hace tortuosa la entrada de agua.
- **Labio flexible PETG:** pestaña continua de ~0.7 mm que sella por contacto bajo la precarga de los clips.
- **Desecante (sílice):** evita empañamiento/condensación en la ventana.

Nivel realista: **resistente a lluvia/salpicaduras** (cercano a impermeable), no inmersión.

## 9. Estructura del repositorio

```
trampa-trips/
├── README.md                 # este archivo
├── src/                      # modelos CAD paramétricos (build123d + cadgen)
│   ├── README.md             # catálogo de modelos
│   ├── lib/specs.py          # dimensiones, tolerancias y datums compartidos
│   ├── lib/parts_factory.py  # geometría de cada pieza
│   ├── chasis_bandeja.py
│   ├── tapa_carcasa.py
│   ├── ventana_pc.py
│   ├── bisel_ventana.py
│   ├── parasol_capucha.py
│   ├── marco_tarjeta.py
│   ├── tarjeta_azul.py
│   ├── soporte_base.py
│   ├── componentes_internos.py
│   └── assembly.py           # ensamble completo + poses cinemáticas
├── checks/                   # verificación geométrica y de interferencias
│   └── verify_assembly.py
├── STL/                      # mallas listas para imprimir (laminar)
└── 3MF/                      # archivos 3MF para Bambu Studio / OrcaSlicer
```

## 10. Regenerar los modelos 3D

Los archivos de impresión (STL/3MF) ya están incluidos. Si quieres **regenerarlos o modificar dimensiones**, edita `src/lib/specs.py` y ejecuta (requiere `uv`):

```bash
cd trampa-trips
PYTHONPATH=src uvx --no-config --managed-python --python 3.13 --from cadgen==0.7.21 python src/assembly.py
# verificación geométrica y de interferencias:
uvx --no-config --managed-python --python 3.13 --from cadgen==0.7.21 python checks/verify_assembly.py
```

Todas las cotas clave (tamaño de batería, cámara, placa, tolerancias de snap-fit) viven en `src/lib/specs.py`, de modo que ajustar el diseño a un componente real es cuestión de editar constantes y volver a correr.

## 11. Estado y próximos pasos

- [x] Diseño mecánico completo (6 piezas impresas + ventana + tarjeta).
- [x] Verificación geométrica, topológica y de interferencias (0 colisiones en 171 pares).
- [ ] Impresión PETG y ensamble físico.
- [ ] Firmware ESP32-S3: captura a microSD, deep-sleep, LED de estado, estimación de densidad.
- [ ] Análisis fino de imágenes (OpenCV) en PC para calibrar el umbral de fumigación.

## Licencia

MIT — siéntete libre de usar, modificar y compartir.
