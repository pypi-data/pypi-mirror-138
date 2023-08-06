import os
import unittest
import numpy as np
import imgio
import rawpipe


thisdir = os.path.dirname(__file__)


class RegressionTest(unittest.TestCase):

    def test_fullpipe(self):
        print("\nConfirming bit-exact output of basic ISP blocks...")
        bayer_pattern = "RGGB"
        gamma_mode = "sRGB"
        whitelevel = None
        wb = [1.7, 2.4]
        ccm = np.array([[ 0.9, 0.4, -0.3],   # noqa
                        [-0.2, 1.1,  0.1],   # noqa
                        [ 0.0,-0.4,  1.4]])  # noqa
        expected, maxval = imgio.imread(os.path.join(thisdir, "expected.ppm"))
        raw = np.fromfile(os.path.join(thisdir, "input.raw"), dtype=np.uint16)
        raw = raw.reshape(expected.shape[:2])
        self.assertEqual(raw.shape[0], expected.shape[0])
        self.assertEqual(raw.shape[1], expected.shape[1])
        alg = rawpipe.Algorithms(verbose=True)
        raw = alg.subtract(raw, [10, 20, 30, 40])
        raw = alg.subtract(raw, [246, 236, 226, 216])  # total = 256
        raw = alg.linearize(raw, 0, whitelevel).astype(np.float64)
        raw = alg.bayer_combine(*alg.bayer_split(raw))  # no-op
        raw = alg.demosaic(raw, bayer_pattern)
        raw = alg.subtract(raw, [0, 0, 0])  # no-op
        raw = alg.wb(raw, wb)
        raw = alg.ccm(raw, ccm)
        raw = alg.gamut(raw, "ACES", p=1.2)
        raw = alg.saturate(raw, lambda x: x ** 0.5)
        raw = rawpipe.verbose.gamma(raw, gamma_mode)
        raw = rawpipe.verbose.quantize(raw, maxval, expected.dtype)
        self.assertEqual(np.count_nonzero(expected - raw), 0)

    def test_bayer_wb(self):
        expected, maxval = imgio.imread(os.path.join(thisdir, "expected.ppm"))
        raw = np.fromfile(os.path.join(thisdir, "input.raw"), dtype=np.uint16)
        raw = raw.reshape(expected.shape[:2])
        raw = raw.astype(np.float32)
        wb = np.asarray([1.7, 2.4]).astype(np.float32)
        res = rawpipe.wb(raw, wb, "GBRG")
        org_b = rawpipe.bayer_split(raw)[1]
        res_b = rawpipe.bayer_split(res)[1]
        self.assertEqual(res.dtype, np.float32)
        np.testing.assert_allclose(org_b * wb[-1], res_b)

    def test_preserve_dtype(self):
        raw = np.random.random((28, 12))
        rgb = np.random.random((28, 12, 3))
        for dt in [np.float16, np.float32, np.float64]:
            raw_src = raw.astype(dt)
            rgb_src = rgb.astype(dt)
            res01 = rawpipe.clip(raw_src, 0.1, 0.9)
            res02 = rawpipe.bayer_combine(*rawpipe.bayer_split(raw_src))
            res03 = rawpipe.downsample(raw_src, 1)
            res04 = rawpipe.downsample(rgb_src, 1)
            res05 = rawpipe.resize(rgb_src, 20, 14)
            res06 = rawpipe.subtract(raw_src, blacklevels=[0.1, 0.2, 0.3, 0.4])
            res07 = rawpipe.subtract(rgb_src, blacklevels=[0.1, 0.2, 0.3])
            res08 = rawpipe.linearize(raw_src, 0.1, 0.9)
            res09 = rawpipe.linearize(rgb_src, 0.1, num_clipped=2)
            res10 = rawpipe.wb(raw_src, [1.2, 2.9], "RGGB")
            res11 = rawpipe.wb(rgb_src, [1.2, 1.3, 2.9], "GBRG")
            res12 = rawpipe.demosaic(raw_src, "RGGB")
            res13 = rawpipe.demosaic(raw_src, "RGGB", downsample=True)
            res14 = rawpipe.lsc(raw_src, raw_src[::3, ::2] * 0.5)
            res15 = rawpipe.lsc(rgb_src, rgb_src[::2, ::3] * 0.5)
            res16 = rawpipe.ccm(rgb_src, np.arange(9).reshape(3, 3))
            res17 = rawpipe.gamut(rgb_src)
            res18 = rawpipe.tonemap(rgb_src)
            res19 = rawpipe.saturate(rgb_src, lambda v: v ** 0.7)
            res20 = rawpipe.gamma(raw_src)
            res21 = rawpipe.gamma(rgb_src)
            results = [res01, res02, res03, res04, res05, res06,
                       res07, res10, res11, res12, res13, res14,
                       res15, res16, res17, res18, res19, res20,
                       res21]
            for res in results:
                self.assertEqual(res.dtype, dt)
            self.assertEqual(res08.dtype, np.float32)  # linearize()
            self.assertEqual(res09.dtype, np.float32)  # linearize()

    def test_errors(self):
        raw = np.fromfile(os.path.join(thisdir, "input.raw"), dtype=np.uint16)
        res = rawpipe.verbose.gamma(raw, None)  # should be no-op
        res = rawpipe.verbose.gamma(res, "")  # should be no-op
        res = rawpipe.verbose.gamma(res, False)  # should be no-op
        self.assertTrue(np.all(raw == res))
        with self.assertRaises(AssertionError):
            raw = rawpipe.gamma(raw, "srgb")  # expecting "sRGB"
        with self.assertRaises(AssertionError):
            raw = rawpipe.gamma(raw, True)  # does not evaluate to False
        with self.assertRaises(AssertionError):
            raw = rawpipe.demosaic(raw, "RGGB")  # raw is not in [0, 1]


if __name__ == "__main__":
    np.set_printoptions(formatter={'float': lambda x: f"{x:6.4f}"}, linewidth=180)
    unittest.main()
