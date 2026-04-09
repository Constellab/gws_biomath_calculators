import importlib
import json
import os

from gws_core import BaseTestCase, File, TaskRunner

from gws_biomath_calculators.biomath_calcul.dna_rna_prot_molecular_weight_calc.bioseq_mw import BioSeqMW

TESTDATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "testdata"))
SHORT_DNA_FA = os.path.join(TESTDATA_DIR, "short_dna.fa")


class TestBioSeqMW(BaseTestCase):

    def test_ssdna_linear_hydroxyl(self):
        """ssDNA linear 5'-hydroxyl => JSON with MW result."""
        outputs = TaskRunner(
            task_type=BioSeqMW,
            inputs={"input_path": File(SHORT_DNA_FA)},
            params={
                "type": "DNA",
                "strand": "ss",
                "topology": "linear",
                "five_prime": "hydroxyl",
            },
        ).run()
        result_file: File = outputs["json"]
        self.assertIsNotNone(result_file)
        self.assertTrue(os.path.exists(result_file.path))

        data = json.loads(open(result_file.path, encoding="utf-8").read())
        self.assertIn("result", data)
        mw_val = data["result"].get("molecular_weight_Da")
        self.assertIsNotNone(mw_val)
        self.assertGreater(mw_val, 0)

    def test_dsdna_linear_phosphate(self):
        """dsDNA linear 5'-phosphate => JSON with MW result."""
        outputs = TaskRunner(
            task_type=BioSeqMW,
            inputs={"input_path": File(SHORT_DNA_FA)},
            params={
                "type": "DNA",
                "strand": "ds",
                "topology": "linear",
                "five_prime": "phosphate",
            },
        ).run()
        result_file: File = outputs["json"]
        data = json.loads(open(result_file.path, encoding="utf-8").read())
        self.assertIn("result", data)
        mw_val = data["result"].get("molecular_weight_Da")
        self.assertIsNotNone(mw_val)
        self.assertGreater(mw_val, 0)

    def test_ssdna_circular(self):
        """ssDNA circular => MW should differ from linear."""
        outputs_linear = TaskRunner(
            task_type=BioSeqMW,
            inputs={"input_path": File(SHORT_DNA_FA)},
            params={"type": "DNA", "strand": "ss", "topology": "linear", "five_prime": "hydroxyl"},
        ).run()
        outputs_circular = TaskRunner(
            task_type=BioSeqMW,
            inputs={"input_path": File(SHORT_DNA_FA)},
            params={"type": "DNA", "strand": "ss", "topology": "circular", "five_prime": "hydroxyl"},
        ).run()
        mw_lin = json.loads(open(outputs_linear["json"].path, encoding="utf-8").read())["result"]["molecular_weight_Da"]
        mw_cir = json.loads(open(outputs_circular["json"].path, encoding="utf-8").read())["result"]["molecular_weight_Da"]
        self.assertNotEqual(mw_lin, mw_cir)
