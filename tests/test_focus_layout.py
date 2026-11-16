"""Keep the continuous-focus panel clear of the complete ordinary focus tree."""
from pathlib import Path
import unittest

from tools.render_focus_layout import layout, ITEM, GRID_ORIGIN

ROOT = Path(__file__).resolve().parents[1]


class FocusLayoutTests(unittest.TestCase):
    def test_continuous_panel_is_below_all_focuses_and_their_connections(self):
        data = layout(ROOT)
        panel = data['panel']
        self.assertEqual((panel['width'], panel['height']), (770, 380))
        self.assertEqual(panel['x'] + GRID_ORIGIN[0], min(f['px'] for f in data['focuses']))
        bottom = max(f['py'] + ITEM[1] for f in data['focuses'])
        self.assertGreaterEqual(panel['y'] - bottom, 300)
        # All prerequisite links have both endpoints in the normal-tree area;
        # the panel is below its entire bounding box, not merely between nodes.
        by_id = {f['id']: f for f in data['focuses']}
        for f in data['focuses']:
            for parent in f['parents']:
                self.assertLess(by_id[parent]['y'], f['y'])
                self.assertLess(f['py'] + ITEM[1], panel['y'])

    def test_normal_focus_boxes_do_not_overlap_and_use_nonnegative_columns(self):
        focuses = layout(ROOT)['focuses']
        self.assertEqual(len(focuses), 78)
        self.assertTrue(all(f['x'] >= 0 for f in focuses))
        for index, first in enumerate(focuses):
            for second in focuses[index + 1:]:
                self.assertTrue(abs(first['px'] - second['px']) >= ITEM[0] + 16
                                or abs(first['py'] - second['py']) >= ITEM[1],
                                (first['id'], second['id']))

    def test_staff_inlay_does_not_cover_focuses_or_the_continuous_panel(self):
        data = layout(ROOT)
        self.assertTrue(data['inlays'])

        def separate(first, second):
            x, y, width, height = first
            other_x, other_y, other_width, other_height = second
            return (x + width <= other_x or other_x + other_width <= x
                    or y + height <= other_y or other_y + other_height <= y)

        panel = data['panel']
        panel_box = tuple(panel[key] for key in ('x', 'y', 'width', 'height'))
        for inlay in data['inlays']:
            inlay_box = tuple(inlay[key] for key in ('x', 'y', 'width', 'height'))
            self.assertTrue(separate(inlay_box, panel_box), 'Inlay overlaps continuous panel')
            for focus in data['focuses']:
                focus_box = (focus['px'], focus['py'], *ITEM)
                self.assertTrue(separate(inlay_box, focus_box), focus['id'])


if __name__ == '__main__':
    unittest.main()
