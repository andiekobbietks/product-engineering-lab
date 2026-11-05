import ast
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXP = ROOT / "experiments" / "001-nyfasi-reconstruction"
DOCS = ROOT / "docs"


class Sand3DGalleryContractTests(unittest.TestCase):
    def test_build_program_publishes_ast_source_ranges_and_complete_assembly(self):
        script = (EXP / "scripts" / "build_reconstruction.py").read_text(encoding="utf-8")
        ast.parse(script)
        for contract in (
            "nyfasi_complete_assembly.glb",
            "source_symbols",
            "source_object_prefixes",
            "source_ranges",
            "component.name",
            "roller_rotation",
            "build_reconstruction.py",
            "cad-parameters.json",
        ):
            self.assertIn(contract, script)

    def test_gallery_uses_complete_assembly_and_native_joint_extras(self):
        viewer = (DOCS / "experiments" / "assembly-explorer.html").read_text(encoding="utf-8")
        for contract in (
            "manifest.assembly_file",
            "s3d_joint",
            "source_symbols",
            "jointNode.quaternion",
            "sourceSymbolForObject",
            "build_reconstruction.py",
            "No schematic or guessed-geometry fallback",
        ):
            self.assertIn(contract, viewer)
        self.assertNotIn("new THREE.CylinderGeometry(12,12,112", viewer)

    def test_architecture_decisions_are_present_and_linked(self):
        index = (DOCS / "decisions" / "index.md").read_text(encoding="utf-8")
        adr1 = (DOCS / "decisions" / "adr-0001-sand3d-canonical-engine.md").read_text(encoding="utf-8")
        adr2 = (DOCS / "decisions" / "adr-0002-sand3d-source-linked-gallery.md").read_text(encoding="utf-8")
        self.assertIn("ADR-0001", index)
        self.assertIn("Sand3D", adr1)
        self.assertIn("s3d_joint", adr2)


if __name__ == "__main__":
    unittest.main()
