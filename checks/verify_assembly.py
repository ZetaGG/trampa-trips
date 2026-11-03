"""Geometric, topological, and interference checks for the Trampa de Trips CAD models (Option A)."""

from __future__ import annotations

from itertools import combinations
from pathlib import Path

from cadgen import read_scene, read_step
from cadgen.geometry import boundary_edges, is_sound, overlap_volume, topology_errors

ROOT = Path(__file__).resolve().parent.parent

PRINTABLE_PARTS = [
    "chasis_bandeja",
    "tapa_carcasa",
    "ventana_pc",
    "bisel_ventana",
    "parasol_capucha",
    "marco_tarjeta",
    "tarjeta_azul",
    "soporte_base",
]


def main() -> None:
    print("=== 1. Individual Printable Part Checks ===")
    for name in PRINTABLE_PARTS:
        step_path = ROOT / "STEP" / f"{name}.step"
        shape = read_step(step_path)
        solids = shape.solids()
        solid_count = len(solids)
        valid = shape.is_valid
        sound = is_sound(shape)
        t_errs = topology_errors(shape)
        b_edges = sum(len(boundary_edges(sh)) for s in solids for sh in s.shells())
        vol = sum(s.volume for s in solids)
        bb = shape.bounding_box().size
        print(
            f"  {name:18s}: solids={solid_count}, valid={valid}, sound={sound}, "
            f"topo_errs={len(t_errs)}, free_edges={b_edges}, vol={vol:,.1f} mm^3, "
            f"bbox=({bb.X:.1f} x {bb.Y:.1f} x {bb.Z:.1f}) mm"
        )
        assert solid_count == 1, f"{name} must be a single connected solid, got {solid_count}"
        assert valid, f"{name} failed BRepCheck"
        assert sound, f"{name} failed is_sound"
        assert len(t_errs) == 0, f"{name} has topology errors: {t_errs}"
        assert b_edges == 0, f"{name} has open boundary edges: {b_edges}"
        assert vol > 0.0, f"{name} has non-positive volume: {vol}"
        assert max(bb.X, bb.Y, bb.Z) <= 256.0, f"{name} exceeds 256 mm build plate: {bb}"

    print("\n=== 2. Assembly Pairwise Interference Check ===")
    scene = read_scene(ROOT / "STEP" / "assembly.step")
    leaves = list(scene.leaves())
    print(f"  Total leaf occurrences in assembly.step: {len(leaves)}")

    bodies = []
    for leaf in leaves:
        sh = leaf.shape()
        for idx, s in enumerate(sh.solids()):
            bodies.append((f"{leaf.label}({leaf.ref})[{idx}]", s))

    max_overlap_mm3 = 0.01
    failures = []
    tested = 0
    for (ref_a, sa), (ref_b, sb) in combinations(bodies, 2):
        bba = sa.bounding_box(optimal=False)
        bbb = sb.bounding_box(optimal=False)
        if (
            bba.max.X < bbb.min.X or bbb.max.X < bba.min.X
            or bba.max.Y < bbb.min.Y or bbb.max.Y < bba.min.Y
            or bba.max.Z < bbb.min.Z or bbb.max.Z < bba.min.Z
        ):
            tested += 1
            continue
        ov = overlap_volume(sa, sb)
        tested += 1
        if ov > max_overlap_mm3:
            failures.append((ref_a, ref_b, ov))

    print(f"  Tested pairs: {tested}, interference failures (> {max_overlap_mm3} mm^3): {len(failures)}")
    for ra, rb, ov in failures:
        print(f"    OVERLAP: {ra} <-> {rb}: {ov:.3f} mm^3")
    assert len(failures) == 0, f"Found {len(failures)} interfering body pairs!"

    print("\n=== 3. Functional Dimension & Alignment Checks ===")
    card_sel = scene.resolve("#tarjeta_azul").shape()
    card_bb = card_sel.bounding_box()
    win_sel = scene.resolve("#ventana_pc").shape()
    win_bb = win_sel.bounding_box()
    esp_sel = scene.resolve("#esp32_s3_pcb").shape()
    esp_bb = esp_sel.bounding_box()
    batt_sel = scene.resolve("#bateria_12v_4000mah").shape()
    batt_bb = batt_sel.bounding_box()
    buck_sel = scene.resolve("#buck_70x30x20").shape()
    buck_bb = buck_sel.bounding_box()
    base_sel = scene.resolve("#soporte_base").shape()
    base_bb = base_sel.bounding_box()

    optical_dist_mm = card_bb.min.Y - win_bb.max.Y
    print(f"  Tarjeta azul size: {card_bb.size.X:.2f} x {card_bb.size.Z:.2f} x {card_bb.size.Y:.2f} mm")
    print(f"  ESP32-S3 PCB size (X x Y x Z): {esp_bb.size.X:.2f} x {esp_bb.size.Y:.2f} x {esp_bb.size.Z:.2f} mm")
    print(f"  Bateria 12V 4000mAh size (X x Y x Z): {batt_bb.size.X:.2f} x {batt_bb.size.Y:.2f} x {batt_bb.size.Z:.2f} mm")
    print(f"  Buck 70x30x20 size (X x Y x Z): {buck_bb.size.X:.2f} x {buck_bb.size.Y:.2f} x {buck_bb.size.Z:.2f} mm")
    print(f"  Clear optical distance (window front to sticky card face): {optical_dist_mm:.2f} mm")
    print(f"  Table stand bottom Z datum: {base_bb.min.Z:.3f} mm")

    assert abs(card_bb.size.X - 100.0) < 0.05
    assert abs(card_bb.size.Z - 250.0) < 0.05
    assert abs(esp_bb.size.X - 28.0) < 0.05
    assert abs(esp_bb.size.Y - 58.0) < 0.05
    assert abs(batt_bb.size.X - 70.0) < 0.05
    assert abs(batt_bb.size.Y - 60.0) < 0.05
    assert abs(batt_bb.size.Z - 20.0) < 0.05
    assert abs(buck_bb.size.X - 70.0) < 0.05
    assert abs(buck_bb.size.Y - 30.0) < 0.05
    assert abs(buck_bb.size.Z - 20.0) < 0.05
    assert 115.0 <= optical_dist_mm <= 155.0
    assert abs(base_bb.min.Z - 0.0) < 0.01

    print("\nALL GEOMETRIC & TOPOLOGICAL CHECKS PASSED!")


if __name__ == "__main__":
    main()
