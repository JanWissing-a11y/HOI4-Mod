"""Catch broken links between the staff inlay, its GUI and dynamic content.

Each case mutates an isolated project copy. These checks exercise the project
validator, not Clausewitz rendering or the staff's gameplay interpreter.
"""
from pathlib import Path
import shutil
import tempfile
import unittest

from tools.validate_mod import children, field, parse, validate, walk


ROOT = Path(__file__).resolve().parents[1]
GUI = 'interface/WFL_beraterstab.gui'
INLAY = 'common/focus_inlay_windows/WFL_beraterstab.txt'


def zoom_layout_problems(text):
    """Check the no-scissor workaround and the bounds that make it safe.

    Vanilla's zoomed focus inlays explicitly disable container clipping. With
    that workaround children must fit their parent without relying on a crop.
    This is a source-level guard, not an emulation of the engine's renderer.
    """
    problems = []
    nodes = parse(text)

    def dimensions(node, key, width_key, height_key):
        block = next((n for n in children(node) if n.key == key), None)
        if block is None:
            return None
        return float(field(block, width_key) or 0), float(field(block, height_key) or 0)

    def inspect(container):
        name = field(container, 'name')
        if field(container, 'clipping') != 'no':
            problems.append(f'{name}: zoom clipping must be disabled')
        size = dimensions(container, 'size', 'width', 'height')
        if size is None:
            problems.append(f'{name}: missing explicit container bounds')
            return
        for child in children(container):
            if child.key == 'containerWindowType':
                extent = dimensions(child, 'size', 'width', 'height')
                inspect(child)
            elif child.key == 'instantTextBoxType':
                extent = (float(field(child, 'maxWidth') or 0),
                          float(field(child, 'maxHeight') or 0))
            else:
                continue
            position = dimensions(child, 'position', 'x', 'y') or (0, 0)
            if extent and (min(position) < 0 or position[0] + extent[0] > size[0]
                           or position[1] + extent[1] > size[1]):
                problems.append(f'{field(child, "name")}: outside parent {name}')

    roots = [node for node in walk(nodes) if node.key == 'guiTypes']
    for root in roots:
        for container in children(root):
            if container.key == 'containerWindowType':
                inspect(container)
    return problems


class FocusInlayZoomTests(unittest.TestCase):
    def test_zoomed_inlay_does_not_use_clipping_and_content_fits(self):
        self.assertEqual(zoom_layout_problems((ROOT / GUI).read_text(encoding='utf-8-sig')), [])

    def test_guard_catches_root_and_nested_clipping_regressions(self):
        text = (ROOT / GUI).read_text(encoding='utf-8-sig')
        for name in ('WFL_beraterstab_window', 'WFL_staff_slot_1_card',
                     'WFL_staff_till_hoehne_card'):
            with self.subTest(container=name):
                start = text.index(f'name = "{name}"')
                clipping = text.index('clipping = no', start)
                broken = text[:clipping] + text[clipping:].replace('clipping = no', 'clipping = yes', 1)
                self.assertIn(f'{name}: zoom clipping must be disabled', zoom_layout_problems(broken))

    def test_guard_catches_content_that_relies_on_parent_cropping(self):
        text = (ROOT / GUI).read_text(encoding='utf-8-sig')
        start = text.index('name = "WFL_staff_slot_1_card"')
        position = text.index('position = ', start)
        end = text.index('}', position) + 1
        broken = text[:position] + 'position = { x = 1000 y = 107 }' + text[end:]
        self.assertTrue(any('WFL_staff_slot_1_card: outside parent' in problem
                            for problem in zoom_layout_problems(broken)))


class FocusInlayValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        temporary = tempfile.TemporaryDirectory()
        cls.addClassCleanup(temporary.cleanup)
        cls.root = Path(temporary.name) / 'mod'
        shutil.copytree(
            ROOT, cls.root,
            ignore=shutil.ignore_patterns('.git', '__pycache__', '.local-test', 'dist'),
        )
        # Establish that the diagnostics below are caused by our mutations.
        baseline = validate(cls.root).errors
        if baseline:
            raise AssertionError(f'Invalid unmodified inlay fixture: {baseline}')

    def setUp(self):
        self.saved = {}
        self.addCleanup(self.restore)

    def restore(self):
        for relative, content in self.saved.items():
            (self.root / relative).write_bytes(content)

    def replace(self, relative, before, after):
        path = self.root / relative
        self.saved.setdefault(relative, path.read_bytes())
        content = path.read_text(encoding='utf-8-sig')
        self.assertIn(before, content)
        path.write_text(content.replace(before, after, 1), encoding='utf-8')

    def assert_problems(self, *messages):
        errors = validate(self.root).errors
        for message in messages:
            self.assertTrue(any(message in error for error in errors), (message, errors))

    def test_gui_syntax_is_validated(self):
        self.replace(GUI, 'guiTypes = {', 'guiTypes = { containerWindowType = {')
        self.assert_problems(f'{GUI}: unclosed block')

    def test_focus_inlay_and_gui_window_bindings_must_resolve(self):
        # Inject a mistyped focus-tree binding without depending on its position.
        self.replace(
            'common/national_focus/WFL_focus.txt', 'id = WFL_focus_tree',
            'id = WFL_focus_tree\n'
            '    inlay_window = { id = WFL_missing_inlay position = { x = 4500 y = 1000 } }',
        )
        self.replace(INLAY, 'window_name = WFL_beraterstab_window',
                     'window_name = WFL_missing_window')
        self.assert_problems('unknown focus inlay: WFL_missing_inlay',
                             'inlay has unknown GUI window: WFL_beraterstab_inlay')

    def test_dynamic_portrait_must_target_an_existing_gui_component(self):
        self.replace(INLAY, 'WFL_staff_slot_1_portrait = {',
                     'WFL_staff_missing_portrait = {')
        self.assert_problems('inlay has unknown GUI component: WFL_staff_missing_portrait')

    def test_dynamic_gui_text_must_resolve_to_scripted_localisation(self):
        self.replace(GUI, '[WFLStaffSlot1Name]', '[WFLStaffMissingName]')
        self.assert_problems('unknown scripted UI text: WFLStaffMissingName')

    def test_static_and_dynamic_own_sprites_must_be_registered(self):
        self.replace(GUI, 'spriteType = "GFX_WFL_staff_empty"',
                     'spriteType = "GFX_WFL_missing_static"')
        self.replace(INLAY, 'GFX_WFL_staff_dante_grossy = {',
                     'GFX_WFL_missing_dynamic = {')
        self.assert_problems('unknown GUI sprite: GFX_WFL_missing_static',
                             'unknown inlay sprite: GFX_WFL_missing_dynamic')


if __name__ == '__main__':
    unittest.main()
