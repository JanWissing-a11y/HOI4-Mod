from pathlib import Path
import tempfile
import unittest
from zipfile import ZipFile

from tools.package_mod import package


ROOT = Path(__file__).resolve().parents[1]


class PackageTests(unittest.TestCase):
    def test_reproducible_runtime_package_excludes_local_data(self):
        with tempfile.TemporaryDirectory() as temporary:
            first = Path(temporary) / 'first.zip'
            second = Path(temporary) / 'second.zip'
            package(ROOT, first)
            package(ROOT, second)
            self.assertEqual(first.read_bytes(), second.read_bytes())
            with ZipFile(first) as archive:
                names = set(archive.namelist())
            self.assertTrue({'descriptor.mod', 'tools/install.ps1', 'tools/data/building_overrides.json',
                             'history/states/1082-Wesel-Flueren.txt', 'gfx/flags/WFL.tga',
                             'portraits/WFL_portraits.txt'} <= names)
            self.assertNotIn('map/buildings.txt', names)
            self.assertFalse(any(name.startswith(('.git/', '.local-test/', 'dist/')) for name in names))


if __name__ == '__main__':
    unittest.main()
