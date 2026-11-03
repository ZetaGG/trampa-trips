"""Lightweight (`ligero`) parametric build123d factories — same external envelope & fits, minimal filament."""

from __future__ import annotations

from cadgen import build123d as bd
from cadgen import srgb

from lib import specs_ligero as sp


def _centered_box(dx: float, dy: float, dz: float, cx: float = 0.0, cy: float = 0.0, z0: float = 0.0) -> bd.Solid:
    """Create a box centered at (cx, cy) in XY and spanning [z0, z0 + dz] in Z."""
    return bd.Pos(cx, cy, z0 + dz / 2.0) * bd.Box(dx, dy, dz)


def _arched_window(dx: float, dy: float, z0: float, z1: float, cx: float, cy: float) -> bd.Shape:
    """Cutting tool: a window through the X axis, closed on top by a self-supporting
    semicircular arch (radius = dy / 2). Prints without supports and avoids a long flat bridge."""
    r = dy / 2.0
    box = _centered_box(dx, dy, (z1 - z0) - r, cx, cy, z0)
    arch = bd.Pos(cx, cy, z1 - r) * bd.Rot(0.0, 90.0, 0.0) * bd.Cylinder(radius=r, height=dx)
    return box + arch


def make_chasis_bandeja_ligero() -> bd.Shape:
    """Lightweight Part 1:
    - Same external dimensions (86 x 172 x 60 mm nominal box) and same internal component datums.
    - 1.8 mm side/front/rear walls below the top sealing rim (instead of 3.1-3.2 mm).
    - 1.6 mm floor (via underside lightening pockets between the T-rails).
    - Hollowed/arched ESP32 pin-rails (U-channel top + 3 support piers instead of solid bars).
    - 1.2 mm divider walls and raceway wall.
    """
    x_half = sp.OUTER_X / 2.0   # 43.0
    y_front = sp.OUTER_Y / 2.0  # 86.0

    # 1. Main outer block (x in [-43, 43], y in [-86, 86], z in [-3, 57])
    outer = _centered_box(sp.OUTER_X, sp.OUTER_Y, sp.INNER_Z + sp.FLOOR_T, 0.0, 0.0, -sp.FLOOR_T)

    # 2. Subtract main interior cavity (1.8 mm walls up to z=52.5, then 4.2 mm top rim at z=52.5..57)
    lower_cav = _centered_box(sp.CAVITY_X, sp.CAVITY_Y, 52.8, 0.0, 0.0, 0.0)
    upper_cav = _centered_box(sp.INNER_X, sp.INNER_Y, 7.0, 0.0, 0.0, 51.5)
    body = outer - lower_cav - upper_cav

    # Thin the floor from 3.0 mm to 1.6 mm using bottom lightening SLOTS (z = -3.2 .. -1.6).
    # Slots (12-18 mm wide) instead of big pockets so every ceiling is a short, safe bridge.
    # T-rail zones (|x| in [22.5, 31.0]) stay solid at full 3.0 mm.
    floor_cuts = None
    for sx in (-14.0, 0.0, 14.0):  # under ESP / mid section
        c = _centered_box(12.0, 110.0, 1.6, sx, 0.0, -3.2)
        floor_cuts = c if floor_cuts is None else floor_cuts + c
    for sx in (-30.0, -10.0, 10.0, 30.0):  # under front (camera / ESP pins)
        c = _centered_box(16.0, 18.0, 1.6, sx, 71.0, -3.2)
        floor_cuts = floor_cuts + c
    for sx in (-30.0, -10.0, 10.0, 30.0):  # under rear (buck / tray)
        c = _centered_box(16.0, 16.0, 1.6, sx, -71.0, -3.2)
        floor_cuts = floor_cuts + c
    body = body - floor_cuts

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

    # 5. Six Perimeter Snap-Fit Catch Lugs
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
    boss_z0 = sp.OPTICAL_CENTER_Z - sp.WINDOW_BOSS_H / 2.0
    boss = _centered_box(sp.WINDOW_BOSS_W, sp.WINDOW_BOSS_PROJ + 1.5, sp.WINDOW_BOSS_H, 0.0, y_front + (sp.WINDOW_BOSS_PROJ - 1.5) / 2.0, boss_z0)
    bezel_catch_l = _centered_box(2.5, 1.3, 12.0, -sp.WINDOW_BOSS_W / 2.0 - 0.25, y_front + 2.55, sp.OPTICAL_CENTER_Z - 6.0)
    bezel_catch_r = _centered_box(2.5, 1.3, 12.0, sp.WINDOW_BOSS_W / 2.0 + 0.25, y_front + 2.55, sp.OPTICAL_CENTER_Z - 6.0)
    body = body + boss + bezel_catch_l + bezel_catch_r

    win_pocket_w = sp.WINDOW_SIZE + 2.0 * sp.CLEARANCE
    win_pocket = _centered_box(win_pocket_w, 3.5, win_pocket_w, 0.0, sp.WINDOW_POCKET_Y0 + 1.75, sp.OPTICAL_CENTER_Z - win_pocket_w / 2.0)
    body = body - win_pocket

    aperture_cyl = (
        bd.Pos(0.0, y_front, sp.OPTICAL_CENTER_Z)
        * bd.Rot(90.0, 0.0, 0.0)
        * bd.Cylinder(radius=sp.OPTICAL_APERTURE_DIA / 2.0, height=20.0)
    )
    body = body - aperture_cyl

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

    # 7. Two Vertical L-Rails on Narrow Front Wall for Glare Hood (thinned web)
    for sign in (-1.0, 1.0):
        web = _centered_box(2.0, 4.5, 31.0, sign * 27.0, y_front + 1.25, 9.5)
        flange = _centered_box(2.0, 1.8, 31.0, sign * 29.0, y_front + 2.6, 9.5)
        stop = _centered_box(4.0, 4.5, 2.4, sign * 28.0, y_front + 1.25, 7.1)
        body = body + web + flange + stop

    # 8. Bottom Mounting T-Rail Socket (with side lightening windows to save filament!)
    for sign in (-1.0, 1.0):
        rail_wall = _centered_box(2.6, 120.0, 7.0, sign * 27.8, 0.0, -9.0)
        rail_lip = _centered_box(6.6, 120.0, 2.0, sign * 25.8, 0.0, -9.0)
        # Cut 3 lightening windows along the T-rail wall
        w1 = _centered_box(8.0, 26.0, 3.2, sign * 27.8, -36.0, -6.5)
        w2 = _centered_box(8.0, 26.0, 3.2, sign * 27.8, 0.0, -6.5)
        w3 = _centered_box(8.0, 26.0, 3.2, sign * 27.8, 36.0, -6.5)
        body = body + (rail_wall + rail_lip - w1 - w2 - w3)
    rear_stop = _centered_box(58.0, 2.2, 7.0, 0.0, -58.9, -9.0)
    body = body + rear_stop

    # 9. Lightweight Internal Cradles, Hollowed Pin-Rails & Cable Channels
    # 9a. OV5640 Camera Cradle (thinned pillars)
    for sign in (-1.0, 1.0):
        pillar = _centered_box(2.4, 3.6, 39.5, sign * 13.5, 80.8, -1.0)
        slot_cut = _centered_box(1.6, 2.0, 26.0, sign * 12.6, 80.8, 12.6)
        nib = _centered_box(2.6, 1.8, 1.5, sign * 12.9, 80.8, 37.4)
        body = body + (pillar - slot_cut) + nib
    cam_bottom_support = (
        _centered_box(25.0, 3.6, 13.6, 0.0, 80.8, -1.0)
        - _centered_box(19.0, 6.0, 15.0, 0.0, 80.8, 1.5)
    )
    body = body + cam_bottom_support

    # 9b. Hollowed/Arched Twin Slotted Pin-Rails for ESP32-S3 (`rieles_pines_esp32`)
    for sign in (-1.0, 1.0):
        rx = sign * (sp.ESP32_PIN_PITCH_X / 2.0)  # +-12.7 mm
        rail_box = _centered_box(4.2, 60.8, sp.ESP32_RAIL_TOP_Z + 1.0, rx, sp.ESP32_CENTER_Y, -1.0)
        pin_slot = _centered_box(2.0, 58.8, 5.5, rx, sp.ESP32_CENTER_Y, 15.5)
        # Cut 2 long arch windows underneath the pin slot (z = 1.5 .. 13.5) so each rail is a light 3-pier bridge!
        arch1 = _centered_box(6.0, 22.0, 12.0, rx, sp.ESP32_CENTER_Y - 14.0, 1.5)
        arch2 = _centered_box(6.0, 22.0, 12.0, rx, sp.ESP32_CENTER_Y + 14.0, 1.5)
        stop_back = _centered_box(4.2, 1.0, 3.0, rx, 17.6, 19.5)
        stop_front = _centered_box(4.2, 1.0, 3.0, rx, 77.4, 19.5)
        body = body + (rail_box - pin_slot - arch1 - arch2) + stop_back + stop_front

    # 3 Cable-Retainer Fingers inside the Under-ESP Tunnel (connected to left rail piers at y=18.5, 47.5, 76.5)
    for fy in (18.5, 47.5, 76.5):
        tunnel_finger = _centered_box(5.0, 4.0, 1.4, -8.8, fy, 8.0)
        body = body + tunnel_finger

    # 9c. Thin Floor Support Ribs under Battery & Buck (`z = 0.0 .. 2.5` mm, 1.8 mm thick)
    for rx_rib in (-22.0, 17.0):
        floor_rib_batt = _centered_box(1.8, 54.0, 3.5, rx_rib, sp.BATT_CENTER_Y, -1.0)
        floor_rib_buck = _centered_box(1.8, 24.0, 3.5, rx_rib, sp.BUCK_CENTER_Y, -1.0)
        body = body + floor_rib_batt + floor_rib_buck

    # 9d. Thin Transverse Divider Wall 1 (1.2 mm thick, at y = 15.8)
    div1 = _centered_box(sp.CAVITY_X + 1.0, 1.2, 16.0, 0.0, 15.8, -1.0)
    cut_div1_center = _centered_box(18.0, 4.0, 18.0, 0.0, 15.8, 0.0)
    cut_div1_right = _centered_box(8.5, 4.0, 18.0, 37.5, 15.8, 0.0)
    cut_div1_left = _centered_box(16.0, 4.0, 11.0, -26.0, 15.8, 4.5)
    body = body + (div1 - cut_div1_center - cut_div1_right - cut_div1_left)

    # 9e. Thin Transverse Divider Wall 2 (1.2 mm thick, at y = -49.4)
    div2 = _centered_box(sp.CAVITY_X + 1.0, 1.2, 16.0, 0.0, -49.4, -1.0)
    cut_div2_center = _centered_box(18.0, 4.0, 18.0, 0.0, -49.4, 0.0)
    cut_div2_right = _centered_box(8.5, 4.0, 18.0, 37.5, -49.4, 0.0)
    cut_div2_left = _centered_box(16.0, 4.0, 11.0, -26.0, -49.4, 4.5)
    body = body + (div2 - cut_div2_center - cut_div2_right - cut_div2_left)

    # 9f. Thin Right-Side Cable Raceway Guide Wall (1.2 mm thick at x = 33.8)
    raceway_wall = _centered_box(1.2, 98.0, 14.0, 33.8, -32.0, -1.0)
    dc_exit_batt = _centered_box(4.0, 22.0, 13.0, 33.8, -36.0, 2.5)
    wire_exit_buck = _centered_box(4.0, 20.0, 13.0, 33.8, -66.0, 2.5)
    body = body + (raceway_wall - dc_exit_batt - wire_exit_buck)

    for rfy in (-76.0, -49.4, -15.0, 15.8):
        rw_finger = _centered_box(4.0, 4.0, 1.4, 35.4, rfy, 12.6)
        body = body + rw_finger

    # Short corner locator ribs on Left side
    rib_batt_l = _centered_box(2.8, 20.0, 13.0, -39.9, sp.BATT_CENTER_Y, -1.0)
    rib_buck_l = _centered_box(2.8, 12.0, 13.0, -39.9, sp.BUCK_CENTER_Y, -1.0)
    body = body + rib_batt_l + rib_buck_l

    # 2 Cantilever Retention Clips for Battery
    batt_clip_f = _centered_box(10.0, 1.4, 25.9, -15.0, 15.5, -1.0) + _centered_box(10.0, 1.5, 1.5, -15.0, 14.1, 23.3)
    batt_clip_b = _centered_box(10.0, 1.4, 25.9, -15.0, -49.1, -1.0) + _centered_box(10.0, 1.5, 1.5, -15.0, -47.7, 23.3)
    body = body + batt_clip_f + batt_clip_b

    body.label = "chasis_bandeja"
    body.color = srgb("#2E3B4E")
    return body


def make_tapa_carcasa_ligero() -> bd.Shape:
    """Lightweight Part 2:
    - Same external footprint and Option B labyrinth + 0.7mm PETG wiper lip + 6 snap clips.
    - Roof hollowed out to a 1.8 mm thin shell (saves ~50% filament on the lid!).
    """
    x_half = sp.OUTER_X / 2.0
    y_half = sp.OUTER_Y / 2.0

    skirt_in_x = sp.OUTER_X + 2.0 * sp.CLEARANCE
    skirt_in_y = sp.OUTER_Y + 2.0 * sp.CLEARANCE
    skirt_out_x = skirt_in_x + 2.0 * sp.LID_SKIRT_THICK
    skirt_out_y = skirt_in_y + 2.0 * sp.LID_SKIRT_THICK

    lid_top_z = sp.INNER_Z + 9.0  # 66.0 mm — identical silhouette to the original lid
    main_block = _centered_box(skirt_out_x, skirt_out_y, lid_top_z - sp.LID_SKIRT_BOTTOM_Z, 0.0, 0.0, sp.LID_SKIRT_BOTTOM_Z)

    # Roof tiers, same outer footprint as the original, but hollowed into a raised border ring
    # and a nameplate plaque (solid plates here cost ~44 cm3 of PETG for zero function).
    tier_out_x = skirt_out_x - 14.0
    tier_out_y = skirt_out_y - 8.0
    roof_tier1 = (
        _centered_box(tier_out_x, tier_out_y, 2.0, 0.0, 0.0, lid_top_z)
        - _centered_box(tier_out_x - 10.0, tier_out_y - 10.0, 2.5, 0.0, 0.0, lid_top_z - 0.2)
    )
    badge_x, badge_y = 46.0, 78.0
    roof_tier2 = (
        _centered_box(badge_x, badge_y, 3.5, 0.0, 0.0, lid_top_z)
        - _centered_box(badge_x - 6.0, badge_y - 6.0, 2.6, 0.0, 0.0, lid_top_z + 1.0)
    )
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

    lip_center_ofs = (sp.GROOVE_OFFSET_IN + sp.GROOVE_OFFSET_OUT) / 2.0
    lip_out_x = sp.INNER_X + 2.0 * (lip_center_ofs + sp.PETG_LIP_THICKNESS / 2.0)
    lip_out_y = sp.INNER_Y + 2.0 * (lip_center_ofs + sp.PETG_LIP_THICKNESS / 2.0)
    lip_in_x = sp.INNER_X + 2.0 * (lip_center_ofs - sp.PETG_LIP_THICKNESS / 2.0)
    lip_in_y = sp.INNER_Y + 2.0 * (lip_center_ofs - sp.PETG_LIP_THICKNESS / 2.0)
    wiper_lip = (
        _centered_box(lip_out_x, lip_out_y, 4.0, 0.0, 0.0, sp.INNER_Z - 3.0)
        - _centered_box(lip_in_x, lip_in_y, 4.5, 0.0, 0.0, sp.INNER_Z - 3.2)
    )
    lid = lid + wiper_lip

    # Deep interior hollowing of the roof (leaves a 2.0 mm roof shell at z = 64.0..66.0)
    roof_shell = 2.0
    dome_recess = _centered_box(
        sp.INNER_X - 1.0,
        sp.INNER_Y - 1.0,
        (lid_top_z - roof_shell) - (sp.LID_CEILING_Z - 0.1),
        0.0,
        0.0,
        sp.LID_CEILING_Z - 0.1,
    )
    lid = lid - dome_recess

    # 6 Cantilever Snap-Fit Clips around perimeter
    clip_z0 = sp.CATCH_Z_BOTTOM - 4.0  # 37.0
    for sy in sp.SIDE_CLIP_Y:
        for sign in (-1.0, 1.0):
            root_bridge = _centered_box(3.2, sp.CLIP_WIDTH, 5.5, sign * (x_half + 2.5), sy, sp.LID_SKIRT_BOTTOM_Z)
            arm = _centered_box(2.0, sp.CLIP_WIDTH, 20.0, sign * (x_half + 3.3), sy, clip_z0)
            tooth = _centered_box(2.3, sp.CLIP_WIDTH, 2.15, sign * (x_half + 1.5), sy, clip_z0 + 1.5)
            grip = _centered_box(1.6, sp.CLIP_WIDTH, 1.8, sign * (x_half + 4.6), sy, clip_z0)
            lid = lid + root_bridge + arm + tooth + grip

    for rx in sp.REAR_CLIP_X:
        root_bridge = _centered_box(sp.CLIP_WIDTH, 3.2, 5.5, rx, -(y_half + 2.5), sp.LID_SKIRT_BOTTOM_Z)
        arm = _centered_box(sp.CLIP_WIDTH, 2.0, 20.0, rx, -(y_half + 3.3), clip_z0)
        tooth = _centered_box(sp.CLIP_WIDTH, 2.3, 2.15, rx, -(y_half + 1.5), clip_z0 + 1.5)
        grip = _centered_box(sp.CLIP_WIDTH, 1.6, 1.8, rx, -(y_half + 4.6), clip_z0)
        lid = lid + root_bridge + arm + tooth + grip

    lid.label = "tapa_carcasa"
    lid.color = srgb("#3E5066")
    return lid


def make_ventana_pc_ligero() -> bd.Shape:
    """Part 3a: Clear polycarbonate/acrylic optical window plate (25 x 25 x 2.0 mm)."""
    win = _centered_box(sp.WINDOW_SIZE, sp.WINDOW_THICK, sp.WINDOW_SIZE, 0.0, sp.WINDOW_POCKET_Y0 + 1.45, sp.OPTICAL_CENTER_Z - sp.WINDOW_SIZE / 2.0)
    win.label = "ventana_pc"
    win.color = srgb("#A8D8EA", 0.38)
    return win


def make_bisel_ventana_ligero() -> bd.Shape:
    """Lightweight Part 3b: Thinned window bezel (1.5 mm front plate)."""
    y_front = sp.OUTER_Y / 2.0
    bz_w = sp.WINDOW_BOSS_W + 2.0 * (0.35 + 1.6)
    bz_h = sp.WINDOW_BOSS_H + 2.0 * (0.35 + 1.15)
    z0 = sp.OPTICAL_CENTER_Z - bz_h / 2.0

    front_plate = _centered_box(bz_w, 1.6, bz_h, 0.0, y_front + 4.8, z0)
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
        bridge = _centered_box(2.8, 1.5, 10.0, sign * 19.95, y_front + 5.0, sp.OPTICAL_CENTER_Z - 5.0)
        arm = _centered_box(1.6, 5.4, 10.0, sign * 20.65, y_front + 3.05, sp.OPTICAL_CENTER_Z - 5.0)
        tooth = _centered_box(2.0, 1.15, 10.0, sign * 19.55, y_front + 0.925, sp.OPTICAL_CENTER_Z - 5.0)
        bezel = bezel + bridge + arm + tooth

    bezel.label = "bisel_ventana"
    bezel.color = srgb("#D97724")
    return bezel


def make_parasol_capucha_ligero() -> bd.Shape:
    """Lightweight Part 4: 1.6 mm thin-wall glare hood & rain visor."""
    y_front = sp.OUTER_Y / 2.0
    z_base = 9.85
    hood = _centered_box(65.0, 1.8, 33.65, 0.0, y_front + 4.75, z_base) - _centered_box(46.0, 4.0, 32.0, 0.0, y_front + 4.75, z_base - 0.35)

    for sign in (-1.0, 1.0):
        side_wall = _centered_box(1.8, 3.6, 30.4, sign * 31.3, y_front + 2.15, z_base)
        back_lip = _centered_box(2.5, 0.8, 30.4, sign * 29.75, y_front + 0.75, z_base)
        hood = hood + side_wall + back_lip

    visor_roof = _centered_box(68.0, 34.0, 1.6, 0.0, y_front + 21.0, z_base + 32.05)
    hood = hood + visor_roof
    for sign in (-1.0, 1.0):
        baffle = _centered_box(1.6, 34.0, 29.5, sign * 33.2, y_front + 21.0, z_base + 3.15)
        hood = hood + baffle

    hood.label = "parasol_capucha"
    hood.color = srgb("#232B35")
    return hood


def make_tarjeta_azul_ligero() -> bd.Shape:
    """Standard 100 x 250 x 1.0 mm Blue Sticky Trap Card."""
    card = _centered_box(sp.CARD_WIDTH_X, sp.CARD_THICK_Y, sp.CARD_HEIGHT_Z, 0.0, sp.CARD_WORLD_Y, sp.CARD_BOTTOM_Z)
    card.label = "tarjeta_azul"
    card.color = srgb("#0077FF")
    return card


def make_marco_tarjeta_ligero() -> bd.Shape:
    """Lightweight Part 5: Thinned C-channels and lightened top arch (~38% less filament)."""
    yc = sp.CARD_WORLD_Y
    frame = _centered_box(112.0, 9.0, 5.5, 0.0, yc, 10.0)
    card_slot_bottom = _centered_box(100.8, 2.4, 5.0, 0.0, yc, 12.6)
    cross_relief = _centered_box(94.0, 12.0, 4.0, 0.0, yc, 13.5)
    drain1 = _centered_box(14.0, 2.4, 8.0, -25.0, yc, 9.0)
    drain2 = _centered_box(14.0, 2.4, 8.0, 25.0, yc, 9.0)
    frame = frame - card_slot_bottom - cross_relief - drain1 - drain2

    for sign in (-1.0, 1.0):
        # Keep bottom socket stub (Z = 10..38) at full 9.5 x 9.0 mm to fit soporte_base,
        # and thin the upper channel (Z = 38..232) to 6.5 x 6.0 mm (1.8 mm walls)!
        c_stub = _centered_box(9.5, 9.0, 28.0, sign * 51.25, yc, 10.0)
        c_upper = _centered_box(6.5, 6.0, 195.0, sign * 49.75, yc, 37.0)
        c_slot = _centered_box(5.0, 2.4, 225.0, sign * 48.3, yc, 12.6)
        c_open = _centered_box(4.5, 12.0, 225.0, sign * 47.0, yc, 13.5)
        frame = frame + (c_stub + c_upper - c_slot - c_open)

    rear_mid_bar = _centered_box(104.0, 2.0, 5.0, 0.0, yc + 2.5, 125.0)
    frame = frame + rear_mid_bar

    for sign in (-1.0, 1.0):
        step_arm = _centered_box(4.0, 20.0, 5.5, sign * 52.4, yc - 7.5, 226.5)
        riser = _centered_box(4.0, 5.5, 25.5, sign * 52.4, yc - 15.5, 226.5)
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


def make_soporte_base_ligero() -> bd.Shape:
    """Lightweight Part 6:
    - Same external footprint (128 x 246 mm) and same Pod/Frame mating interfaces.
    - Underside of all runners & crossbeams hollowed to a 3.2 mm C-channel shell (invisible from above!).
    - Pedestal columns & gussets hollowed out with side lightening windows (saves >55% filament!).
    """
    # 1. Table Base Runners & Crossbeams (outer Z = 0..10, hollowed underneath Z = 0..6.8)
    base = _centered_box(128.0, 20.0, 10.0, 0.0, -140.0, 0.0) - _centered_box(120.0, 14.0, 7.0, 0.0, -140.0, -0.2)
    base = base + (_centered_box(128.0, 22.0, 10.0, 0.0, 85.0, 0.0) - _centered_box(96.0, 16.0, 7.0, 0.0, 85.0, -0.2))
    base = base + (_centered_box(128.0, 18.0, 10.0, 0.0, -25.0, 0.0) - _centered_box(96.0, 12.0, 7.0, 0.0, -25.0, -0.2))
    for sign in (-1.0, 1.0):
        runner = _centered_box(16.0, 246.0, 10.0, sign * 56.0, -27.0, 0.0)
        r_hollow1 = _centered_box(10.5, 92.0, 7.0, sign * 56.0, -83.0, -0.2)
        r_hollow2 = _centered_box(10.5, 88.0, 7.0, sign * 56.0, 29.0, -0.2)
        base = base + (runner - r_hollow1 - r_hollow2)

    # 2. Rear Snap-Fit Socket Towers for `marco_tarjeta` (thinned walls)
    for sign in (-1.0, 1.0):
        outer_tower = _centered_box(5.0, 18.0, 38.0, sign * 58.85, 85.0, 0.0)
        front_lip = _centered_box(9.5, 3.0, 38.0, sign * 56.6, 76.6, 0.0)
        rear_lip = _centered_box(9.5, 3.0, 38.0, sign * 56.6, 93.4, 0.0)
        base = base + outer_tower + front_lip + rear_lip

    # 3. Hollowed Front Pedestal Columns & Lightened T-Rail Platform
    y_ped = sp.POD_WORLD_Y + 10.0  # -115.0
    for sign in (-1.0, 1.0):
        col = _centered_box(10.0, 68.0, 96.0, sign * 16.0, y_ped, 8.0)
        # 4 truss windows per column, each closed by a self-supporting arch on top
        # (16 mm piers left; no unsupported flat bridge inside the load-bearing column)
        col_cuts = None
        for wy in (y_ped - 14.0, y_ped + 14.0):
            for wz0, wz1 in ((14.0, 52.0), (58.0, 96.0)):
                c = _arched_window(14.0, 24.0, wz0, wz1, sign * 16.0, wy)
                col_cuts = c if col_cuts is None else col_cuts + c
        gusset = _centered_box(4.0, 42.0, 36.0, sign * 16.0, y_ped + 40.0, 8.0) - _centered_box(8.0, 24.0, 22.0, sign * 16.0, y_ped + 43.0, 14.0)
        base = base + (col - col_cuts) + gusset

    top_bridge = _centered_box(44.0, 72.0, 4.0, 0.0, y_ped, 99.65) - _centered_box(22.0, 56.0, 6.0, 0.0, y_ped, 98.0)
    t_neck = _centered_box(44.0, 72.0, 4.5, 0.0, y_ped, 103.0) - _centered_box(36.0, 60.0, 6.0, 0.0, y_ped, 102.0)
    t_flange = _centered_box(50.8, 72.0, 2.2, 0.0, y_ped, 107.2) - _centered_box(36.0, 60.0, 4.0, 0.0, y_ped, 106.5)
    latch_arm = _centered_box(16.0, 26.0, 3.0, 0.0, y_ped + 44.0, 99.0)
    front_latch = _centered_box(16.0, 2.2, 8.5, 0.0, y_ped + 55.75, 100.0)
    base = base + top_bridge + t_neck + t_flange + latch_arm + front_latch

    base.label = "soporte_base"
    base.color = srgb("#4A5568")
    return base


def make_componentes_internos_ligero() -> bd.Shape:
    """Reference electronic components & routed power cables inside `chasis_bandeja_ligero`."""
    children = []

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

    batt_pack = _centered_box(sp.BATT_WID_X, sp.BATT_LEN_Y, sp.BATT_H_Z, sp.BATT_CENTER_X, sp.BATT_CENTER_Y, sp.BATT_BASE_Z)
    batt_pack.label = "bateria_12v_4000mah"
    batt_pack.color = srgb("#1565C0")
    children.append(batt_pack)

    buck = _centered_box(sp.BUCK_WID_X, sp.BUCK_LEN_Y, sp.BUCK_H_Z, sp.BUCK_CENTER_X, sp.BUCK_CENTER_Y, sp.BUCK_BASE_Z)
    buck.label = "buck_70x30x20"
    buck.color = srgb("#0D47A1")
    children.append(buck)

    c12_out = _centered_box(4.2, 3.0, 3.0, 35.1, -36.0, 4.5)
    c12_run = _centered_box(3.0, 33.0, 3.0, 37.2, -51.0, 4.5)
    c12_in = _centered_box(4.2, 3.0, 3.0, 35.1, -66.0, 4.5)
    cable_12v = c12_out + c12_run + c12_in
    cable_12v.label = "cable_12v_bateria_buck"
    cable_12v.color = srgb("#E53935")
    children.append(cable_12v)

    c3v_trench = _centered_box(4.0, 128.0, 1.8, 0.0, 14.3, 0.4)
    c3v_riser = _centered_box(4.0, 1.6, 32.5, 0.0, 77.5, 0.4)
    c3v_bridge = _centered_box(15.0, 3.0, 2.2, -5.85, 76.0, 31.0)
    cable_3v3 = c3v_trench + c3v_riser + c3v_bridge
    cable_3v3.label = "cable_3v3_buck_esp"
    cable_3v3.color = srgb("#FB8C00")
    children.append(cable_3v3)

    return bd.Compound(children=children, label="componentes_internos")
