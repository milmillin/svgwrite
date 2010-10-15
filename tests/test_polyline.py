#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: test polyline object
# Created: 25.09.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3

import sys
import unittest

from svgwrite import Polyline, parameter

class TestPolyline(unittest.TestCase):
    def setUp(self):
        parameter.set_debug(True)

    def test_numbers(self):
        polyline = Polyline(points=[(0,0), (1,1)])
        self.assertEqual(polyline.tostring(), '<polyline points="0,0 1,1" />')

    def test_coordinates(self):
        # list of points is a list of numbers not coordinates -> no units allowed!!
        self.assertRaises(TypeError, Polyline, [('1cm','1cm'), ('2mm', '1mm')])

    def test_errors(self):
        self.assertRaises(TypeError, Polyline, 0)
        self.assertRaises(TypeError, Polyline, None)
        self.assertRaises(TypeError, Polyline, [(None, None)])

class TestPointsToStringFullProfile(unittest.TestCase):
    def setUp(self):
        parameter.set_debug(True)
        parameter.set_profile('full')
        self.polyline = Polyline()

    def test_valid_points(self):
        # valid units: cm|em|ex|in|mm|pc|pt|px|%
        # dont't know if '%' is valid for points?
        result = self.polyline.points_to_string([(10,10), ('20cm', '20em'), ('30ex', '30in'), ('40mm', '40pc'), ('50pt', '50px'), ('60%', '60%')])
        # it's an unicode string
        self.assertTrue(isinstance(result, unicode))
        self.assertEqual(result, u"10,10 20cm,20em 30ex,30in 40mm,40pc 50pt,50px 60%,60%")
        # e-notation is valid
        result = self.polyline.points_to_string([('1e10pt','1e-10in')])
        self.assertEqual(result, u"1e10pt,1e-10in")

    def test_invalid_points(self):
        # invalid unit #'p'
        self.assertRaises(TypeError, self.polyline.points_to_string, [(10,10), ('20p', '20px')])

    def test_invalid_tuple_count(self):
        # 3-tuple not allowed
        self.assertRaises(TypeError, self.polyline.points_to_string, [(10,10), ('20px', '20px', '20px')])
        # 1-tuple not allowed
        self.assertRaises(TypeError, self.polyline.points_to_string, [(10,10), ('20px', )])

class TestPointsToStringTinyProfile(unittest.TestCase):
    def setUp(self):
        parameter.set_debug(True)
        parameter.set_profile('tiny')
        self.polyline = Polyline()

    def test_valid_points(self):
        # valid units: cm|em|ex|in|mm|pc|pt|px|%
        # dont't know if '%' is valid for points?
        result = self.polyline.points_to_string([(10,10), ('20cm', '20em'), ('30ex', '30in'), ('40mm', '40pc'), ('50pt', '50px'), ('60%', '60%')])
        # it's an unicode string
        self.assertTrue(isinstance(result, unicode))
        self.assertEqual(result, u"10,10 20cm,20em 30ex,30in 40mm,40pc 50pt,50px 60%,60%")

    def test_value_range(self):
        # invalid unit #'p'
        self.assertRaises(TypeError, self.polyline.points_to_string, [(100000,10)])
        self.assertRaises(TypeError, self.polyline.points_to_string, [(-100000,10)])
        self.assertRaises(TypeError, self.polyline.points_to_string, [(10,100000)])
        self.assertRaises(TypeError, self.polyline.points_to_string, [(-10,-100000)])

if __name__=='__main__':
    unittest.main()