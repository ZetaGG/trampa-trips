"""Shared specifications for the lightweight (`ligero`) optimized version.
All functional datums, external dimensions, and component sizes are identical to `src/lib/specs.py`.
"""

from __future__ import annotations

CLEARANCE = 0.30
SEAL_CLEARANCE = 0.25
PETG_LIP_THICKNESS = 0.70

OUTER_X = 86.0
OUTER_Y = 172.0
FLOOR_T = 3.0
INNER_Z = 57.0

RIM_WIDTH = 4.2
INNER_X = OUTER_X - 2.0 * RIM_WIDTH  # 77.6 mm
INNER_Y = OUTER_Y - 2.0 * RIM_WIDTH  # 163.6 mm

# Lightweight thin walls (1.8 mm instead of 3.1-3.2 mm) in the main cavity below the rim:
CAVITY_X = OUTER_X - 2.0 * 1.8       # 82.4 mm (1.8 mm side walls)
CAVITY_Y = OUTER_Y - 2.0 * 1.8       # 168.4 mm (1.8 mm front/rear walls)

GROOVE_OFFSET_IN = 0.8
GROOVE_OFFSET_OUT = 2.2
GROOVE_DEPTH = 3.5

RIDGE_OFFSET_IN = 2.2
RIDGE_OFFSET_OUT = 3.2
RIDGE_HEIGHT = 3.0

LID_CEILING_Z = INNER_Z + 0.40       # 57.4 mm
LID_SKIRT_BOTTOM_Z = INNER_Z - 3.50  # 53.5 mm
LID_SKIRT_THICK = 1.60               # Thinned outer skirt (1.6 mm instead of 2.2 mm)

CLIP_WIDTH = 10.0                    # 10 mm wide clips (saves material while keeping snap force)
SIDE_CLIP_Y = (-44.0, 44.0)
REAR_CLIP_X = (-20.0, 20.0)
CATCH_Z_BOTTOM = 41.0
CATCH_Z_TOP = 45.0
CATCH_PROTRUSION = 2.0

OPTICAL_CENTER_Z = 25.0
OPTICAL_APERTURE_DIA = 20.0
WINDOW_SIZE = 25.0
WINDOW_THICK = 2.0
WINDOW_BOSS_W = 36.0
WINDOW_BOSS_H = 29.0
WINDOW_BOSS_PROJ = 3.5
WINDOW_POCKET_Y0 = 87.2

OV5640_PCB_SIZE = 24.0
OV5640_SENSOR_SIZE = 8.5
OV5640_LENS_DIA = 8.5

ESP32_WID_X = 28.0
ESP32_LEN_Y = 58.0
ESP32_THICK = 1.6
ESP32_CENTER_X = 0.0
ESP32_CENTER_Y = 47.5
ESP32_RAIL_TOP_Z = 20.0
ESP32_BASE_Z = 20.3
ESP32_PIN_PITCH_X = 25.4

BATT_WID_X = 70.0
BATT_LEN_Y = 60.0
BATT_H_Z = 20.0
BATT_CENTER_X = -2.5
BATT_CENTER_Y = -16.8
BATT_BASE_Z = 2.9

BUCK_WID_X = 70.0
BUCK_LEN_Y = 30.0
BUCK_H_Z = 20.0
BUCK_CENTER_X = -2.5
BUCK_CENTER_Y = -66.0
BUCK_BASE_Z = 2.9

POD_WORLD_Y = -125.0
POD_WORLD_Z = 113.0

CARD_WIDTH_X = 100.0
CARD_HEIGHT_Z = 250.0
CARD_THICK_Y = 1.0
CARD_WORLD_Y = 85.0
CARD_BOTTOM_Z = 13.0
