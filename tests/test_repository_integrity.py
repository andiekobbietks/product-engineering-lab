import ast
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXP = ROOT / "experiments" / "001-nyfasi-reconstruction"


class RepositoryIntegrityTests(unittest.TestCase):
    def test_product_model_references_known_sources(self):
        model = json.loads((EXP / "models" / "product-model.json").read_text())
        sources = json.loads((EXP / "evidence" / "source-register.json").read_text())
        known_ids = {source["id"] for source in sources}
        self.assertTrue(set(model["sources"]).issubset(known_ids))
        for component in model["components"]:
            for parameter in component["parameters"]:
                self.assertTrue(set(parameter["evidence_ids"]).issubset(known_ids))

    def test_product_model_schema_is_valid_json(self):
        schema = json.loads((EXP / "models" / "product-model.schema.json").read_text())
        self.assertEqual(schema["$schema"], "https://json-schema.org/draft/2020-12/schema")

    def test_colab_notebook_is_valid_json_and_not_empty(self):
        notebook = json.loads((EXP / "notebooks" / "nyfasi_reconstruction_colab.ipynb").read_text())
        self.assertEqual(notebook["nbformat"], 4)
        self.assertGreaterEqual(len(notebook["cells"]), 4)

    def test_reconstruction_script_parses(self):
        script = (EXP / "scripts" / "build_reconstruction.py").read_text()
        ast.parse(script)

    def test_no_manufacturing_release_claim(self):
        model = json.loads((EXP / "models" / "product-model.json").read_text())
        self.assertEqual(model["model_status"], "research")


if __name__ == "__main__":
    unittest.main()
