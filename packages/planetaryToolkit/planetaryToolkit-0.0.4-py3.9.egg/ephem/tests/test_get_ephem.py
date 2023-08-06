#!/usr/bin/env python

import unittest
from planetaryToolkit.ephem import get_ephem


class TestNaif(unittest.TestCase):
    def test_lookup(
        self, test_names=["Neptune", "despina", "PUCK"], test_ids=[899, 805, 715]
    ):

        for i in range(len(test_names)):
            self.assertEqual(get_ephem.naif_lookup(test_names[i]), str(test_ids[i]))

    def test_asteroid(self):

        self.assertEqual(get_ephem.naif_lookup("BENNU"), "101955;")

    def test_comet(self):
        with self.assertRaises(NotImplementedError):
            get_ephem.naif_lookup("CHURYUMOV-GERASIMENKO")


class TestGetEphem(unittest.TestCase):
    def test_goodcase1(
        self,
        code="899",
        obscode="568",
        tstart="2021-10-08 00:00",
        tend="2021-10-09 00:00",
        stepsize="30 minutes",
        quantities="1,3,4,8,9,12,13,14,15,17,19,20",
    ):

        out, observatory_coords = get_ephem.get_ephemerides(
            code, obscode, tstart, tend, stepsize, quantities
        )

        self.assertEqual(len(observatory_coords), 3)
        self.assertEqual(out.shape, (49, 26))

    def test_goodcase2(
        self,
        code="Proteus",
        obscode="568",
        tstart="2021-10-08 00:00",
        tend="2021-10-09 00:00",
        stepsize="2 hours",
        quantities="all",
    ):

        out, observatory_coords = get_ephem.get_ephemerides(
            code, obscode, tstart, tend, stepsize, quantities
        )

        self.assertEqual(len(observatory_coords), 3)
        self.assertEqual(out.shape, (13, 89))

    def test_failcases(
        self,
        code="899",
        obscode="568",
        tstart="2021-10-08 00:00",
        tend="2021-10-09 00:00",
        stepsize="30 minutes",
        quantities="1,3,4,8,9,12,13,14,15,17,19,20",
    ):

        # bad naif
        with self.assertRaises(ValueError):
            get_ephem.get_ephemerides(
                "-999", obscode, tstart, tend, stepsize, quantities
            )

        # bad tstart
        with self.assertRaises(ValueError):
            get_ephem.get_ephemerides(
                code, obscode, "20211008 0000", tend, stepsize, quantities
            )

    def test_argparse_defaults(self):

        args = get_ephem.parse_arguments(["899", "568", "2021-10-08 00:00"])
        self.assertEqual(args.code, "899")
        self.assertEqual(args.obscode, "568")
        self.assertEqual(args.tstart, "2021-10-08 00:00")
        self.assertEqual(args.tend, "2021-10-08 00:00")
        self.assertEqual(args.stepsize, "30 minutes")
        self.assertEqual(args.quantities, "1,3,4,8,9,12,13,14,15,17,19,20")

    def test_argparse(
        self,
        code="899",
        obscode="568",
        tstart="2021-10-08 00:00",
        tend="2021-10-09 00:00",
        stepsize="30 minutes",
        quantities="1,3,4,8,9,12,13,14,15,17,19,20",
    ):
        args = get_ephem.parse_arguments(
            [code, obscode, tstart, tend, stepsize, quantities]
        )
        self.assertEqual(args.code, code)
        self.assertEqual(args.obscode, obscode)
        self.assertEqual(args.tstart, tstart)
        self.assertEqual(
            args.tend, tend
        )  # you get a list when nargs = 1, but just a string when nargs = '?'
        self.assertEqual(args.stepsize, stepsize)
        self.assertEqual(args.quantities, quantities)


if __name__ == "__main__":

    unittest.main()
