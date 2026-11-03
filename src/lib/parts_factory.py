"""Parametric build123d factories for all parts of the Trampa de Trips (Option A + Full Cable Routing)."""

from __future__ import annotations

from cadgen import build123d as bd
from cadgen import srgb

from lib import specs as sp


def _centered_box(dx: float, dy: float, dz: float, cx: float = 0.0, cy: float = 0.0, z0: float = 0.0) -> bd.Solid:
    """Create a box centered at (cx, cy) in XY and spanning [z0, z0 + dz] in Z."""
    return bd.Pos(cx, cy, z0 + dz / 2.0) * bd.Box(dx, dy, dz)


def make_chasis_bandeja() -> bd.Shape:
    """Part 1: Main sealed pod tray with dedicated cable-routing infrastructure:
    - Under-ESP Central Cable Tunnel (20.6 x 20.0 mm between the twin slotted pin-rails)
      with 3 cable-retainer fingers and aligned central pass-through slots in Dividers 1 & 2.
    - 6.3 mm wide Right-Side Cable Raceway (`x in [+33.5, +39.8]`) with 3 retainer fingers.
    - 2.5 mm tall floor support ribs under the Battery & Buck (forming an under-component
      central wire trench `x in [-12, +12]` as well as side raceway access).
    - Wide DC Barrel Connector Exit Slot from the Battery bay and generous 2.0-3.6 mm bay clearances.
    """
    x_half = sp.OUTER_X / 2.0   # 43.0
    y_front = sp.OUTER_Y / 2.0  # 86.0

    # 1. Main outer block (x in [-43, 43], y in [-86, 86], z in [-3, 57])
    outer = _centered_box(sp.OUTER_X, sp.OUTER_Y, sp.INNER_Z + sp.FLOOR_T, 0.0, 0.0, -sp.FLOOR_T)

    # 2. Subtract main interior cavity (two-step for top sealing rim at z = 52..57)
    lower_cav = _centered_box(sp.CAVITY_X, sp.CAVITY_Y, 52.5, 0.0, 0.0, 0.0)
    upper_cav = _centered_box(sp.INNER_X, sp.INNER_Y, 7.0, 0.0, 0.0, 51.5)
    body = outer - lower_cav - upper_cav

    # 3. Option B Sealing Groove in top rim (z = 53.5 .. 57.5)
    g_out_x = sp.INNER_X + 2.0 * sp.GROOVE_OFFSET_OUT
    g_out_y = sp.INNER_Y + 2.0 * sp.GROOVE_OFFSET_OUT
    g_in_x = sp.INNER_X + 2.0 * sp.GROOVE_OFFSET_IN
    g_in_y = sp.INNER_Y + 2.0 * sp.GROOVE_OFFSET_IN
    groove_ring = (
        _centered_box(g_out_x, g_out_y, sp.GROOVE_DEPTH + 0.5, 0.0, 0.0, sp.INNER_Z - sp.GROOVE_DEPTH)
        - _centered_box(g_in_x, g_in_y, sp.GROOVE_DEPTH + 1.0, 0.0, 0.0, sp.INNER_Z - sp.GROOVE_DEPTH - 0.2)
    )
    body = body - groove_ring

    # 4. Option B Labyrinth Male Ridge rising above top rim (z = 57.0 .. 60.0)
    r_out_x = sp.INNER_X + 2.0 * sp.RIDGE_OFFSET_OUT
    r_out_y = sp.INNER_Y + 2.0 * sp.RIDGE_OFFSET_OUT
    r_in_x = sp.INNER_X + 2.0 * sp.RIDGE_OFFSET_IN
    r_in_y = sp.INNER_Y + 2.0 * sp.RIDGE_OFFSET_IN
    ridge_ring = (
        _centered_box(r_out_x, r_out_y, sp.RIDGE_HEIGHT + 1.0, 0.0, 0.0, sp.INNER_Z - 1.0)
        - _centered_box(r_in_x, r_in_y, sp.RIDGE_HEIGHT + 2.0, 0.0, 0.0, sp.INNER_Z - 1.5)
    )
    body = body + ridge_ring

    # 5. Six Perimeter Snap-Fit Catch Lugs (2 left, 2 right, 2 rear)
    catches = []
    catch_h = sp.CATCH_Z_TOP - sp.CATCH_Z_BOTTOM
    for sy in sp.SIDE_CLIP_Y:
        catches.append(_centered_box(sp.CATCH_PROTRUSION + 1.0, sp.CLIP_WIDTH, catch_h, -x_half - sp.CATCH_PROTRUSION / 2.0 + 0.5, sy, sp.CATCH_Z_BOTTOM))
        catches.append(_centered_box(sp.CATCH_PROTRUSION + 1.0, sp.CLIP_WIDTH, catch_h, x_half + sp.CATCH_PROTRUSION / 2.0 - 0.5, sy, sp.CATCH_Z_BOTTOM))
    for rx in sp.REAR_CLIP_X:
        catches.append(_centered_box(sp.CLIP_WIDTH, sp.CATCH_PROTRUSION + 1.0, catch_h, rx, -y_front - sp.CATCH_PROTRUSION / 2.0 + 0.5, sp.CATCH_Z_BOTTOM))
    for c in catches:
        body = body + c

    # 6. Front Optical Window Boss on narrow +Y face (y = +86.0, z in [10.5, 39.5])
    boss_z0 = sp.OPTICAL_CENTER_Z - sp.WINDOW_BOSS_H / 2.0  # 10.5
    boss = _centered_box(sp.WINDOW_BOSS_W, sp.WINDOW_BOSS_PROJ + 1.0, sp.WINDOW_BOSS_H, 0.0, y_front + (sp.WINDOW_BOSS_PROJ - 1.0) / 2.0, boss_z0)
    bezel_catch_l = _centered_box(2.5, 1.3, 12.0, -sp.WINDOW_BOSS_W / 2.0 - 0.25, y_front + 2.55, sp.OPTICAL_CENTER_Z - 6.0)
    bezel_catch_r = _centered_box(2.5, 1.3, 12.0, sp.WINDOW_BOSS_W / 2.0 + 0.25, y_front + 2.55, sp.OPTICAL_CENTER_Z - 6.0)
    body = body + boss + bezel_catch_l + bezel_catch_r

    # Cut Window Pocket (25.6 x 25.6 mm, centered at z=25.0 -> z in [12.2, 37.8], from y = 87.2 to 90.5)
    win_pocket_w = sp.WINDOW_SIZE + 2.0 * sp.CLEARANCE  # 25.6
    win_pocket = _centered_box(win_pocket_w, 3.5, win_pocket_w, 0.0, sp.WINDOW_POCKET_Y0 + 1.75, sp.OPTICAL_CENTER_Z - win_pocket_w / 2.0)
    body = body - win_pocket

    # Cut Optical Aperture (dia 20.0 mm cylinder along Y axis through front wall)
    aperture_cyl = (
        bd.Pos(0.0, y_front, sp.OPTICAL_CENTER_Z)
        * bd.Rot(90.0, 0.0, 0.0)
        * bd.Cylinder(radius=sp.OPTICAL_APERTURE_DIA / 2.0, height=20.0)
    )
    body = body - aperture_cyl

    # Option B Printed PETG Window Sealing Ridge on pocket seat
    ridge_outer = (
        bd.Pos(0.0, sp.WINDOW_POCKET_Y0 - 0.125, sp.OPTICAL_CENTER_Z)
        * bd.Rot(90.0, 0.0, 0.0)
        * bd.Cylinder(radius=11.4, height=0.75)
    )
    ridge_inner = (
        bd.Pos(0.0, sp.WINDOW_POCKET_Y0 - 0.125, sp.OPTICAL_CENTER_Z)
        * bd.Rot(90.0, 0.0, 0.0)
        * bd.Cylinder(radius=10.7, height=1.2)
    )
    body = body + (ridge_outer - ridge_inner)

    # 7. Two Vertical L-Rails on Narrow Front Wall for Glare Hood (`parasol_capucha`, z in [9.5, 40.5])
    for sign in (-1.0, 1.0):
        web = _centered_box(2.5, 4.5, 31.0, sign * 26.75, y_front + 1.25, 9.5)
        flange = _centered_box(2.0, 2.0, 31.0, sign * 29.0, y_front + 2.5, 9.5)
        stop = _centered_box(4.5, 4.5, 3.0, sign * 27.75, y_front + 1.25, 6.5)
        body = body + web + flange + stop

    # 8. Bottom Mounting T-Rail Socket (`encaje_inferior_pod`, z = -9.0 .. -3.0)
    for sign in (-1.0, 1.0):
        rail_wall = _centered_box(3.5, 120.0, 7.0, sign * 28.25, 0.0, -9.0)
        rail_lip = _centered_box(7.5, 120.0, 2.5, sign * 26.25, 0.0, -9.0)
        body = body + rail_wall + rail_lip
    rear_stop = _centered_box(60.0, 3.0, 7.0, 0.0, -58.5, -9.0)
    body = body + rear_stop

    # 9. Internal Cradles, Slotted Pin-Rails & Dedicated Cable Routing Channels
    # 9a. OV5640 Camera Cradle behind narrow front wall (y_inner = +82.8)
    # Carrier PCB is 24x24x1.5 at y = 80.05..81.55, centered at x=0.0, z=25.0 -> z in [13.0, 37.0]
    for sign in (-1.0, 1.0):
        pillar = _centered_box(3.2, 4.2, 40.0, sign * 13.9, 80.75, -1.0)
        slot_cut = _centered_box(2.0, 2.1, 26.0, sign * 12.8, 80.8, 12.6)
        nib = _centered_box(3.2, 2.0, 1.6, sign * 13.2, 80.8, 37.4)
        body = body + (pillar - slot_cut) + nib
    cam_bottom_support = (
        _centered_box(26.0, 4.2, 13.6, 0.0, 80.75, -1.0)
        - _centered_box(16.0, 6.0, 15.0, 0.0, 80.75, 2.0)
    )
    body = body + cam_bottom_support

    # 9b. Twin Slotted Pin-Rails for ESP32-S3 (`rieles_pines_esp32`) + Under-ESP Cable Tunnel Retainers
    # ESP32-S3 PCB is 28.0 (X) x 58.0 (Y), centered at x=0.0, y=47.5 (y in [18.5, 76.5]), z in [20.3, 21.9].
    for sign in (-1.0, 1.0):
        rx = sign * (sp.ESP32_PIN_PITCH_X / 2.0)  # +-12.7 mm
        rail_box = _centered_box(4.8, 60.8, sp.ESP32_RAIL_TOP_Z + 1.0, rx, sp.ESP32_CENTER_Y, -1.0)
        pin_slot = _centered_box(2.0, 58.8, 5.5, rx, sp.ESP32_CENTER_Y, 15.5)
        stop_back = _centered_box(4.8, 1.0, 3.0, rx, 17.6, 19.5)
        stop_front = _centered_box(4.8, 1.0, 3.0, rx, 77.4, 19.5)
        body = body + (rail_box - pin_slot) + stop_back + stop_front

    # 3 Cable-Retainer Fingers inside the 20.6 x 20.0 mm Under-ESP Tunnel (projecting inward from left rail at z = 8.0 mm)
    for fy in (28.0, 47.5, 66.0):
        tunnel_finger = _centered_box(5.5, 5.0, 1.6, -8.5, fy, 8.0)
        body = body + tunnel_finger

    # 9c. Floor Support Ribs under Battery & Buck (`z = 0.0 .. 2.5` mm at x = -22.0 and x = +17.0 mm)
    # Raises Battery & Buck to z = 2.9 mm and creates a 29.0 mm wide x 2.5 mm tall Under-Component Central Cable Trench!
    for rx_rib in (-22.0, 17.0):
        floor_rib_batt = _centered_box(3.0, 56.0, 3.5, rx_rib, sp.BATT_CENTER_Y, -1.0)
        floor_rib_buck = _centered_box(3.0, 26.0, 3.5, rx_rib, sp.BUCK_CENTER_Y, -1.0)
        body = body + floor_rib_batt + floor_rib_buck

    # 9d. Transverse Divider Wall 1 (between ESP rails and Battery bay, at y in [15.0, 16.6])
    div1 = _centered_box(sp.CAVITY_X + 1.0, 1.6, 17.5, 0.0, 15.8, -1.0)
    # Cut 1: Central 16.0 mm wide Tunnel Pass-Through (x in [-8.0, +8.0], all the way down to z = 0.0!)
    cut_div1_center = _centered_box(16.0, 4.0, 18.0, 0.0, 15.8, 0.0)
    # Cut 2: Right-Side Cable Raceway Pass-Through (x in [+33.5, +40.5], all the way down to z = 0.0!)
    cut_div1_right = _centered_box(7.5, 4.0, 18.0, 37.0, 15.8, 0.0)
    body = body + (div1 - cut_div1_center - cut_div1_right)

    # 9e. Transverse Divider Wall 2 (between Battery bay and Rear Buck bay, at y in [-50.2, -48.6])
    div2 = _centered_box(sp.CAVITY_X + 1.0, 1.6, 17.5, 0.0, -49.4, -1.0)
    # Cut 1: Central 16.0 mm wide Tunnel Pass-Through (x in [-8.0, +8.0], down to z = 0.0!)
    cut_div2_center = _centered_box(16.0, 4.0, 18.0, 0.0, -49.4, 0.0)
    # Cut 2: Right-Side Cable Raceway Pass-Through (x in [+33.5, +40.5], down to z = 0.0!)
    cut_div2_right = _centered_box(7.5, 4.0, 18.0, 37.0, -49.4, 0.0)
    body = body + (div2 - cut_div2_center - cut_div2_right)

    # 9f. Right-Side Cable Raceway Guide Wall (`x in [+33.0, +34.6]`, leaving 71.5 mm bay on left and 5.2 mm cable channel on right!)
    # Battery & Buck span x in [-37.5, +32.5] (0.5 mm clear of +33.0 wall, and 1.0 mm clear of left corner ribs at -38.5!).
    raceway_wall = _centered_box(1.6, 98.0, 15.0, 33.8, -32.0, -1.0)
    # Cut wide DC Connector & Wire Exit Slots in the raceway wall for Battery (at y in [-44.0, -28.0]) and Buck (at y in [-76.0, -56.0])
    dc_exit_batt = _centered_box(4.0, 16.0, 13.0, 33.8, -36.0, 2.5)
    wire_exit_buck = _centered_box(4.0, 18.0, 13.0, 33.8, -66.0, 2.5)
    body = body + (raceway_wall - dc_exit_batt - wire_exit_buck)

    # 3 Overhanging Cable-Retainer Fingers over the Right-Side Cable Raceway (`x in [+34.6, +39.8]`, z = 13.5..15.0)
    for rfy in (-76.0, -49.4, -15.0, 15.8):
        rw_finger = _centered_box(4.2, 5.0, 1.5, 35.5, rfy, 13.5)
        body = body + rw_finger

    # Left-side corner locator ribs (at x in [-40.0, -38.3], leaving 0.8 mm clearance to component edge at -37.5!)
    rib_batt_l = _centered_box(1.7, 36.0, 15.0, -39.15, sp.BATT_CENTER_Y, -1.0)
    rib_buck_l = _centered_box(1.7, 18.0, 15.0, -39.15, sp.BUCK_CENTER_Y, -1.0)
    body = body + rib_batt_l + rib_buck_l

    # 2 Cantilever Retention Clips for Battery (on Div1 at y=+15.5 and Div2 at y=-49.1, hooking at z=23.3..24.9 above z=22.9 battery top!)
    batt_clip_f = _centered_box(14.0, 1.6, 25.9, -15.0, 15.5, -1.0) + _centered_box(14.0, 1.6, 1.6, -15.0, 14.1, 23.3)
    batt_clip_b = _centered_box(14.0, 1.6, 25.9, -15.0, -49.1, -1.0) + _centered_box(14.0, 1.6, 1.6, -15.0, -47.7, 23.3)
    body = body + batt_clip_f + batt_clip_b

    body.label = "chasis_bandeja"
    body.color = srgb("#2E3B4E")
    return body


def make_tapa_carcasa() -> bd.Shape:
    """Part 2: Top cover with Option B labyrinth female channel,
    0.7mm flexible PETG wiper lip, outer labyrinth skirt, sloped roof, and 6 cantilever snap clips.
    """
    x_half = sp.OUTER_X / 2.0
    y_half = sp.OUTER_Y / 2.0

    skirt_in_x = sp.OUTER_X + 2.0 * sp.CLEARANCE
    skirt_in_y = sp.OUTER_Y + 2.0 * sp.CLEARANCE
    skirt_out_x = skirt_in_x + 2.0 * sp.LID_SKIRT_THICK
    skirt_out_y = skirt_in_y + 2.0 * sp.LID_SKIRT_THICK

    lid_top_z = sp.INNER_Z + 9.0  # 66.0
    main_block = _centered_box(skirt_out_x, skirt_out_y, lid_top_z - sp.LID_SKIRT_BOTTOM_Z, 0.0, 0.0, sp.LID_SKIRT_BOTTOM_Z)

    roof_tier1 = _centered_box(skirt_out_x - 14.0, skirt_out_y - 8.0, 2.5, 0.0, 0.0, lid_top_z - 0.5)
    roof_tier2 = _centered_box(skirt_out_x - 32.0, skirt_out_y - 16.0, 2.0, 0.0, 0.0, lid_top_z + 1.5)
    lid = main_block + roof_tier1 + roof_tier2

    under_cut = _centered_box(skirt_in_x, skirt_in_y, sp.LID_CEILING_Z - sp.LID_SKIRT_BOTTOM_Z + 1.0, 0.0, 0.0, sp.LID_SKIRT_BOTTOM_Z - 1.0)
    lid = lid - under_cut

    fem_out_x = sp.INNER_X + 2.0 * (sp.RIDGE_OFFSET_OUT + 0.35)
    fem_out_y = sp.INNER_Y + 2.0 * (sp.RIDGE_OFFSET_OUT + 0.35)
    fem_in_x = sp.INNER_X + 2.0 * (sp.RIDGE_OFFSET_IN - 0.35)
    fem_in_y = sp.INNER_Y + 2.0 * (sp.RIDGE_OFFSET_IN - 0.35)
    fem_groove = (
        _centered_box(fem_out_x, fem_out_y, 3.6, 0.0, 0.0, sp.INNER_Z)
        - _centered_box(fem_in_x, fem_in_y, 4.0, 0.0, 0.0, sp.INNER_Z - 0.2)
    )
    lid = lid - fem_groove

    lip_center_ofs = (sp.GROOVE_OFFSET_IN + sp.GROOVE_OFFSET_OUT) / 2.0  # 1.50 mm
    lip_out_x = sp.INNER_X + 2.0 * (lip_center_ofs + sp.PETG_LIP_THICKNESS / 2.0)
    lip_out_y = sp.INNER_Y + 2.0 * (lip_center_ofs + sp.PETG_LIP_THICKNESS / 2.0)
    lip_in_x = sp.INNER_X + 2.0 * (lip_center_ofs - sp.PETG_LIP_THICKNESS / 2.0)
    lip_in_y = sp.INNER_Y + 2.0 * (lip_center_ofs - sp.PETG_LIP_THICKNESS / 2.0)
    wiper_lip = (
        _centered_box(lip_out_x, lip_out_y, 4.0, 0.0, 0.0, sp.INNER_Z - 3.0)
        - _centered_box(lip_in_x, lip_in_y, 4.5, 0.0, 0.0, sp.INNER_Z - 3.2)
    )
    lid = lid + wiper_lip

    dome_recess = _centered_box(sp.INNER_X - 4.0, sp.INNER_Y - 4.0, 4.6, 0.0, 0.0, sp.LID_CEILING_Z - 0.1)
    lid = lid - dome_recess

    clip_z0 = sp.CATCH_Z_BOTTOM - 4.0  # 37.0
    for sy in sp.SIDE_CLIP_Y:
        for sign in (-1.0, 1.0):
            root_bridge = _centered_box(3.2, sp.CLIP_WIDTH, 5.5, sign * (x_half + 3.1), sy, sp.LID_SKIRT_BOTTOM_Z)
            arm = _centered_box(2.4, sp.CLIP_WIDTH, 20.0, sign * (x_half + 3.5), sy, clip_z0)
            tooth = _centered_box(2.5, sp.CLIP_WIDTH, 2.15, sign * (x_half + 1.6), sy, clip_z0 + 1.5)
            grip = _centered_box(1.8, sp.CLIP_WIDTH, 2.0, sign * (x_half + 5.0), sy, clip_z0)
            lid = lid + root_bridge + arm + tooth + grip

    for rx in sp.REAR_CLIP_X:
        root_bridge = _centered_box(sp.CLIP_WIDTH, 3.2, 5.5, rx, -(y_half + 3.1), sp.LID_SKIRT_BOTTOM_Z)
        arm = _centered_box(sp.CLIP_WIDTH, 2.4, 20.0, rx, -(y_half + 3.5), clip_z0)
        tooth = _centered_box(sp.CLIP_WIDTH, 2.5, 2.15, rx, -(y_half + 1.6), clip_z0 + 1.5)
        grip = _centered_box(sp.CLIP_WIDTH, 1.8, 2.0, rx, -(y_half + 5.0), clip_z0)
        lid = lid + root_bridge + arm + tooth + grip

    lid.label = "tapa_carcasa"
    lid.color = srgb("#3E5066")
    return lid


def make_ventana_pc() -> bd.Shape:
    """Part 3a: Clear polycarbonate/acrylic optical window plate (25 x 25 x 2.0 mm)."""
    win = _centered_box(sp.WINDOW_SIZE, sp.WINDOW_THICK, sp.WINDOW_SIZE, 0.0, sp.WINDOW_POCKET_Y0 + 1.45, sp.OPTICAL_CENTER_Z - sp.WINDOW_SIZE / 2.0)
    win.label = "ventana_pc"
    win.color = srgb("#A8D8EA", 0.38)
    return win


def make_bisel_ventana() -> bd.Shape:
    """Part 3b: Snap-fit window bezel that retains `ventana_pc` against the PETG window ridge."""
    y_front = sp.OUTER_Y / 2.0  # 86.0
    bz_w = sp.WINDOW_BOSS_W + 2.0 * (0.35 + 2.0)          # 40.7
    bz_h = sp.WINDOW_BOSS_H + 2.0 * (0.35 + 1.15)         # 32.0
    z0 = sp.OPTICAL_CENTER_Z - bz_h / 2.0                 # 9.0

    front_plate = _centered_box(bz_w, 2.0, bz_h, 0.0, y_front + 5.0, z0)
    skirt_outer = _centered_box(bz_w, 2.8, bz_h, 0.0, y_front + 2.8, z0)
    skirt_inner = _centered_box(sp.WINDOW_BOSS_W + 0.70, 3.4, sp.WINDOW_BOSS_H + 0.70, 0.0, y_front + 2.7, z0 + 1.15)
    catch_cut = _centered_box(bz_w + 2.0, 3.6, 12.8, 0.0, y_front + 2.6, sp.OPTICAL_CENTER_Z - 6.4)
    bezel = front_plate + (skirt_outer - skirt_inner - catch_cut)

    view_hole = (
        bd.Pos(0.0, y_front + 4.0, sp.OPTICAL_CENTER_Z)
        * bd.Rot(90.0, 0.0, 0.0)
        * bd.Cylinder(radius=10.25, height=8.0)
    )
    bezel = bezel - view_hole

    for sign in (-1.0, 1.0):
        bridge = _centered_box(3.0, 2.0, 11.2, sign * 20.15, y_front + 5.0, sp.OPTICAL_CENTER_Z - 5.6)
        arm = _centered_box(1.8, 5.65, 11.2, sign * 20.75, y_front + 3.175, sp.OPTICAL_CENTER_Z - 5.6)
        tooth = _centered_box(2.2, 1.15, 11.2, sign * 19.65, y_front + 0.925, sp.OPTICAL_CENTER_Z - 5.6)
        bezel = bezel + bridge + arm + tooth

    bezel.label = "bisel_ventana"
    bezel.color = srgb("#D97724")
    return bezel


def make_parasol_capucha() -> bd.Shape:
    """Part 4: Slide-on glare-blocking hood / rain visor on narrow +Y face."""
    y_front = sp.OUTER_Y / 2.0  # 86.0
    z_base = 9.85
    hood = _centered_box(65.0, 2.5, 33.65, 0.0, y_front + 5.1, z_base) - _centered_box(46.0, 4.0, 32.0, 0.0, y_front + 5.1, z_base - 0.35)

    for sign in (-1.0, 1.0):
        side_wall = _centered_box(2.1, 4.0, 30.4, sign * 31.45, y_front + 2.35, z_base)
        back_lip = _centered_box(2.7, 0.8, 30.4, sign * 29.75, y_front + 0.75, z_base)
        hood = hood + side_wall + back_lip

    visor_roof = _centered_box(68.0, 35.0, 2.2, 0.0, y_front + 21.5, z_base + 31.45)
    hood = hood + visor_roof
    for sign in (-1.0, 1.0):
        baffle = _centered_box(2.5, 35.0, 29.0, sign * 32.75, y_front + 21.5, z_base + 3.15)
        hood = hood + baffle

    hood.label = "parasol_capucha"
    hood.color = srgb("#232B35")
    return hood


def make_tarjeta_azul() -> bd.Shape:
    """Standard 100 x 250 x 1.0 mm Blue Sticky Trap Card in World Coordinates."""
    card = _centered_box(sp.CARD_WIDTH_X, sp.CARD_THICK_Y, sp.CARD_HEIGHT_Z, 0.0, sp.CARD_WORLD_Y, sp.CARD_BOTTOM_Z)
    card.label = "tarjeta_azul"
    card.color = srgb("#0077FF")
    return card


def make_marco_tarjeta() -> bd.Shape:
    """Part 5: Open frame for the 100 x 250 mm blue sticky card + balanced overhead hanging hook."""
    yc = sp.CARD_WORLD_Y  # +85.0 mm
    frame = _centered_box(112.0, 9.0, 7.0, 0.0, yc, 10.0)
    card_slot_bottom = _centered_box(100.8, 2.4, 6.0, 0.0, yc, 12.6)
    cross_relief = _centered_box(92.0, 12.0, 4.0, 0.0, yc, 14.0)
    drain1 = _centered_box(8.0, 2.4, 8.0, -25.0, yc, 9.0)
    drain2 = _centered_box(8.0, 2.4, 8.0, 25.0, yc, 9.0)
    frame = frame - card_slot_bottom - cross_relief - drain1 - drain2

    for sign in (-1.0, 1.0):
        c_outer = _centered_box(9.5, 9.0, 222.0, sign * 51.25, yc, 10.0)
        c_slot = _centered_box(5.0, 2.4, 225.0, sign * 48.3, yc, 12.6)
        c_open = _centered_box(4.5, 12.0, 225.0, sign * 47.0, yc, 14.0)
        frame = frame + (c_outer - c_slot - c_open)

    rear_mid_bar = _centered_box(112.0, 3.0, 8.0, 0.0, yc + 3.0, 125.0)
    frame = frame + rear_mid_bar

    for sign in (-1.0, 1.0):
        step_arm = _centered_box(5.0, 22.0, 8.0, sign * 53.5, yc - 6.5, 224.0)
        riser = _centered_box(5.0, 8.0, 28.0, sign * 53.5, yc - 15.5, 224.0)
        frame = frame + step_arm + riser

    top_arch_bar = _centered_box(112.0, 8.0, 8.0, 0.0, yc - 15.5, 246.0)
    balance_arm = _centered_box(14.0, 54.0, 8.0, 0.0, 46.5, 246.0)
    hook_tab = _centered_box(24.0, 24.0, 8.0, 0.0, 26.0, 246.0) - (
        bd.Pos(0.0, 25.0, 250.0) * bd.Cylinder(radius=7.0, height=12.0)
    )
    frame = frame + top_arch_bar + balance_arm + hook_tab

    frame.label = "marco_tarjeta"
    frame.color = srgb("#2E3B4E")
    return frame


def make_soporte_base() -> bd.Shape:
    """Part 6: Dual-purpose classroom presentation table stand & fixed-distance optical bridge."""
    base = _centered_box(128.0, 20.0, 10.0, 0.0, -140.0, 0.0)
    base = base + _centered_box(128.0, 22.0, 10.0, 0.0, 85.0, 0.0)
    base = base + _centered_box(128.0, 18.0, 10.0, 0.0, -25.0, 0.0)
    for sign in (-1.0, 1.0):
        runner = _centered_box(16.0, 246.0, 10.0, sign * 56.0, -27.0, 0.0)
        base = base + runner

    for sign in (-1.0, 1.0):
        outer_tower = _centered_box(7.65, 22.0, 38.0, sign * 60.175, 85.0, 0.0)
        front_lip = _centered_box(12.0, 4.0, 38.0, sign * 58.0, 76.1, 0.0)
        rear_lip = _centered_box(12.0, 4.0, 38.0, sign * 58.0, 93.9, 0.0)
        base = base + outer_tower + front_lip + rear_lip

    y_ped = sp.POD_WORLD_Y + 10.0  # -115.0
    for sign in (-1.0, 1.0):
        col = _centered_box(12.0, 68.0, 96.0, sign * 16.0, y_ped, 8.0)
        gusset = _centered_box(8.0, 45.0, 45.0, sign * 16.0, y_ped + 40.0, 8.0)
        base = base + col + gusset

    top_bridge = _centered_box(44.0, 72.0, 5.65, 0.0, y_ped, 98.0)
    t_neck = _centered_box(44.0, 72.0, 4.5, 0.0, y_ped, 103.0)
    t_flange = _centered_box(52.0, 72.0, 2.7, 0.0, y_ped, 106.9)
    latch_arm = _centered_box(22.0, 26.0, 4.0, 0.0, y_ped + 44.0, 98.0)
    front_latch = _centered_box(22.0, 2.5, 9.5, 0.0, y_ped + 55.75, 100.0)
    base = base + top_bridge + t_neck + t_flange + latch_arm + front_latch

    base.label = "soporte_base"
    base.color = srgb("#4A5568")
    return base


def make_componentes_internos() -> bd.Shape:
    """Reference electronic components & routed power cables inside `chasis_bandeja`:
    - OV5640 Camera Module + Lens at narrow +Y front face
    - ESP32-S3 (28 x 58 mm) oriented toward camera, pins pointing UP (+Z),
      with downward pin tails seated inside the twin slotted rails
    - 12V 4000mAh 18650 3S1P Lithium Pack (70 x 60 x 20 mm, flat on 2.5 mm ribs)
    - Buck Converter (70 x 30 x 20 mm, flat on 2.5 mm ribs) at the rear (-Y)
    - Routed Power Harness (`cable_12v_bateria_buck` in side raceway & `cable_3v3_buck_esp`
      through the central under-ESP tunnel up to the ESP32-S3 header pins).
    """
    children = []

    # 1. OV5640 Camera Carrier + Lens Barrel (at y = 80.05..86.0, z = 25.0)
    cam_pcb = _centered_box(sp.OV5640_PCB_SIZE, 1.5, sp.OV5640_PCB_SIZE, 0.0, 80.8, sp.OPTICAL_CENTER_Z - sp.OV5640_PCB_SIZE / 2.0)
    cam_pcb.label = "ov5640_carrier_pcb"
    cam_pcb.color = srgb("#263238")
    children.append(cam_pcb)

    cam_lens = (
        bd.Pos(0.0, 83.9, sp.OPTICAL_CENTER_Z)
        * bd.Rot(90.0, 0.0, 0.0)
        * bd.Cylinder(radius=sp.OV5640_LENS_DIA / 2.0, height=4.4)
    )
    cam_lens.label = "ov5640_lente"
    cam_lens.color = srgb("#111111")
    children.append(cam_lens)

    # 2. ESP32-S3 PCB (28 x 58 x 1.6 mm at x=0, y=47.5, z=20.3..21.9) + Upward Pins + Downward Pin Tails
    esp_pcb = _centered_box(sp.ESP32_WID_X, sp.ESP32_LEN_Y, sp.ESP32_THICK, sp.ESP32_CENTER_X, sp.ESP32_CENTER_Y, sp.ESP32_BASE_Z)
    esp_pcb.label = "esp32_s3_pcb"
    esp_pcb.color = srgb("#1B5E20")
    children.append(esp_pcb)

    esp_shield = _centered_box(18.0, 18.0, 3.2, 0.0, sp.ESP32_CENTER_Y + 8.0, sp.ESP32_BASE_Z + sp.ESP32_THICK)
    esp_shield.label = "esp32_s3_wroom"
    esp_shield.color = srgb("#B0BEC5")
    children.append(esp_shield)

    pins_up_l = _centered_box(1.2, 52.0, 8.5, -sp.ESP32_PIN_PITCH_X / 2.0, sp.ESP32_CENTER_Y, sp.ESP32_BASE_Z + sp.ESP32_THICK)
    pins_up_r = _centered_box(1.2, 52.0, 8.5, sp.ESP32_PIN_PITCH_X / 2.0, sp.ESP32_CENTER_Y, sp.ESP32_BASE_Z + sp.ESP32_THICK)
    pins_down_l = _centered_box(1.0, 52.0, 3.5, -sp.ESP32_PIN_PITCH_X / 2.0, sp.ESP32_CENTER_Y, 16.8)
    pins_down_r = _centered_box(1.0, 52.0, 3.5, sp.ESP32_PIN_PITCH_X / 2.0, sp.ESP32_CENTER_Y, 16.8)
    pins_comp = pins_up_l + pins_up_r + pins_down_l + pins_down_r
    pins_comp.label = "esp32_pines"
    pins_comp.color = srgb("#FFD54F")
    children.append(pins_comp)

    # 3. 12V 4000mAh 18650 3S1P Lithium Battery Pack (70 x 60 x 20 mm at x=-2.5, y=-16.8, z=2.9..22.9)
    batt_pack = _centered_box(sp.BATT_WID_X, sp.BATT_LEN_Y, sp.BATT_H_Z, sp.BATT_CENTER_X, sp.BATT_CENTER_Y, sp.BATT_BASE_Z)
    batt_pack.label = "bateria_12v_4000mah"
    batt_pack.color = srgb("#1565C0")
    children.append(batt_pack)

    # 4. Buck Converter (70 x 30 x 20 mm at x=-2.5, y=-66.0, z=2.9..22.9)
    buck = _centered_box(sp.BUCK_WID_X, sp.BUCK_LEN_Y, sp.BUCK_H_Z, sp.BUCK_CENTER_X, sp.BUCK_CENTER_Y, sp.BUCK_BASE_Z)
    buck.label = "buck_70x30x20"
    buck.color = srgb("#0D47A1")
    children.append(buck)

    # 5. Routed Reference Cables:
    # 5a. 12V Cable from Battery DC Exit Slot (y=-36.0) along Right-Side Cable Raceway (x=+37.2, z=4.5..7.5) into Buck IN (y=-66.0)
    c12_out = _centered_box(4.2, 3.0, 3.0, 35.1, -36.0, 4.5)
    c12_run = _centered_box(3.0, 33.0, 3.0, 37.2, -51.0, 4.5)
    c12_in = _centered_box(4.2, 3.0, 3.0, 35.1, -66.0, 4.5)
    cable_12v = c12_out + c12_run + c12_in
    cable_12v.label = "cable_12v_bateria_buck"
    cable_12v.color = srgb("#E53935")
    children.append(cable_12v)

    # 5b. 3.3V/GND Cable from Buck OUT (y=-50.5, x=0.0) running through the Under-Battery Central Trench
    # (x=0.0, z=0.4..2.2) -> through Divider 1 central cutout -> through Under-ESP Tunnel (y=15..78) ->
    # emerging at front of ESP (y=+78.2) and rising up to connect onto the upward ESP32-S3 header pins (z=31.0..33.5)!
    c3v_trench = _centered_box(4.0, 128.0, 1.8, 0.0, 14.3, 0.4)
    c3v_riser = _centered_box(4.0, 1.6, 32.5, 0.0, 77.5, 0.4)
    c3v_bridge = _centered_box(15.0, 3.0, 2.2, -5.85, 76.0, 31.0)
    cable_3v3 = c3v_trench + c3v_riser + c3v_bridge
    cable_3v3.label = "cable_3v3_buck_esp"
    cable_3v3.color = srgb("#FB8C00")
    children.append(cable_3v3)

    return bd.Compound(children=children, label="componentes_internos")
