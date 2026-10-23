import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from music_24h_pilot import render_frame, audio_samples, FPS, DURATION


class PilotContract(unittest.TestCase):
    def test_three_scenes_are_animated(self):
        for a, b in ((0.5, 1.1), (5.7, 6.5), (10.0, 10.8)):
            x = render_frame(a, 270, 480)
            y = render_frame(b, 270, 480)
            self.assertEqual(x.size, (270, 480))
            self.assertNotEqual(x.tobytes(), y.tobytes())

    def test_music_cut_has_no_beat_tail(self):
        before = audio_samples(2.4, 0.2)
        after = audio_samples(4.0, 0.2)
        self.assertGreater(before.std(), after.std() * 8)

    def test_fixed_timeline(self):
        self.assertEqual((FPS, DURATION), (30, 15))


if __name__ == '__main__':
    unittest.main()
