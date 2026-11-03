"""Shared dimensions, tolerances, coordinate datums, and component factories.

Coordinate convention:
- Pod-local coordinates (x, y, z):
  - Origin (0, 0, 0) is the center of the interior floor of `chasis_bandeja`.
  - +y points toward the front camera window (optical axis).
  - +z points upward toward `tapa_carcasa`.
  - x is left-right symmetric.
- Assembly world coordinates (X, Y, Z):
  - Z = 0.0 is the flat classroom table surface (`soporte_base` bottom).
  - Pod origin (0, 0, 0) sits at World (0.0, POD_WORLD_Y, POD_WORLD_Z) = (0.0, -110.0, 118.0).
  - Camera window front is at World Y ≈ -42.35 mm, optical center at World Z = 133.5 mm.
  - Blue sticky card (`100 x 250 x 1.0` mm) sits vertically at World Y = +85.0 mm,
    centered at World Z = 138.0 mm (Z from 13.0 to 263.0 mm), giving an unobstructed
    ~126.85 mm optical working distance for the 70° FOV OV5640 camera to image the card.
"""

from __future__ import annotations

# --- Print & Snap-Fit Tolerances (mm) ---
CLEARANCE = 0.30          # General sliding / mating clearance per side
SEAL_CLEARANCE = 0.25     # Labyrinth & wiper lip nominal CAD clearance
PETG_LIP_THICKNESS = 0.70 # Option B compliant PETG wiper blade thickness (1.5-2 perimeters)

# --- Pod Main Dimensions (Pod-Local Frame) ---
INNER_X = 108.0           # Interior width at top rim (accommodates 70x60x20 12V pack + LM2596 + ESP32-S3)
INNER_Y = 118.0           # Interior length at top rim
INNER_Z = 38.0            # Interior cavity height from floor (z=0) to rim (z=38)
RIM_WIDTH = 5.0           # Top rim width for Option B Labyrinth + PETG lip
FLOOR_T = 3.0             # Chassis bottom floor thickness (z = -3.0 .. 0.0)

OUTER_X = INNER_X + 2.0 * RIM_WIDTH  # 118.0 mm (x in [-59, +59])
OUTER_Y = INNER_Y + 2.0 * RIM_WIDTH  # 128.0 mm (y in [-64, +64])

# Option B Labyrinth & Wiper Lip Parameters at z = INNER_Z (38.0 mm)
GROOVE_OFFSET_IN = 1.0
GROOVE_OFFSET_OUT = 2.6
GROOVE_DEPTH = 3.5

RIDGE_OFFSET_IN = 2.6
RIDGE_OFFSET_OUT = 3.8
RIDGE_HEIGHT = 3.0

# Lid (`tapa_carcasa`) mating heights in Pod-Local Frame:
LID_CEILING_Z = INNER_Z + 0.40       # 38.4 mm (0.4 mm axial gap over rim ledge)
LID_SKIRT_BOTTOM_Z = INNER_Z - 3.50  # 34.5 mm
LID_SKIRT_THICK = 2.20               # Outer skirt thickness

# Perimeter Snap-Fit Clips (6 clips: 2 left, 2 right, 2 rear)
CLIP_WIDTH = 12.0
SIDE_CLIP_Y = (-30.0, 30.0)
REAR_CLIP_X = (-30.0, 30.0)
CATCH_Z_BOTTOM = 22.0
CATCH_Z_TOP = 26.0
CATCH_PROTRUSION = 2.0

# --- Front Optical Window & Bezel (+y face of Pod, y_outer = +64.0) ---
OPTICAL_CENTER_Z = 15.5
OPTICAL_APERTURE_DIA = 20.0
WINDOW_SIZE = 25.0                   # 25 x 25 x 2.0 mm clear PC plate
WINDOW_THICK = 2.0
WINDOW_BOSS_W = 36.0                 # x in [-18, +18]
WINDOW_BOSS_H = 29.0                 # z in [1.0, 30.0] (clears lid skirt at z=34.5)
WINDOW_BOSS_PROJ = 3.5               # y from 64.0 to 67.5
WINDOW_POCKET_Y0 = 65.2              # Window seat plane at y = 65.2

# --- Electronic Components Specs (mm) ---
ESP32_LEN_X = 58.0
ESP32_WID_Y = 28.0
ESP32_THICK = 1.6
ESP32_CENTER_X = 4.0
ESP32_CENTER_Y = 30.5
ESP32_BASE_Z = 6.0

OV5640_PCB_SIZE = 24.0               # Carrier + LED ring board behind aperture
OV5640_SENSOR_SIZE = 8.5
OV5640_LENS_DIA = 8.5

# 12V 4000mAh 18650 3S1P Rechargeable Lithium Pack (70 x 60 x 20 mm, removable)
BATT_LEN_X = 70.0
BATT_WID_Y = 60.0
BATT_H_Z = 20.0
BATT_CENTER_X = -14.0
BATT_CENTER_Y = -26.5

# LM2596 DC-DC Buck Converter (12V -> 3.3V, 21 x 43 mm module)
BUCK_LEN_X = 21.0
BUCK_WID_Y = 43.0
BUCK_CENTER_X = -42.0
BUCK_CENTER_Y = 30.5

SWITCH_LEN_X = 8.0
SWITCH_WID_Y = 19.0
SWITCH_CENTER_X = 44.5
SWITCH_CENTER_Y = 35.0

DESICCANT_LEN_X = 20.0
DESICCANT_WID_Y = 44.0
DESICCANT_CENTER_X = 39.5
DESICCANT_CENTER_Y = -26.5

# --- World Assembly Coordinates (mm) ---
POD_WORLD_Y = -110.0
POD_WORLD_Z = 118.0                  # Places optical center at Z = 118 + 15.5 = 133.5 mm

CARD_WIDTH_X = 100.0                 # Standard 10 x 25 cm blue sticky trap
CARD_HEIGHT_Z = 250.0
CARD_THICK_Y = 1.0
CARD_WORLD_Y = 85.0
CARD_BOTTOM_Z = 13.0                 # Card spans Z = 13.0 .. 263.0 mm (center Z = 138.0 mm)
