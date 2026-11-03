"""Geometric, topological, interference, and filament-saving checks for the `ligero` models."""

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

PRINTED_PETG_PARTS = [
    "chasis_bandeja",
    "tapa_carcasa",
    "bisel_ventana",
    "parasol_capucha",
    "marco_tarjeta",
    "soporte_base",
]


def main() -> None:
    print("=== 1. Lightweight (`ligero`) Part Checks & Filament Comparison vs Original ===")
    total_orig_vol = 0.0
    total_lig_vol = 0.0

    for name in PRINTABLE_PARTS:
        lig_path = ROOT / "STEP" / "ligero" / f"{name}.step"
        orig_path = ROOT / "STEP" / f"{name}.step"
        shape = read_step(lig_path)
        orig_shape = read_step(orig_path)

        solids = shape.solids()
        solid_count = len(solids)
        valid = shape.is_valid
        sound = is_sound(shape)
        t_errs = topology_errors(shape)
        b_edges = sum(len(boundary_edges(sh)) for s in solids for sh in s.shells())
        vol = sum(s.volume for s in solids)
        orig_vol = sum(s.volume for s in orig_shape.solids())
        bb = shape.bounding_box().size

        saving_pct = (1.0 - vol / orig_vol) * 100.0 if orig_vol > 0 else 0.0
        if name in PRINTED_PETG_PARTS:
            total_orig_vol += orig_vol
            total_lig_vol += vol

        obb = orig_shape.bounding_box().size
        d_bb = (abs(bb.X - obb.X), abs(bb.Y - obb.Y), abs(bb.Z - obb.Z))
        print(
            f"  {name:18s}: solids={solid_count}, valid={valid}, sound={sound}, "
            f"orig={orig_vol/1000.0:6.1f} cm^3 -> ligero={vol/1000.0:6.1f} cm^3 "
            f"({saving_pct:+5.1f}%), bbox=({bb.X:.1f} x {bb.Y:.1f} x {bb.Z:.1f}) mm "
            f"[orig: {obb.X:.1f} x {obb.Y:.1f} x {obb.Z:.1f}]"
        )
        assert solid_count == 1, f"{name} must be a single connected solid, got {solid_count}"
        assert valid, f"{name} failed BRepCheck"
        assert sound, f"{name} failed is_sound"
        assert len(t_errs) == 0, f"{name} has topology errors: {t_errs}"
        assert b_edges == 0, f"{name} has open boundary edges: {b_edges}"
        assert vol > 0.0, f"{name} has non-positive volume: {vol}"
        assert max(bb.X, bb.Y, bb.Z) <= 256.0, f"{name} exceeds 256 mm build plate: {bb}"

    total_saving_pct = (1.0 - total_lig_vol / total_orig_vol) * 100.0
    print(
        f"\n  TOTAL 6 PRINTED PETG PARTS: {total_orig_vol/1000.0:.1f} cm^3 -> "
        f"{total_lig_vol/1000.0:.1f} cm^3 (SAVED {total_saving_pct:.1f}% SOLID VOLUME!)"
    )

    print("\n=== 2. Lightweight Assembly Pairwise Interference Check ===")
    scene = read_scene(ROOT / "STEP" / "ligero" / "assembly.step")
    leaves = list(scene.leaves())
    print(f"  Total leaf occurrences in ligero/assembly.step: {len(leaves)}")

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

    print("\nALL LIGHTWEIGHT (`ligero`) GEOMETRIC & TOPOLOGICAL CHECKS PASSED!")


if __name__ == "__main__":
    main()
