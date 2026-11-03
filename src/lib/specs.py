"""Shared dimensions, tolerances, coordinate datums, and component factories.

Updated for Option A with full cable-routing channels, DC connector exit slots,
under-ESP cable tunnel, raised battery/buck support ribs, and generous bay clearances:
- Pod outer box: 86.0 mm (X width) x 172.0 mm (Y length) x 60.0 mm (Z height).
- Camera on narrow front face (+Y), directly in front of the ESP32-S3.
- ESP32-S3 (28 x 58 mm) flat with pins pointing UP (+Z) on twin 20mm slotted pin-rails,
  forming a 20.6 x 20.0 mm central cable tunnel underneath with retainer fingers.
- Dedicated 6.3 mm wide Right-Side Cable Raceway (`x in [+33.5, +39.8]`) with retainer fingers
  connecting Buck <-> Battery <-> ESP32-S3.
- 12V 4000mAh Battery (70 x 60 x 20 mm) & Buck (70 x 30 x 20 mm) seated on 2.5 mm floor ribs
  with 2.0-3.6 mm perimeter clearance and DC plug exit slots.
"""

from __future__ import annotations

# --- Print & Snap-Fit Tolerances (mm) ---
CLEARANCE = 0.30          # General sliding / mating clearance per side
SEAL_CLEARANCE = 0.25     # Labyrinth & wiper lip nominal CAD clearance
PETG_LIP_THICKNESS = 0.70 # Option B compliant PETG wiper blade thickness

# --- Pod Main Dimensions (Pod-Local Frame: X=width, Y=length/optical axis, Z=height) ---
OUTER_X = 86.0            # Width including 6.3 mm side cable channel (x in [-43.0, +43.0])
OUTER_Y = 172.0           # Length including wire clearances (y in [-86.0, +86.0])
FLOOR_T = 3.0             # Chassis bottom floor thickness (z = -3.0 .. 0.0)
INNER_Z = 57.0            # Interior cavity height (z = 0.0 .. 57.0 -> total box height = 60.0 mm)

RIM_WIDTH = 4.2           # Top rim width for Option B Labyrinth + PETG lip
INNER_X = OUTER_X - 2.0 * RIM_WIDTH  # 77.6 mm top opening
INNER_Y = OUTER_Y - 2.0 * RIM_WIDTH  # 163.6 mm top opening

# Lower interior cavity (below z = 52.0 mm rim step):
CAVITY_X = 79.6           # x in [-39.8, +39.8] (3.1 mm side walls)
CAVITY_Y = 165.6          # y in [-82.8, +82.8] (3.2 mm front/rear walls)

# Option B Labyrinth & Wiper Lip Parameters at z = INNER_Z (57.0 mm)
GROOVE_OFFSET_IN = 0.8
GROOVE_OFFSET_OUT = 2.2
GROOVE_DEPTH = 3.5

RIDGE_OFFSET_IN = 2.2
RIDGE_OFFSET_OUT = 3.2
RIDGE_HEIGHT = 3.0

# Lid (`tapa_carcasa`) mating heights in Pod-Local Frame:
LID_CEILING_Z = INNER_Z + 0.40       # 57.4 mm
LID_SKIRT_BOTTOM_Z = INNER_Z - 3.50  # 53.5 mm
LID_SKIRT_THICK = 2.20               # Outer skirt thickness

# Perimeter Snap-Fit Clips (6 clips: 2 left, 2 right, 2 rear)
CLIP_WIDTH = 12.0
SIDE_CLIP_Y = (-44.0, 44.0)
REAR_CLIP_X = (-20.0, 20.0)
CATCH_Z_BOTTOM = 41.0
CATCH_Z_TOP = 45.0
CATCH_PROTRUSION = 2.0

# --- Front Optical Window & Bezel (on narrow +Y face at y_front = +86.0) ---
OPTICAL_CENTER_Z = 25.0
OPTICAL_APERTURE_DIA = 20.0
WINDOW_SIZE = 25.0                   # 25 x 25 x 2.0 mm clear PC plate
WINDOW_THICK = 2.0
WINDOW_BOSS_W = 36.0                 # x in [-18, +18]
WINDOW_BOSS_H = 29.0                 # z in [10.5, 39.5] (clears lid skirt at z=53.5)
WINDOW_BOSS_PROJ = 3.5               # y from 86.0 to 89.5
WINDOW_POCKET_Y0 = 87.2              # Window seat plane at y = 87.2

# --- Electronic Components Specs (mm) ---
# 1. OV5640 Camera behind front wall (y_inner = +82.8)
OV5640_PCB_SIZE = 24.0
OV5640_SENSOR_SIZE = 8.5
OV5640_LENS_DIA = 8.5

# 2. ESP32-S3 (oriented toward camera: 28 mm wide along X, 58 mm long along Y, pins UP)
ESP32_WID_X = 28.0
ESP32_LEN_Y = 58.0
ESP32_THICK = 1.6
ESP32_CENTER_X = 0.0
ESP32_CENTER_Y = 47.5                # y in [18.5, 76.5]
ESP32_RAIL_TOP_Z = 20.0              # 20 mm tall pin rails (forms 20.6x20mm cable tunnel underneath)
ESP32_BASE_Z = 20.3                  # PCB sits at z = 20.3 .. 21.9 mm
ESP32_PIN_PITCH_X = 25.4             # Center-to-center distance between the 2 pin rows

# 3. 12V 4000mAh 18650 3S1P Battery Pack (lying flat behind ESP: 70 across X, 60 along Y, 20 tall)
# Shifted to x = -2.5 mm so x in [-37.5, +32.5], leaving a 6.3 mm Right-Side Cable Channel at x in [+33.5, +39.8]
# Elevated on z = 2.5 mm floor ribs (sits at z = 2.9 .. 22.9 mm) so wires can also pass underneath!
BATT_WID_X = 70.0
BATT_LEN_Y = 60.0
BATT_H_Z = 20.0
BATT_CENTER_X = -2.5
BATT_CENTER_Y = -16.8                # y in [-46.8, +13.2] (3.6 mm Y clearance in [-48.6, +15.0] bay)
BATT_BASE_Z = 2.9

# 4. Buck Converter (70 across X, 30 along Y, 20 tall, at rear behind battery)
BUCK_WID_X = 70.0
BUCK_LEN_Y = 30.0
BUCK_H_Z = 20.0
BUCK_CENTER_X = -2.5
BUCK_CENTER_Y = -66.0                # y in [-81.0, -51.0] (2.6 mm Y clearance in [-82.8, -50.2] bay)
BUCK_BASE_Z = 2.9

# --- World Assembly Coordinates (mm) ---
POD_WORLD_Y = -125.0
POD_WORLD_Z = 113.0                  # Places optical center at Z = 113 + 25 = 138.0 mm

CARD_WIDTH_X = 100.0                 # Standard 10 x 25 cm blue sticky trap
CARD_HEIGHT_Z = 250.0
CARD_THICK_Y = 1.0
CARD_WORLD_Y = 85.0
CARD_BOTTOM_Z = 13.0                 # Card spans Z = 13.0 .. 263.0 mm (center Z = 138.0 mm)
