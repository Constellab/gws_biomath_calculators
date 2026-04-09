import os

from gws_core import BaseTestCase, File, TaskRunner

from gws_biomath_calculators.biomath_calcul.gc_content_calculator.gc_content_calculator import GCContentCalculator

TESTDATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "testdata"))
SHORT_DNA_FA = os.path.join(TESTDATA_DIR, "short_dna.fa")


class TestGCContentCalculator(BaseTestCase):

    def test_gc_content(self):
        """Short DNA sequence => HTML report with GC content."""
        outputs = TaskRunner(
            task_type=GCContentCalculator,
            inputs={"input_path": File(SHORT_DNA_FA)},
            params={"prefix": "test_gc_content"},
        ).run()

        report_html: File = outputs["report_html"]
        self.assertIsNotNone(report_html)
        self.assertTrue(os.path.exists(report_html.path))
        html_content = open(report_html.path, encoding="utf-8").read()
        self.assertIn("<html", html_content.lower())
        self.assertGreater(len(html_content), 100)
