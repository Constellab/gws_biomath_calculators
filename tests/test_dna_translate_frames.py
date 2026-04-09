import os

from gws_core import BaseTestCase, File, ResourceSet, TaskRunner

from gws_biomath_calculators.biomath_calcul.dna_translation.dna_translate_frames import DNATranslateFramesORF

TESTDATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "testdata"))
SHORT_DNA_FA = os.path.join(TESTDATA_DIR, "short_dna.fa")


class TestDNATranslateFramesORF(BaseTestCase):

    def test_translation(self):
        """Short DNA => text report + 3 per-frame ORF tables."""
        outputs = TaskRunner(
            task_type=DNATranslateFramesORF,
            inputs={"input_path": File(SHORT_DNA_FA)},
            params={"prefix": "test_translate"},
        ).run()

        report: File = outputs["report"]
        orf_tables: ResourceSet = outputs["orf_tables"]

        self.assertIsNotNone(report)
        self.assertTrue(os.path.exists(report.path))
        content = open(report.path, encoding="utf-8").read()
        self.assertGreater(len(content), 0)

        self.assertIsNotNone(orf_tables)
        self.assertGreaterEqual(len(orf_tables.get_resources()), 1)
