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
            "validate_articulated_glb",
            "source_ranges",
            "component.name",
            "roller_rotation",
            "roller_end_features_component_group",
            "superellipse",
            "tooth_tip_taper_deg",
            "rx=180",
            "housing_outline_profile",
            "upper_retaining_arms",
            'f"upper_retaining_arm_{side}"',
            "upper_housing_complete",
            "retaining_arms",
            "roller_projection_count",
            "tooth_node_records",
            "rotation[0]",
            'P["tooth_root_z"]',
            "roller_projection_height",
            "s3d.dome",
            "assembly_sha256",
            "build_reconstruction.py",
            "cad-parameters.json",
        ):
            self.assertIn(contract, script)
        # The Python source must contain one escaped newline in its string literal,
        # so the generated JSON ends with a real line-feed, not the two characters \ and n.
        self.assertIn(StringManifestWriter, script)
        self.assertNotIn(StringDoubleEscapedManifestWriter, script)

    def test_gallery_uses_complete_assembly_and_native_joint_extras(self):
        viewer = (DOCS / "experiments" / "assembly-explorer.html").read_text(encoding="utf-8")
        for contract in (
            "manifest.assembly_file",
            "manifest.assembly_sha256",
            "encodeURIComponent(manifest.assembly_sha256",
            "s3d_joint",
            "source_symbols",
            "jointNode.quaternion",
            "sourceSymbolForObject",
            "highlightPython",
            "build_reconstruction.py",
            "No schematic or guessed-geometry fallback",
        ):
            self.assertIn(contract, viewer)
        self.assertNotIn("new THREE.CylinderGeometry(12,12,112", viewer)
        builder = (EXP / "scripts" / "build_reconstruction.py").read_text(encoding="utf-8")
        self.assertNotIn("s3d.knurl", builder)
        self.assertNotIn("roller_core_d", builder)

    def test_architecture_decisions_are_present_and_linked(self):
        index = (DOCS / "decisions" / "index.md").read_text(encoding="utf-8")
        adr1 = (DOCS / "decisions" / "adr-0001-sand3d-canonical-engine.md").read_text(encoding="utf-8")
        adr2 = (DOCS / "decisions" / "adr-0002-sand3d-source-linked-gallery.md").read_text(encoding="utf-8")
        self.assertIn("ADR-0001", index)
        self.assertIn("Sand3D", adr1)
        self.assertIn("s3d_joint", adr2)


# Exact source-text contracts for the JSON writer.
StringManifestWriter = r'json.dumps(manifest, indent=2) + "\n"'
StringDoubleEscapedManifestWriter = r'json.dumps(manifest, indent=2) + "\\n"'


if __name__ == "__main__":
    unittest.main()
