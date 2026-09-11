import tempfile
import unittest
from pathlib import Path

import importlib.util

MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "scraper" / "scraper.py"
spec = importlib.util.spec_from_file_location("scraper_module", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
assert spec is not None and spec.loader is not None
spec.loader.exec_module(module)

class ResolverRutaSalidaTests(unittest.TestCase):
    def test_reuses_project_root_when_running_from_repo_root(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "reflexiones_escalante_2026"
            root.mkdir()
            (root / "package.json").write_text("{}", encoding="utf-8")
            (root / "content").mkdir()

            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(root)
                result = module.resolver_ruta_salida(Path("reflexiones_escalante_2026"))
                self.assertEqual(result, root)
            finally:
                os.chdir(original_cwd)

    def test_does_not_reuse_random_folder_with_same_name(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(root)
                result = module.resolver_ruta_salida(Path("reflexiones_escalante_2026"))
                self.assertEqual(result, (root / "reflexiones_escalante_2026").resolve())
            finally:
                os.chdir(original_cwd)


if __name__ == "__main__":
    unittest.main()
