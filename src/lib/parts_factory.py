"""Parametric build123d factories for all parts of the Trampa de Trips."""

from __future__ import annotations

from cadgen import build123d as bd
from cadgen import srgb

from lib import specs as sp


def _centered_box(dx: float, dy: float, dz: float, cx: float = 0.0, cy: float = 0.0, z0: float = 0.0) -> bd.Solid:
    """Create a box centered at (cx, cy) in XY and spanning [z0, z0 + dz] in Z."""
    return bd.Pos(cx, cy, z0 + dz / 2.0) * bd.Box(dx, dy, dz)


def make_chasis_bandeja() -> bd.Shape:
    """Part 1: Main sealed pod tray with internal snap-fit cradles (removable 12V 4000mAh
    battery bay with finger cutouts + universal connector clamp, LM2596 12V->3.3V buck,
    ESP32-S3 58x28, OV5640, switch, status LED, silica cage), cable channels,
    Option B labyrinth male ridge + sealing groove, 6 perimeter clip catches,
    front optical window boss, and bottom mounting T-rail socket.
    """
    x_half = sp.OUTER_X / 2.0  # 59.0
    y_front = sp.OUTER_Y / 2.0  # 64.0

    # 1. Main outer block (x in [-59, 59], y in [-64, 64], z in [-3, 38])
    outer = _centered_box(sp.OUTER_X, sp.OUTER_Y, sp.INNER_Z + sp.FLOOR_T, 0.0, 0.0, -sp.FLOOR_T)

    # 2. Subtract main interior cavity (two-step for 5mm top sealing rim)
    lower_cav = _centered_box(sp.INNER_X + 2.0, sp.INNER_Y + 2.0, 33.0, 0.0, 0.0, 0.0)
    upper_cav = _centered_box(sp.INNER_X, sp.INNER_Y, 7.0, 0.0, 0.0, 32.0)
    body = outer - lower_cav - upper_cav

    # 3. Option B Sealing Groove in top rim (z = 34.5 .. 38.5)
    g_out_x = sp.INNER_X + 2.0 * sp.GROOVE_OFFSET_OUT
    g_out_y = sp.INNER_Y + 2.0 * sp.GROOVE_OFFSET_OUT
    g_in_x = sp.INNER_X + 2.0 * sp.GROOVE_OFFSET_IN
    g_in_y = sp.INNER_Y + 2.0 * sp.GROOVE_OFFSET_IN
    groove_ring = (
        _centered_box(g_out_x, g_out_y, sp.GROOVE_DEPTH + 0.5, 0.0, 0.0, sp.INNER_Z - sp.GROOVE_DEPTH)
        - _centered_box(g_in_x, g_in_y, sp.GROOVE_DEPTH + 1.0, 0.0, 0.0, sp.INNER_Z - sp.GROOVE_DEPTH - 0.2)
    )
    body = body - groove_ring

    # 4. Option B Labyrinth Male Ridge rising above top rim (z = 38.0 .. 41.0)
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

    # 6. Front Optical Window Boss (+Y face at y = +64.0, z in [1.0, 30.0], y in [64.0, 67.5])
    boss = _centered_box(sp.WINDOW_BOSS_W, sp.WINDOW_BOSS_PROJ + 1.0, sp.WINDOW_BOSS_H, 0.0, y_front + (sp.WINDOW_BOSS_PROJ - 1.0) / 2.0, 1.0)
    bezel_catch_l = _centered_box(2.5, 1.3, 12.0, -sp.WINDOW_BOSS_W / 2.0 - 0.25, y_front + 2.55, sp.OPTICAL_CENTER_Z - 6.0)
    bezel_catch_r = _centered_box(2.5, 1.3, 12.0, sp.WINDOW_BOSS_W / 2.0 + 0.25, y_front + 2.55, sp.OPTICAL_CENTER_Z - 6.0)
    body = body + boss + bezel_catch_l + bezel_catch_r

    # Cut Window Pocket (25.6 x 25.6 mm, centered at z=15.5 -> z in [2.7, 28.3], from y = 65.2 to 68.5)
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

    # Option B Printed PETG Window Sealing Ridge on pocket seat (y = 65.2 .. 65.45)
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

    # 7. Two Vertical L-Rails on Front Wall for Glare Hood (`parasol_capucha`, z in [0.0, 31.0])
    for sign in (-1.0, 1.0):
        web = _centered_box(2.5, 4.5, 31.0, sign * 26.75, y_front + 1.25, 0.0)
        flange = _centered_box(2.0, 2.0, 31.0, sign * 29.0, y_front + 2.5, 0.0)
        stop = _centered_box(4.5, 4.5, 3.0, sign * 27.75, y_front + 1.25, -3.0)
        body = body + web + flange + stop

    # 8. Bottom Mounting T-Rail Socket (`encaje_inferior_pod`, z = -9.0 .. -3.0)
    for sign in (-1.0, 1.0):
        rail_wall = _centered_box(3.5, 90.0, 7.0, sign * 34.25, 0.0, -9.0)
        rail_lip = _centered_box(7.5, 90.0, 2.5, sign * 32.25, 0.0, -9.0)
        body = body + rail_wall + rail_lip
    rear_stop = _centered_box(72.0, 3.0, 7.0, 0.0, -43.5, -9.0)
    body = body + rear_stop

    # 9. Waterproof Translucent Status LED Bore in Right Wall (leaves 0.8 mm PETG outer window at x = 58.2..59.0)
    led_bore = (
        bd.Pos(x_half - 3.0, 14.0, 10.0)
        * bd.Rot(0.0, 90.0, 0.0)
        * bd.Cylinder(radius=3.0, height=4.4)
    )
    body = body - led_bore

    # 10. Internal Component Cradles & Cable Routing Channels (fused into floor z = -1.0 .. 0.0)
    # 10a. OV5640 Camera + LED Ring Cradle behind front wall (y_inner = +59.0)
    # Carrier PCB is 24x24x1.5 at y=56.05..57.55, centered at x=0.0, z=15.5 -> z in [3.5, 27.5]
    for sign in (-1.0, 1.0):
        pillar = _centered_box(3.2, 6.5, 30.0, sign * 13.9, y_front - 7.25, -1.0)
        slot_cut = _centered_box(2.0, 2.4, 26.0, sign * 12.8, y_front - 7.2, 3.1)
        nib = _centered_box(3.2, 2.2, 1.6, sign * 13.2, y_front - 7.2, 27.9)
        body = body + (pillar - slot_cut) + nib
    cam_bottom_support = (
        _centered_box(26.0, 6.5, 4.1, 0.0, y_front - 7.25, -1.0)
        - _centered_box(16.0, 8.0, 6.0, 0.0, y_front - 7.25, 1.0)
    )
    body = body + cam_bottom_support

    # 10b. ESP32-S3 Cradle (58 x 28 mm board centered at x=+4.0, y=30.5, PCB at z=6.0..7.6)
    for sx in (-1.0, 1.0):
        for sy in (-1.0, 1.0):
            px = sp.ESP32_CENTER_X + sx * (sp.ESP32_LEN_X / 2.0 + 1.9)  # 4.0 +- 30.9 -> -26.9, +34.9
            py = sp.ESP32_CENTER_Y + sy * (sp.ESP32_WID_Y / 2.0 + 1.9)  # 30.5 +- 15.9 -> 14.6, 46.4
            post = _centered_box(3.2, 3.2, 12.0, px, py, -1.0)
            ledge = _centered_box(
                3.0,
                3.0,
                6.7,
                sp.ESP32_CENTER_X + sx * (sp.ESP32_LEN_X / 2.0 - 0.8),
                sp.ESP32_CENTER_Y + sy * (sp.ESP32_WID_Y / 2.0 - 0.8),
                -1.0,
            )
            hook = _centered_box(2.2, 3.2, 1.5, sp.ESP32_CENTER_X + sx * (sp.ESP32_LEN_X / 2.0 - 0.2), py, 9.5)
            body = body + post + ledge + hook

    # 10c. Removable 12V 4000mAh 18650 3S1P Battery Pack Bay (70 x 60 x 20 mm centered at x=-14.0, y=-26.5)
    # Pack spans x in [-49.0, +21.0], y in [-56.5, +3.5], z in [0.4, 20.4].
    bx0, by0 = sp.BATT_CENTER_X, sp.BATT_CENTER_Y
    bw, bl = sp.BATT_LEN_X + 0.8, sp.BATT_WID_Y + 0.8  # 70.8 x 60.8 inner pocket
    batt_outer = _centered_box(bw + 4.4, bl + 4.0, 15.0, bx0, by0, -1.0)
    batt_inner = _centered_box(bw, bl, 17.0, bx0, by0, 0.0)
    # Wide finger-extraction cutouts (`muescas_extraccion`) on Left and Right walls so user can grab and lift pack
    finger_cut_x = _centered_box(bw + 8.0, 32.0, 13.0, bx0, by0, 3.0)
    # Wire exit slot at front-right corner of battery bay (around x = +16..+21, y = +3.5)
    wire_exit_cut = _centered_box(12.0, 8.0, 15.0, bx0 + bw / 2.0 - 6.0, by0 + bl / 2.0, 1.5)
    batt_cradle = batt_outer - batt_inner - finger_cut_x - wire_exit_cut
    # Two flexible cantilever snap-retainer clips at front and rear of bay (z up to 22.8, tooth at z=20.8..22.6)
    for sy in (-1.0, 1.0):
        cy_clip = by0 + sy * (bl / 2.0 + 1.0)
        clip_arm = _centered_box(16.0, 2.0, 23.8, bx0 - 4.0, cy_clip, -1.0)
        clip_tooth = _centered_box(16.0, 1.6, 1.8, bx0 - 4.0, by0 + sy * (bl / 2.0 - 0.4), 20.8)
        batt_cradle = batt_cradle + clip_arm + clip_tooth
    body = body + batt_cradle

    # Universal Cable Strain-Relief & Connector Clamp (`abrazadera_cable_conector`, at x=+18.0, y=+7.5)
    # Holds the battery's DC barrel plug / JST / wire lead in place without needing reprints if connector changes
    clamp_base = _centered_box(10.0, 6.0, 9.5, 18.0, 7.5, -1.0) - _centered_box(5.6, 8.0, 8.0, 18.0, 7.5, 1.5)
    clamp_lip = _centered_box(2.0, 6.0, 1.4, 15.6, 7.5, 7.1)
    body = body + clamp_base + clamp_lip

    # 10d. LM2596 DC-DC Buck Converter Cradle (12V -> 3.3V, 21 x 43 mm module at x=-42.0, y=30.5)
    # Inner pocket 21.8 x 43.8 mm, outer 25.0 x 47.0 mm -> x in [-54.5, -29.5], clear of ESP32 posts at -28.5!
    buck_outer = _centered_box(25.0, 47.0, 8.5, sp.BUCK_CENTER_X, sp.BUCK_CENTER_Y, -1.0)
    buck_inner = _centered_box(21.8, 43.8, 10.0, sp.BUCK_CENTER_X, sp.BUCK_CENTER_Y, 0.0)
    buck_open = _centered_box(14.0, 50.0, 9.0, sp.BUCK_CENTER_X, sp.BUCK_CENTER_Y, 1.5)
    body = body + (buck_outer - buck_inner - buck_open)

    # 10e. Slide Switch Cradle (at x=+44.5, y=35.0, inner 8.6 x 19.6)
    sw_outer = _centered_box(12.6, 23.6, 10.0, sp.SWITCH_CENTER_X, sp.SWITCH_CENTER_Y, -1.0)
    sw_inner = _centered_box(8.6, 19.6, 12.0, sp.SWITCH_CENTER_X, sp.SWITCH_CENTER_Y, 0.0)
    body = body + (sw_outer - sw_inner)

    # 10f. Status LED Cradle Collar (at x=+49.5, y=14.0)
    led_holder = _centered_box(6.0, 9.0, 12.0, 49.5, 14.0, -1.0) - (
        bd.Pos(49.5, 14.0, 10.0) * bd.Rot(0.0, 90.0, 0.0) * bd.Cylinder(radius=2.8, height=10.0)
    )
    body = body + led_holder

    # 10g. Desiccant Silica Gel Perforated Cage (at x=+39.5, y=-26.5, inner 19.0 x 42.0)
    des_outer = _centered_box(23.0, 46.0, 15.0, sp.DESICCANT_CENTER_X, sp.DESICCANT_CENTER_Y, -1.0)
    des_inner = _centered_box(19.0, 42.0, 17.0, sp.DESICCANT_CENTER_X, sp.DESICCANT_CENTER_Y, 0.0)
    des_cage = des_outer - des_inner
    for slot_y in (-38.5, -26.5, -14.5):
        des_cage = des_cage - _centered_box(28.0, 5.0, 11.0, sp.DESICCANT_CENTER_X, slot_y, 3.0)
    body = body + des_cage

    # 10h. Integrated Cable Routing Channels with Retainer Fingers (along y = 7.5..11.5 mm corridor, x in [-27, +15])
    ch_wall_1 = _centered_box(42.0, 1.6, 6.5, -6.0, 7.5, -1.0)
    ch_wall_2 = _centered_box(42.0, 1.6, 6.5, -6.0, 11.2, -1.0)
    body = body + ch_wall_1 + ch_wall_2
    for fx in (-20.0, -6.0, 8.0):
        finger = _centered_box(5.0, 2.6, 1.3, fx, 8.3, 4.2)
        body = body + finger

    body.label = "chasis_bandeja"
    body.color = srgb("#2E3B4E")
    return body


def make_tapa_carcasa() -> bd.Shape:
    """Part 2: Top cover with Option B labyrinth female channel, 0.7mm flexible PETG
    wiper lip, outer labyrinth skirt, sloped rain-shedding roof, and 6 cantilever snap clips.
    """
    x_half = sp.OUTER_X / 2.0  # 59.0
    y_half = sp.OUTER_Y / 2.0  # 64.0

    skirt_in_x = sp.OUTER_X + 2.0 * sp.CLEARANCE
    skirt_in_y = sp.OUTER_Y + 2.0 * sp.CLEARANCE
    skirt_out_x = skirt_in_x + 2.0 * sp.LID_SKIRT_THICK
    skirt_out_y = skirt_in_y + 2.0 * sp.LID_SKIRT_THICK

    lid_top_z = 47.0
    main_block = _centered_box(skirt_out_x, skirt_out_y, lid_top_z - sp.LID_SKIRT_BOTTOM_Z, 0.0, 0.0, sp.LID_SKIRT_BOTTOM_Z)

    roof_tier1 = _centered_box(skirt_out_x - 16.0, skirt_out_y - 8.0, 2.5, 0.0, 0.0, lid_top_z - 0.5)
    roof_tier2 = _centered_box(skirt_out_x - 40.0, skirt_out_y - 16.0, 2.0, 0.0, 0.0, lid_top_z + 1.5)
    lid = main_block + roof_tier1 + roof_tier2

    under_cut = _centered_box(skirt_in_x, skirt_in_y, sp.LID_CEILING_Z - sp.LID_SKIRT_BOTTOM_Z + 1.0, 0.0, 0.0, sp.LID_SKIRT_BOTTOM_Z - 1.0)
    lid = lid - under_cut

    fem_out_x = sp.INNER_X + 2.0 * (sp.RIDGE_OFFSET_OUT + 0.35)
    fem_out_y = sp.INNER_Y + 2.0 * (sp.RIDGE_OFFSET_OUT + 0.35)
    fem_in_x = sp.INNER_X + 2.0 * (sp.RIDGE_OFFSET_IN - 0.35)
    fem_in_y = sp.INNER_Y + 2.0 * (sp.RIDGE_OFFSET_IN - 0.35)
    fem_groove = (
        _centered_box(fem_out_x, fem_out_y, 3.6, 0.0, 0.0, 38.0)
        - _centered_box(fem_in_x, fem_in_y, 4.0, 0.0, 0.0, 37.8)
    )
    lid = lid - fem_groove

    lip_out_x = sp.INNER_X + 2.0 * (1.80 + sp.PETG_LIP_THICKNESS / 2.0)
    lip_out_y = sp.INNER_Y + 2.0 * (1.80 + sp.PETG_LIP_THICKNESS / 2.0)
    lip_in_x = sp.INNER_X + 2.0 * (1.80 - sp.PETG_LIP_THICKNESS / 2.0)
    lip_in_y = sp.INNER_Y + 2.0 * (1.80 - sp.PETG_LIP_THICKNESS / 2.0)
    wiper_lip = (
        _centered_box(lip_out_x, lip_out_y, 4.0, 0.0, 0.0, 35.0)
        - _centered_box(lip_in_x, lip_in_y, 4.5, 0.0, 0.0, 34.8)
    )
    lid = lid + wiper_lip

    dome_recess = _centered_box(sp.INNER_X - 4.0, sp.INNER_Y - 4.0, 4.6, 0.0, 0.0, sp.LID_CEILING_Z - 0.1)
    lid = lid - dome_recess

    # 6 Cantilever Snap-Fit Clips around perimeter (hooking under catch lugs at z = 22.0)
    for sy in sp.SIDE_CLIP_Y:
        for sign in (-1.0, 1.0):
            root_bridge = _centered_box(3.2, sp.CLIP_WIDTH, 5.5, sign * (x_half + 3.1), sy, 34.5)
            arm = _centered_box(2.4, sp.CLIP_WIDTH, 20.0, sign * (x_half + 3.5), sy, 18.0)
            tooth = _centered_box(2.5, sp.CLIP_WIDTH, 2.15, sign * (x_half + 1.6), sy, 19.5)
            grip = _centered_box(1.8, sp.CLIP_WIDTH, 2.0, sign * (x_half + 5.0), sy, 18.0)
            lid = lid + root_bridge + arm + tooth + grip

    for rx in sp.REAR_CLIP_X:
        root_bridge = _centered_box(sp.CLIP_WIDTH, 3.2, 5.5, rx, -(y_half + 3.1), 34.5)
        arm = _centered_box(sp.CLIP_WIDTH, 2.4, 20.0, rx, -(y_half + 3.5), 18.0)
        tooth = _centered_box(sp.CLIP_WIDTH, 2.5, 2.15, rx, -(y_half + 1.6), 19.5)
        grip = _centered_box(sp.CLIP_WIDTH, 1.8, 2.0, rx, -(y_half + 5.0), 18.0)
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
    y_front = sp.OUTER_Y / 2.0  # 64.0
    bz_w = sp.WINDOW_BOSS_W + 2.0 * (0.35 + 2.0)          # 40.7
    bz_h = sp.WINDOW_BOSS_H + 2.0 * (0.35 + 1.15)         # 32.0
    z0 = -0.50

    front_plate = _centered_box(bz_w, 2.0, bz_h, 0.0, y_front + 5.0, z0)
    skirt_outer = _centered_box(bz_w, 2.8, bz_h, 0.0, y_front + 2.8, z0)
    skirt_inner = _centered_box(sp.WINDOW_BOSS_W + 0.70, 3.4, sp.WINDOW_BOSS_H + 0.70, 0.0, y_front + 2.7, 0.65)
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
    """Part 4: Slide-on glare-blocking hood / rain visor that engages the front L-rails."""
    y_front = sp.OUTER_Y / 2.0  # 64.0
    hood = _centered_box(65.0, 2.5, 33.65, 0.0, y_front + 5.1, 0.35) - _centered_box(46.0, 4.0, 32.0, 0.0, y_front + 5.1, 0.0)

    for sign in (-1.0, 1.0):
        side_wall = _centered_box(2.1, 4.0, 30.4, sign * 31.45, y_front + 2.35, 0.35)
        back_lip = _centered_box(2.7, 0.8, 30.4, sign * 29.75, y_front + 0.75, 0.35)
        hood = hood + side_wall + back_lip

    visor_roof = _centered_box(68.0, 35.0, 2.2, 0.0, y_front + 21.5, 31.8)
    hood = hood + visor_roof
    for sign in (-1.0, 1.0):
        baffle = _centered_box(2.5, 35.0, 29.0, sign * 32.75, y_front + 21.5, 3.5)
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
    """Part 5: Open frame for the 100 x 250 mm blue sticky card + balanced overhead hanging hook.
    Total Z height is 244.0 mm (Z = 10.0 .. 254.0 mm) so it fits flat on a 256x256 mm print bed.
    """
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
    base = _centered_box(128.0, 20.0, 10.0, 0.0, -132.0, 0.0)
    base = base + _centered_box(128.0, 22.0, 10.0, 0.0, 85.0, 0.0)
    base = base + _centered_box(128.0, 18.0, 10.0, 0.0, -25.0, 0.0)
    for sign in (-1.0, 1.0):
        runner = _centered_box(16.0, 238.0, 10.0, sign * 56.0, -23.0, 0.0)
        base = base + runner

    for sign in (-1.0, 1.0):
        outer_tower = _centered_box(7.65, 22.0, 38.0, sign * 60.175, 85.0, 0.0)
        front_lip = _centered_box(12.0, 4.0, 38.0, sign * 58.0, 76.1, 0.0)
        rear_lip = _centered_box(12.0, 4.0, 38.0, sign * 58.0, 93.9, 0.0)
        base = base + outer_tower + front_lip + rear_lip

    y_ped = sp.POD_WORLD_Y  # -110.0
    for sign in (-1.0, 1.0):
        col = _centered_box(12.0, 74.0, 101.0, sign * 20.0, y_ped, 8.0)
        gusset = _centered_box(8.0, 45.0, 45.0, sign * 20.0, y_ped + 40.0, 8.0)
        base = base + col + gusset

    top_bridge = _centered_box(55.0, 76.0, 5.65, 0.0, y_ped, 103.0)
    t_neck = _centered_box(56.0, 76.0, 4.5, 0.0, y_ped, 108.0)
    t_flange = _centered_box(64.0, 76.0, 2.7, 0.0, y_ped, 111.9)
    latch_arm = _centered_box(24.0, 14.0, 4.0, 0.0, y_ped + 41.0, 103.0)
    front_latch = _centered_box(24.0, 2.5, 9.5, 0.0, y_ped + 46.75, 105.0)
    base = base + top_bridge + t_neck + t_flange + latch_arm + front_latch

    base.label = "soporte_base"
    base.color = srgb("#4A5568")
    return base


def make_componentes_internos() -> bd.Shape:
    """Reference electronic components inside `chasis_bandeja` (in Pod-Local Frame):
    - ESP32-S3 (58 x 28 mm) + USB-C + microSD
    - OV5640 Camera Module + 4-LED Illumination Ring + FPC Ribbon
    - 12V 4000mAh 18650 3S1P Lithium Pack (70 x 60 x 20 mm, blue shrink-wrap) + DC plug lead
    - LM2596 DC-DC Buck Converter (12V -> 3.3V, 21 x 43 mm)
    - Slide Switch + Status RGB LED + Silica Gel Desiccant Packet
    """
    y_front = sp.OUTER_Y / 2.0  # 64.0
    children = []

    # 1. ESP32-S3 PCB (58 x 28 x 1.6 mm at x=+4.0, y=30.5, z=6.0..7.6)
    esp_pcb = _centered_box(sp.ESP32_LEN_X, sp.ESP32_WID_Y, sp.ESP32_THICK, sp.ESP32_CENTER_X, sp.ESP32_CENTER_Y, sp.ESP32_BASE_Z)
    esp_pcb.label = "esp32_s3_pcb"
    esp_pcb.color = srgb("#1B5E20")
    children.append(esp_pcb)

    esp_shield = _centered_box(18.0, 18.0, 3.2, sp.ESP32_CENTER_X - 8.0, sp.ESP32_CENTER_Y, sp.ESP32_BASE_Z + sp.ESP32_THICK)
    esp_shield.label = "esp32_s3_wroom"
    esp_shield.color = srgb("#B0BEC5")
    children.append(esp_shield)

    usbc = _centered_box(7.5, 9.0, 3.2, sp.ESP32_CENTER_X - sp.ESP32_LEN_X / 2.0 + 3.0, sp.ESP32_CENTER_Y, sp.ESP32_BASE_Z + sp.ESP32_THICK)
    usbc.label = "esp32_usbc"
    usbc.color = srgb("#CFD8DC")
    children.append(usbc)

    sd_slot = _centered_box(14.0, 15.0, 2.2, sp.ESP32_CENTER_X + sp.ESP32_LEN_X / 2.0 - 8.0, sp.ESP32_CENTER_Y, sp.ESP32_BASE_Z + sp.ESP32_THICK)
    sd_slot.label = "ranura_microsd"
    sd_slot.color = srgb("#90A4AE")
    children.append(sd_slot)

    # 2. OV5640 Camera Carrier + Lens Barrel (at y = 56.8..63.4, z = 15.5)
    cam_pcb = _centered_box(sp.OV5640_PCB_SIZE, 1.5, sp.OV5640_PCB_SIZE, 0.0, y_front - 7.2, sp.OPTICAL_CENTER_Z - sp.OV5640_PCB_SIZE / 2.0)
    cam_pcb.label = "ov5640_carrier_pcb"
    cam_pcb.color = srgb("#263238")
    children.append(cam_pcb)

    cam_lens = (
        bd.Pos(0.0, y_front - 3.5, sp.OPTICAL_CENTER_Z)
        * bd.Rot(90.0, 0.0, 0.0)
        * bd.Cylinder(radius=sp.OV5640_LENS_DIA / 2.0, height=5.8)
    )
    cam_lens.label = "ov5640_lente"
    cam_lens.color = srgb("#111111")
    children.append(cam_lens)

    # 3. 12V 4000mAh 18650 3S1P Lithium Battery Pack (70 x 60 x 20 mm at x=-14.0, y=-26.5, z=0.4..20.4)
    batt_pack = _centered_box(sp.BATT_LEN_X, sp.BATT_WID_Y, sp.BATT_H_Z, sp.BATT_CENTER_X, sp.BATT_CENTER_Y, 0.4)
    batt_pack.label = "bateria_12v_4000mah"
    batt_pack.color = srgb("#1565C0")
    children.append(batt_pack)

    # 4. LM2596 DC-DC Buck Converter 12V->3.3V (21 x 43 x 4.0 mm at x=-42.0, y=30.5, z=0.4)
    buck = _centered_box(sp.BUCK_LEN_X, sp.BUCK_WID_Y, 4.0, sp.BUCK_CENTER_X, sp.BUCK_CENTER_Y, 0.4)
    buck.label = "buck_lm2596_12v_3v3"
    buck.color = srgb("#0D47A1")
    children.append(buck)

    # 5. Slide Switch (8 x 19 x 9 mm at x=+44.5, y=35.0, z=0.4)
    sw = _centered_box(8.0, 19.0, 9.0, sp.SWITCH_CENTER_X, sp.SWITCH_CENTER_Y, 0.4)
    sw.label = "interruptor_encendido"
    sw.color = srgb("#37474F")
    children.append(sw)

    # 6. Status RGB LED (at x=+53.5, y=14.0, z=10.0)
    led = (
        bd.Pos(53.5, 14.0, 10.0)
        * bd.Rot(0.0, 90.0, 0.0)
        * bd.Cylinder(radius=2.4, height=6.0)
    )
    led.label = "led_estado_rgb"
    led.color = srgb("#00E676")
    children.append(led)

    # 7. Silica Gel Desiccant Packet (18 x 40 x 8 mm at x=+39.5, y=-26.5, z=0.4)
    silica = _centered_box(18.0, 40.0, 8.0, sp.DESICCANT_CENTER_X, sp.DESICCANT_CENTER_Y, 0.4)
    silica.label = "bolsa_desecante_silice"
    silica.color = srgb("#F5F5DC")
    children.append(silica)

    return bd.Compound(children=children, label="componentes_internos")
