# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2012 Smile (<http://www.smile.fr>). All Rights Reserved
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from datetime import datetime

from openerp.tests.common import TransactionCase

from ..depreciation_board import DepreciationBoard


LINEAR_METHOD = {
    "name": "Linear",
    "base_value": "purchase_value",
    "use_salvage_value": True,
    "start_date": "in_service_date",
    "use_manual_rate": False,
    "rate_formula": "100.0 / length",
    "prorata": True,
    "need_additional_annuity": True,
}
DEGRESSIVE_METHOD = {
    "name": "Degressive",
    "base_value": "book_value",
    "use_salvage_value": False,
    "start_date": "first_day_of_purchase_month",
    "use_manual_rate": True,
    "rate_formula": "max(rate, 100.0 / (length - annuity_number + 1))",
    "prorata": True,
    "need_additional_annuity": False,
}


class DepreciationBoardTestCase(TransactionCase):

    def _test_depreciation_board(self, kwargs, result):
        board = DepreciationBoard(**kwargs)
        lines = [line.__dict__ for line in board.compute()]
        self.assertEqual(lines, result)

    def test_linear_depr_starts_on_1st_day(self):
        kwargs = {'purchase_value': 5000.0, 'method_info': LINEAR_METHOD, 'annuities': 5, 'depreciation_start_date': '2012-01-01'}
        result = [
            {'book_value_wo_exceptional': 4000.0, 'depreciation_date': datetime(2012, 12, 31, 0, 0), 'depreciation_value': 1000.0,
             'accumulated_value': 1000.0, 'exceptional_value': 0.0, 'base_value': 5000.0, 'readonly': False, 'book_value': 4000.0,
             'previous_years_accumulated_value': 0.0, 'current_year_accumulated_value': 1000.0},
            {'book_value_wo_exceptional': 3000.0, 'depreciation_date': datetime(2013, 12, 31, 0, 0), 'depreciation_value': 1000.0,
             'accumulated_value': 2000.0, 'exceptional_value': 0.0, 'base_value': 5000.0, 'readonly': False, 'book_value': 3000.0,
             'previous_years_accumulated_value': 1000.0, 'current_year_accumulated_value': 1000.0},
            {'book_value_wo_exceptional': 2000.0, 'depreciation_date': datetime(2014, 12, 31, 0, 0), 'depreciation_value': 1000.0,
             'accumulated_value': 3000.0, 'exceptional_value': 0.0, 'base_value': 5000.0, 'readonly': False, 'book_value': 2000.0,
             'previous_years_accumulated_value': 2000.0, 'current_year_accumulated_value': 1000.0},
            {'book_value_wo_exceptional': 1000.0, 'depreciation_date': datetime(2015, 12, 31, 0, 0), 'depreciation_value': 1000.0,
             'accumulated_value': 4000.0, 'exceptional_value': 0.0, 'base_value': 5000.0, 'readonly': False, 'book_value': 1000.0,
             'previous_years_accumulated_value': 3000.0, 'current_year_accumulated_value': 1000.0},
            {'book_value_wo_exceptional': 0.0, 'depreciation_date': datetime(2016, 12, 31, 0, 0), 'depreciation_value': 1000.0,
             'accumulated_value': 5000.0, 'exceptional_value': 0.0, 'base_value': 5000.0, 'readonly': False, 'book_value': 0.0,
             'previous_years_accumulated_value': 4000.0, 'current_year_accumulated_value': 1000.0},
        ]
        self._test_depreciation_board(kwargs, result)

    def test_linear_depr_doesnt_start_on_1st_day(self):
        kwargs = {'purchase_value': 5000.0, 'method_info': LINEAR_METHOD, 'annuities': 5, 'depreciation_start_date': '2012-07-01'}
        result = [
            {'book_value_wo_exceptional': 4500.0, 'depreciation_date': datetime(2012, 12, 31, 0, 0), 'depreciation_value': 500.0,
             'accumulated_value': 500.0, 'exceptional_value': 0.0, 'base_value': 5000.0, 'readonly': False, 'book_value': 4500.0,
             'previous_years_accumulated_value': 0.0, 'current_year_accumulated_value': 500.0},
            {'book_value_wo_exceptional': 3500.0, 'depreciation_date': datetime(2013, 12, 31, 0, 0), 'depreciation_value': 1000.0,
             'accumulated_value': 1500.0, 'exceptional_value': 0.0, 'base_value': 5000.0, 'readonly': False, 'book_value': 3500.0,
             'previous_years_accumulated_value': 500.0, 'current_year_accumulated_value': 1000.0},
            {'book_value_wo_exceptional': 2500.0, 'depreciation_date': datetime(2014, 12, 31, 0, 0), 'depreciation_value': 1000.0,
             'accumulated_value': 2500.0, 'exceptional_value': 0.0, 'base_value': 5000.0, 'readonly': False, 'book_value': 2500.0,
             'previous_years_accumulated_value': 1500.0, 'current_year_accumulated_value': 1000.0},
            {'book_value_wo_exceptional': 1500.0, 'depreciation_date': datetime(2015, 12, 31, 0, 0), 'depreciation_value': 1000.0,
             'accumulated_value': 3500.0, 'exceptional_value': 0.0, 'base_value': 5000.0, 'readonly': False, 'book_value': 1500.0,
             'previous_years_accumulated_value': 2500.0, 'current_year_accumulated_value': 1000.0},
            {'book_value_wo_exceptional': 500.0, 'depreciation_date': datetime(2016, 12, 31, 0, 0), 'depreciation_value': 1000.0,
             'accumulated_value': 4500.0, 'exceptional_value': 0.0, 'base_value': 5000.0, 'readonly': False, 'book_value': 500.0,
             'previous_years_accumulated_value': 3500.0, 'current_year_accumulated_value': 1000.0},
            {'book_value_wo_exceptional': 0.0, 'depreciation_date': datetime(2017, 12, 31, 0, 0), 'depreciation_value': 500.0,
             'accumulated_value': 5000.0, 'exceptional_value': 0.0, 'base_value': 5000.0, 'readonly': False, 'book_value': 0.0,
             'previous_years_accumulated_value': 4500.0, 'current_year_accumulated_value': 500.0},
        ]
        self._test_depreciation_board(kwargs, result)

    def test_degressive_depr(self):
        kwargs = {'purchase_value': 5000.0, 'method_info': DEGRESSIVE_METHOD, 'annuities': 5, 'rate': 35.0, 'depreciation_start_date': '2012-07-01'}
        result = [
            {'book_value_wo_exceptional': 4125.0, 'depreciation_date': datetime(2012, 12, 31, 0, 0), 'depreciation_value': 875.0,
             'accumulated_value': 875.0, 'exceptional_value': 0.0, 'base_value': 5000.0, 'readonly': False, 'book_value': 4125.0,
             'previous_years_accumulated_value': 0.0, 'current_year_accumulated_value': 875.0},
            {'book_value_wo_exceptional': 2681.25, 'depreciation_date': datetime(2013, 12, 31, 0, 0), 'depreciation_value': 1443.75,
             'accumulated_value': 2318.75, 'exceptional_value': 0.0, 'base_value': 4125.0, 'readonly': False, 'book_value': 2681.25,
             'previous_years_accumulated_value': 875.0, 'current_year_accumulated_value': 1443.75},
            {'book_value_wo_exceptional': 1742.81, 'depreciation_date': datetime(2014, 12, 31, 0, 0), 'depreciation_value': 938.44,
             'accumulated_value': 3257.19, 'exceptional_value': 0.0, 'base_value': 2681.25, 'readonly': False, 'book_value': 1742.81,
             'previous_years_accumulated_value': 2318.75, 'current_year_accumulated_value': 938.44},
            {'book_value_wo_exceptional': 871.4, 'depreciation_date': datetime(2015, 12, 31, 0, 0), 'depreciation_value': 871.41,
             'accumulated_value': 4128.6, 'exceptional_value': 0.0, 'base_value': 1742.81, 'readonly': False, 'book_value': 871.4,
             'previous_years_accumulated_value': 3257.19, 'current_year_accumulated_value': 871.41},
            {'book_value_wo_exceptional': 0.0, 'depreciation_date': datetime(2016, 12, 31, 0, 0), 'depreciation_value': 871.4,
             'accumulated_value': 5000.0, 'exceptional_value': 0.0, 'base_value': 871.4, 'readonly': False, 'book_value': 0.0,
             'previous_years_accumulated_value': 4128.6, 'current_year_accumulated_value': 871.4},
        ]
        self._test_depreciation_board(kwargs, result)

    def test_linear_depr_with_exceptional(self):
        kwargs = {'purchase_value': 5000.0, 'method_info': LINEAR_METHOD, 'annuities': 5, 'depreciation_start_date': '2012-07-01',
                  'exceptional_values': {'2013-05': 500.0}}
        result = [
            {'book_value_wo_exceptional': 4500.0, 'depreciation_date': datetime(2012, 12, 31, 0, 0), 'depreciation_value': 500.0,
             'accumulated_value': 500.0, 'exceptional_value': 0.0, 'base_value': 5000.0, 'readonly': False, 'book_value': 4500.0,
             'previous_years_accumulated_value': 0.0, 'current_year_accumulated_value': 500.0},
            {'book_value_wo_exceptional': 3500.0, 'depreciation_date': datetime(2013, 12, 31, 0, 0), 'depreciation_value': 1000.0,
             'accumulated_value': 1500.0, 'exceptional_value': 500.0, 'base_value': 5000.0, 'readonly': False, 'book_value': 3000.0,
             'previous_years_accumulated_value': 500.0, 'current_year_accumulated_value': 1500.0},
            {'book_value_wo_exceptional': 2500.0, 'depreciation_date': datetime(2014, 12, 31, 0, 0), 'depreciation_value': 1000.0,
             'accumulated_value': 2500.0, 'exceptional_value': 0.0, 'base_value': 3000.0, 'readonly': False, 'book_value': 2000.0,
             'previous_years_accumulated_value': 2000.0, 'current_year_accumulated_value': 1000.0},
            {'book_value_wo_exceptional': 1500.0, 'depreciation_date': datetime(2015, 12, 31, 0, 0), 'depreciation_value': 1000.0,
             'accumulated_value': 3500.0, 'exceptional_value': 0.0, 'base_value': 3000.0, 'readonly': False, 'book_value': 1000.0,
             'previous_years_accumulated_value': 3000.0, 'current_year_accumulated_value': 1000.0},
            {'book_value_wo_exceptional': 500.0, 'depreciation_date': datetime(2016, 12, 31, 0, 0), 'depreciation_value': 1000.0,
             'accumulated_value': 4500.0, 'exceptional_value': 0.0, 'base_value': 3000.0, 'readonly': False, 'book_value': 0.0,
             'previous_years_accumulated_value': 4000.0, 'current_year_accumulated_value': 1000.0},
        ]
        self._test_depreciation_board(kwargs, result)

    def test_linear_depr_with_readonly(self):
        kwargs = {'purchase_value': 5000.0, 'method_info': LINEAR_METHOD, 'annuities': 5, 'depreciation_start_date': '2012-07-01',
                  'readonly_values': {'2012-12': {'depreciation_value': 500.0, 'base_value': 5000.0},
                                      '2013-12': {'depreciation_value': 1000.0, 'base_value': 5000.0}}}
        result = [
            {'book_value_wo_exceptional': 4500.0, 'depreciation_date': datetime(2012, 12, 31, 0, 0), 'depreciation_value': 500.0,
             'accumulated_value': 500.0, 'exceptional_value': 0.0, 'base_value': 5000.0, 'readonly': True, 'book_value': 4500.0,
             'previous_years_accumulated_value': 0.0, 'current_year_accumulated_value': 500.0},
            {'book_value_wo_exceptional': 3500.0, 'depreciation_date': datetime(2013, 12, 31, 0, 0), 'depreciation_value': 1000.0,
             'accumulated_value': 1500.0, 'exceptional_value': 0.0, 'base_value': 5000.0, 'readonly': True, 'book_value': 3500.0,
             'previous_years_accumulated_value': 500.0, 'current_year_accumulated_value': 1000.0},
            {'book_value_wo_exceptional': 2500.0, 'depreciation_date': datetime(2014, 12, 31, 0, 0), 'depreciation_value': 1000.0,
             'accumulated_value': 2500.0, 'exceptional_value': 0.0, 'base_value': 5000.0, 'readonly': False, 'book_value': 2500.0,
             'previous_years_accumulated_value': 1500.0, 'current_year_accumulated_value': 1000.0},
            {'book_value_wo_exceptional': 1500.0, 'depreciation_date': datetime(2015, 12, 31, 0, 0), 'depreciation_value': 1000.0,
             'accumulated_value': 3500.0, 'exceptional_value': 0.0, 'base_value': 5000.0, 'readonly': False, 'book_value': 1500.0,
             'previous_years_accumulated_value': 2500.0, 'current_year_accumulated_value': 1000.0},
            {'book_value_wo_exceptional': 500.0, 'depreciation_date': datetime(2016, 12, 31, 0, 0), 'depreciation_value': 1000.0,
             'accumulated_value': 4500.0, 'exceptional_value': 0.0, 'base_value': 5000.0, 'readonly': False, 'book_value': 500.0,
             'previous_years_accumulated_value': 3500.0, 'current_year_accumulated_value': 1000.0},
            {'book_value_wo_exceptional': 0.0, 'depreciation_date': datetime(2017, 12, 31, 0, 0), 'depreciation_value': 500.0,
             'accumulated_value': 5000.0, 'exceptional_value': 0.0, 'base_value': 5000.0, 'readonly': False, 'book_value': 0.0,
             'previous_years_accumulated_value': 4500.0, 'current_year_accumulated_value': 500.0},
        ]
        self._test_depreciation_board(kwargs, result)

    def test_linear_depr_with_ro_and_exceptional(self):
        kwargs = {'purchase_value': 5000.0, 'method_info': LINEAR_METHOD, 'annuities': 4, 'depreciation_start_date': '2012-07-01',
                  'readonly_values': {'2012-12': {'depreciation_value': 1500.0, 'base_value': 5000.0},
                                      '2013-12': {'depreciation_value': 1500.0, 'base_value': 3500.0}}, 'exceptional_values': {'2013-05': 500.0}}
        result = [
            {'book_value_wo_exceptional': 3500.0, 'depreciation_date': datetime(2012, 12, 31, 0, 0), 'depreciation_value': 1500.0,
             'accumulated_value': 1500.0, 'exceptional_value': 0.0, 'base_value': 5000.0, 'readonly': True, 'book_value': 3500.0,
             'previous_years_accumulated_value': 0.0, 'current_year_accumulated_value': 1500.0},
            {'book_value_wo_exceptional': 2000.0, 'depreciation_date': datetime(2013, 12, 31, 0, 0), 'depreciation_value': 1500.0,
             'accumulated_value': 3000.0, 'exceptional_value': 500.0, 'base_value': 3500.0, 'readonly': True, 'book_value': 1500.0,
             'previous_years_accumulated_value': 1500.0, 'current_year_accumulated_value': 2000.0},
            {'book_value_wo_exceptional': 1250.0, 'depreciation_date': datetime(2014, 12, 31, 0, 0), 'depreciation_value': 750.0,
             'accumulated_value': 3750.0, 'exceptional_value': 0.0, 'base_value': 1500.0, 'readonly': False, 'book_value': 750.0,
             'previous_years_accumulated_value': 3500.0, 'current_year_accumulated_value': 750.0},
            {'book_value_wo_exceptional': 500.0, 'depreciation_date': datetime(2015, 12, 31, 0, 0), 'depreciation_value': 750.0,
             'accumulated_value': 4500.0, 'exceptional_value': 0.0, 'base_value': 1500.0, 'readonly': False, 'book_value': 0.0,
             'previous_years_accumulated_value': 4250.0, 'current_year_accumulated_value': 750.0},
        ]
        self._test_depreciation_board(kwargs, result)

    def test_linear_depr_with_sale_date(self):
        kwargs = {'purchase_value': 5000.0, 'method_info': LINEAR_METHOD, 'annuities': 5, 'depreciation_start_date': '2012-01-01',
                  'sale_date': '2014-07-01'}
        result = [
            {'book_value_wo_exceptional': 4000.0, 'depreciation_date': datetime(2012, 12, 31, 0, 0), 'depreciation_value': 1000.0,
             'accumulated_value': 1000.0, 'exceptional_value': 0.0, 'base_value': 5000.0, 'readonly': False, 'book_value': 4000.0,
             'previous_years_accumulated_value': 0.0, 'current_year_accumulated_value': 1000.0},
            {'book_value_wo_exceptional': 3000.0, 'depreciation_date': datetime(2013, 12, 31, 0, 0), 'depreciation_value': 1000.0,
             'accumulated_value': 2000.0, 'exceptional_value': 0.0, 'base_value': 5000.0, 'readonly': False, 'book_value': 3000.0,
             'previous_years_accumulated_value': 1000.0, 'current_year_accumulated_value': 1000.0},
            {'book_value_wo_exceptional': 2500.0, 'depreciation_date': datetime(2014, 7, 1, 0, 0), 'depreciation_value': 500.0,
             'accumulated_value': 2500.0, 'exceptional_value': 0.0, 'base_value': 5000.0, 'readonly': False, 'book_value': 2500.0,
             'previous_years_accumulated_value': 2000.0, 'current_year_accumulated_value': 500.0},
        ]
        self._test_depreciation_board(kwargs, result)

    def test_linear_depr_with_sale_date_with_ro(self):
        kwargs = {'purchase_value': 5000.0, 'method_info': LINEAR_METHOD, 'annuities': 5, 'depreciation_start_date': '2012-01-01',
                  'sale_date': '2014-07-01', 'readonly_values': {'2012-12': {'depreciation_value': 1000.0, 'base_value': 5000.0}}}
        result = [
            {'book_value_wo_exceptional': 4000.0, 'depreciation_date': datetime(2012, 12, 31, 0, 0), 'depreciation_value': 1000.0,
             'accumulated_value': 1000.0, 'exceptional_value': 0.0, 'base_value': 5000.0, 'readonly': True, 'book_value': 4000.0,
             'previous_years_accumulated_value': 0.0, 'current_year_accumulated_value': 1000.0},
            {'book_value_wo_exceptional': 3000.0, 'depreciation_date': datetime(2013, 12, 31, 0, 0), 'depreciation_value': 1000.0,
             'accumulated_value': 2000.0, 'exceptional_value': 0.0, 'base_value': 5000.0, 'readonly': False, 'book_value': 3000.0,
             'previous_years_accumulated_value': 1000.0, 'current_year_accumulated_value': 1000.0},
            {'book_value_wo_exceptional': 2500.0, 'depreciation_date': datetime(2014, 7, 1, 0, 0), 'depreciation_value': 500.0,
             'accumulated_value': 2500.0, 'exceptional_value': 0.0, 'base_value': 5000.0, 'readonly': False, 'book_value': 2500.0,
             'previous_years_accumulated_value': 2000.0, 'current_year_accumulated_value': 500.0},
        ]
        self._test_depreciation_board(kwargs, result)

    def test_linear_depr_with_board_stop_date(self):
        kwargs = {'purchase_value': 5000.0, 'method_info': LINEAR_METHOD, 'annuities': 5, 'depreciation_start_date': '2012-01-01',
                  'board_stop_date': '2017-05-30'}
        result = [
            {'book_value_wo_exceptional': 4000.0, 'depreciation_date': datetime(2012, 12, 31, 0, 0), 'depreciation_value': 1000.0,
             'accumulated_value': 1000.0, 'exceptional_value': 0.0, 'base_value': 5000.0, 'readonly': False, 'book_value': 4000.0,
             'previous_years_accumulated_value': 0.0, 'current_year_accumulated_value': 1000.0},
            {'book_value_wo_exceptional': 3000.0, 'depreciation_date': datetime(2013, 12, 31, 0, 0), 'depreciation_value': 1000.0,
             'accumulated_value': 2000.0, 'exceptional_value': 0.0, 'base_value': 5000.0, 'readonly': False, 'book_value': 3000.0,
             'previous_years_accumulated_value': 1000.0, 'current_year_accumulated_value': 1000.0},
            {'book_value_wo_exceptional': 2000.0, 'depreciation_date': datetime(2014, 12, 31, 0, 0), 'depreciation_value': 1000.0,
             'accumulated_value': 3000.0, 'exceptional_value': 0.0, 'base_value': 5000.0, 'readonly': False, 'book_value': 2000.0,
             'previous_years_accumulated_value': 2000.0, 'current_year_accumulated_value': 1000.0},
            {'book_value_wo_exceptional': 1000.0, 'depreciation_date': datetime(2015, 12, 31, 0, 0), 'depreciation_value': 1000.0,
             'accumulated_value': 4000.0, 'exceptional_value': 0.0, 'base_value': 5000.0, 'readonly': False, 'book_value': 1000.0,
             'previous_years_accumulated_value': 3000.0, 'current_year_accumulated_value': 1000.0},
            {'book_value_wo_exceptional': 0.0, 'depreciation_date': datetime(2016, 12, 31, 0, 0), 'depreciation_value': 1000.0,
             'accumulated_value': 5000.0, 'exceptional_value': 0.0, 'base_value': 5000.0, 'readonly': False, 'book_value': 0.0,
             'previous_years_accumulated_value': 4000.0, 'current_year_accumulated_value': 1000.0},
            {'book_value_wo_exceptional': 0.0, 'depreciation_date': datetime(2017, 12, 31, 0, 0), 'depreciation_value': 0.0,
             'accumulated_value': 5000.0, 'exceptional_value': 0.0, 'base_value': 5000.0, 'readonly': False, 'book_value': 0.0,
             'previous_years_accumulated_value': 5000.0, 'current_year_accumulated_value': 0.0},
        ]
        self._test_depreciation_board(kwargs, result)

    def test_linear_depr_with_exceptional_before_start_date(self):
        kwargs = {'purchase_value': 6000.0, 'method_info': LINEAR_METHOD, 'annuities': 5, 'depreciation_start_date': '2012-01-01',
                  'exceptional_values': {'2011-12': 1000.0}}
        result = [
            {'book_value_wo_exceptional': 5000.0, 'depreciation_date': datetime(2012, 12, 31, 0, 0), 'depreciation_value': 1000.0,
             'accumulated_value': 1000.0, 'exceptional_value': 0.0, 'base_value': 5000.0, 'readonly': False, 'book_value': 4000.0,
             'previous_years_accumulated_value': 1000.0, 'current_year_accumulated_value': 1000.0},
            {'book_value_wo_exceptional': 4000.0, 'depreciation_date': datetime(2013, 12, 31, 0, 0), 'depreciation_value': 1000.0,
             'accumulated_value': 2000.0, 'exceptional_value': 0.0, 'base_value': 5000.0, 'readonly': False, 'book_value': 3000.0,
             'previous_years_accumulated_value': 2000.0, 'current_year_accumulated_value': 1000.0},
            {'book_value_wo_exceptional': 3000.0, 'depreciation_date': datetime(2014, 12, 31, 0, 0), 'depreciation_value': 1000.0,
             'accumulated_value': 3000.0, 'exceptional_value': 0.0, 'base_value': 5000.0, 'readonly': False, 'book_value': 2000.0,
             'previous_years_accumulated_value': 3000.0, 'current_year_accumulated_value': 1000.0},
            {'book_value_wo_exceptional': 2000.0, 'depreciation_date': datetime(2015, 12, 31, 0, 0), 'depreciation_value': 1000.0,
             'accumulated_value': 4000.0, 'exceptional_value': 0.0, 'base_value': 5000.0, 'readonly': False, 'book_value': 1000.0,
             'previous_years_accumulated_value': 4000.0, 'current_year_accumulated_value': 1000.0},
            {'book_value_wo_exceptional': 1000.0, 'depreciation_date': datetime(2016, 12, 31, 0, 0), 'depreciation_value': 1000.0,
             'accumulated_value': 5000.0, 'exceptional_value': 0.0, 'base_value': 5000.0, 'readonly': False, 'book_value': 0.0,
             'previous_years_accumulated_value': 5000.0, 'current_year_accumulated_value': 1000.0},
        ]
        self._test_depreciation_board(kwargs, result)

    def test_linear_depr_doesnt_start_on_1st_day_with_6_monthly_depr(self):
        kwargs = {'purchase_value': 2000.0, 'method_info': LINEAR_METHOD, 'annuities': 2, 'depreciation_start_date': '2012-07-01',
                  'depreciation_period': 6}
        result = [
            {'book_value_wo_exceptional': 1500.0, 'depreciation_date': datetime(2012, 12, 31, 0, 0), 'depreciation_value': 500.0,
             'accumulated_value': 500.0, 'exceptional_value': 0.0, 'base_value': 2000.0, 'readonly': False, 'book_value': 1500.0,
             'previous_years_accumulated_value': 0.0, 'current_year_accumulated_value': 500.0},
            {'book_value_wo_exceptional': 1000.0, 'depreciation_date': datetime(2013, 6, 30, 0, 0), 'depreciation_value': 500.0,
             'accumulated_value': 1000.0, 'exceptional_value': 0.0, 'base_value': 2000.0, 'readonly': False, 'book_value': 1000.0,
             'previous_years_accumulated_value': 500.0, 'current_year_accumulated_value': 500.0},
            {'book_value_wo_exceptional': 500.0, 'depreciation_date': datetime(2013, 12, 31, 0, 0), 'depreciation_value': 500.0,
             'accumulated_value': 1500.0, 'exceptional_value': 0.0, 'base_value': 2000.0, 'readonly': False, 'book_value': 500.0,
             'previous_years_accumulated_value': 500.0, 'current_year_accumulated_value': 1000.0},
            {'book_value_wo_exceptional': 250.0, 'depreciation_date': datetime(2014, 6, 30, 0, 0), 'depreciation_value': 250.0,
             'accumulated_value': 1750.0, 'exceptional_value': 0.0, 'base_value': 2000.0, 'readonly': False, 'book_value': 250.0,
             'previous_years_accumulated_value': 1500.0, 'current_year_accumulated_value': 250.0},
            {'book_value_wo_exceptional': 0.0, 'depreciation_date': datetime(2014, 12, 31, 0, 0), 'depreciation_value': 250.0,
             'accumulated_value': 2000.0, 'exceptional_value': 0.0, 'base_value': 2000.0, 'readonly': False, 'book_value': 0.0,
             'previous_years_accumulated_value': 1500.0, 'current_year_accumulated_value': 500.0},
        ]
        self._test_depreciation_board(kwargs, result)

    def test_linear_depr_4_monthly(self):
        kwargs = {'purchase_value': 4000.0, 'method_info': LINEAR_METHOD, 'annuities': 2, 'depreciation_start_date': '2012-01-01',
                  'depreciation_period': 4}
        result = [
            {'book_value_wo_exceptional': 3333.33, 'depreciation_date': datetime(2012, 4, 30, 0, 0), 'depreciation_value': 666.67,
             'accumulated_value': 666.67, 'exceptional_value': 0.0, 'base_value': 4000.0, 'readonly': False, 'book_value': 3333.33,
             'previous_years_accumulated_value': 0.0, 'current_year_accumulated_value': 666.67},
            {'book_value_wo_exceptional': 2666.66, 'depreciation_date': datetime(2012, 8, 31, 0, 0), 'depreciation_value': 666.67,
             'accumulated_value': 1333.34, 'exceptional_value': 0.0, 'base_value': 4000.0, 'readonly': False, 'book_value': 2666.66,
             'previous_years_accumulated_value': 0.0, 'current_year_accumulated_value': 1333.34},
            {'book_value_wo_exceptional': 2000.0, 'depreciation_date': datetime(2012, 12, 31, 0, 0), 'depreciation_value': 666.66,
             'accumulated_value': 2000.0, 'exceptional_value': 0.0, 'base_value': 4000.0, 'readonly': False, 'book_value': 2000.0,
             'previous_years_accumulated_value': 0.0, 'current_year_accumulated_value': 2000.0},
            {'book_value_wo_exceptional': 1333.33, 'depreciation_date': datetime(2013, 4, 30, 0, 0), 'depreciation_value': 666.67,
             'accumulated_value': 2666.67, 'exceptional_value': 0.0, 'base_value': 4000.0, 'readonly': False, 'book_value': 1333.33,
             'previous_years_accumulated_value': 2000.0, 'current_year_accumulated_value': 666.67},
            {'book_value_wo_exceptional': 666.66, 'depreciation_date': datetime(2013, 8, 31, 0, 0), 'depreciation_value': 666.67,
             'accumulated_value': 3333.34, 'exceptional_value': 0.0, 'base_value': 4000.0, 'readonly': False, 'book_value': 666.66,
             'previous_years_accumulated_value': 2000.0, 'current_year_accumulated_value': 1333.34},
            {'book_value_wo_exceptional': 0.0, 'depreciation_date': datetime(2013, 12, 31, 0, 0), 'depreciation_value': 666.66,
             'accumulated_value': 4000.0, 'exceptional_value': 0.0, 'base_value': 4000.0, 'readonly': False, 'book_value': 0.0,
             'previous_years_accumulated_value': 2000.0, 'current_year_accumulated_value': 2000.0},
        ]
        self._test_depreciation_board(kwargs, result)

    def test_linear_depr_monthly_start_on_1st_day(self):
        kwargs = {'purchase_value': 12000.0, 'method_info': LINEAR_METHOD, 'annuities': 1, 'depreciation_start_date': '2012-07-01',
                  'depreciation_period': 1, 'board_stop_date': '2013-06-30'}
        result = [
            {'book_value_wo_exceptional': 11000.0, 'depreciation_date': datetime(2012, 7, 31, 0, 0), 'current_year_accumulated_value': 1000.0,
             'readonly': False, 'depreciation_value': 1000.0, 'accumulated_value': 1000.0, 'exceptional_value': 0.0, 'base_value': 12000.0,
             'previous_years_accumulated_value': 0.0, 'book_value': 11000.0},
            {'book_value_wo_exceptional': 10000.0, 'depreciation_date': datetime(2012, 8, 31, 0, 0), 'current_year_accumulated_value': 2000.0,
             'readonly': False, 'depreciation_value': 1000.0, 'accumulated_value': 2000.0, 'exceptional_value': 0.0, 'base_value': 12000.0,
             'previous_years_accumulated_value': 0.0, 'book_value': 10000.0},
            {'book_value_wo_exceptional': 9000.0, 'depreciation_date': datetime(2012, 9, 30, 0, 0), 'current_year_accumulated_value': 3000.0,
             'readonly': False, 'depreciation_value': 1000.0, 'accumulated_value': 3000.0, 'exceptional_value': 0.0, 'base_value': 12000.0,
             'previous_years_accumulated_value': 0.0, 'book_value': 9000.0},
            {'book_value_wo_exceptional': 8000.0, 'depreciation_date': datetime(2012, 10, 31, 0, 0), 'current_year_accumulated_value': 4000.0,
             'readonly': False, 'depreciation_value': 1000.0, 'accumulated_value': 4000.0, 'exceptional_value': 0.0, 'base_value': 12000.0,
             'previous_years_accumulated_value': 0.0, 'book_value': 8000.0},
            {'book_value_wo_exceptional': 7000.0, 'depreciation_date': datetime(2012, 11, 30, 0, 0), 'current_year_accumulated_value': 5000.0,
             'readonly': False, 'depreciation_value': 1000.0, 'accumulated_value': 5000.0, 'exceptional_value': 0.0, 'base_value': 12000.0,
             'previous_years_accumulated_value': 0.0, 'book_value': 7000.0},
            {'book_value_wo_exceptional': 6000.0, 'depreciation_date': datetime(2012, 12, 31, 0, 0), 'current_year_accumulated_value': 6000.0,
             'readonly': False, 'depreciation_value': 1000.0, 'accumulated_value': 6000.0, 'exceptional_value': 0.0, 'base_value': 12000.0,
             'previous_years_accumulated_value': 0.0, 'book_value': 6000.0},
            {'book_value_wo_exceptional': 5000.0, 'depreciation_date': datetime(2013, 1, 31, 0, 0), 'current_year_accumulated_value': 1000.0,
             'readonly': False, 'depreciation_value': 1000.0, 'accumulated_value': 7000.0, 'exceptional_value': 0.0, 'base_value': 12000.0,
             'previous_years_accumulated_value': 6000.0, 'book_value': 5000.0},
            {'book_value_wo_exceptional': 4000.0, 'depreciation_date': datetime(2013, 2, 28, 0, 0), 'current_year_accumulated_value': 2000.0,
             'readonly': False, 'depreciation_value': 1000.0, 'accumulated_value': 8000.0, 'exceptional_value': 0.0, 'base_value': 12000.0,
             'previous_years_accumulated_value': 6000.0, 'book_value': 4000.0},
            {'book_value_wo_exceptional': 3000.0, 'depreciation_date': datetime(2013, 3, 31, 0, 0), 'current_year_accumulated_value': 3000.0,
             'readonly': False, 'depreciation_value': 1000.0, 'accumulated_value': 9000.0, 'exceptional_value': 0.0, 'base_value': 12000.0,
             'previous_years_accumulated_value': 6000.0, 'book_value': 3000.0},
            {'book_value_wo_exceptional': 2000.0, 'depreciation_date': datetime(2013, 4, 30, 0, 0), 'current_year_accumulated_value': 4000.0,
             'readonly': False, 'depreciation_value': 1000.0, 'accumulated_value': 10000.0, 'exceptional_value': 0.0, 'base_value': 12000.0,
             'previous_years_accumulated_value': 6000.0, 'book_value': 2000.0},
            {'book_value_wo_exceptional': 1000.0, 'depreciation_date': datetime(2013, 5, 31, 0, 0), 'current_year_accumulated_value': 5000.0,
             'readonly': False, 'depreciation_value': 1000.0, 'accumulated_value': 11000.0, 'exceptional_value': 0.0, 'base_value': 12000.0,
             'previous_years_accumulated_value': 6000.0, 'book_value': 1000.0},
            {'book_value_wo_exceptional': 0.0, 'depreciation_date': datetime(2013, 6, 30, 0, 0), 'current_year_accumulated_value': 6000.0,
             'readonly': False, 'depreciation_value': 1000.0, 'accumulated_value': 12000.0, 'exceptional_value': 0.0, 'base_value': 12000.0,
             'previous_years_accumulated_value': 6000.0, 'book_value': 0.0},
        ]
        self._test_depreciation_board(kwargs, result)

    def test_linear_depr_monthly_start_on_16th_day(self):
        kwargs = {'purchase_value': 12000.0, 'method_info': LINEAR_METHOD, 'annuities': 1, 'depreciation_start_date': '2012-07-16',
                  'depreciation_period': 1, 'board_stop_date': '2013-07-15'}
        result = [
            {'book_value_wo_exceptional': 11500.0, 'depreciation_date': datetime(2012, 7, 31, 0, 0), 'current_year_accumulated_value': 500.0,
             'readonly': False, 'depreciation_value': 500.0, 'accumulated_value': 500.0, 'exceptional_value': 0.0, 'base_value': 12000.0,
             'previous_years_accumulated_value': 0.0, 'book_value': 11500.0},
            {'book_value_wo_exceptional': 10500.0, 'depreciation_date': datetime(2012, 8, 31, 0, 0), 'current_year_accumulated_value': 1500.0,
             'readonly': False, 'depreciation_value': 1000.0, 'accumulated_value': 1500.0, 'exceptional_value': 0.0, 'base_value': 12000.0,
             'previous_years_accumulated_value': 0.0, 'book_value': 10500.0},
            {'book_value_wo_exceptional': 9500.0, 'depreciation_date': datetime(2012, 9, 30, 0, 0), 'current_year_accumulated_value': 2500.0,
             'readonly': False, 'depreciation_value': 1000.0, 'accumulated_value': 2500.0, 'exceptional_value': 0.0, 'base_value': 12000.0,
             'previous_years_accumulated_value': 0.0, 'book_value': 9500.0},
            {'book_value_wo_exceptional': 8500.0, 'depreciation_date': datetime(2012, 10, 31, 0, 0), 'current_year_accumulated_value': 3500.0,
             'readonly': False, 'depreciation_value': 1000.0, 'accumulated_value': 3500.0, 'exceptional_value': 0.0, 'base_value': 12000.0,
             'previous_years_accumulated_value': 0.0, 'book_value': 8500.0},
            {'book_value_wo_exceptional': 7500.0, 'depreciation_date': datetime(2012, 11, 30, 0, 0), 'current_year_accumulated_value': 4500.0,
             'readonly': False, 'depreciation_value': 1000.0, 'accumulated_value': 4500.0, 'exceptional_value': 0.0, 'base_value': 12000.0,
             'previous_years_accumulated_value': 0.0, 'book_value': 7500.0},
            {'book_value_wo_exceptional': 6500.0, 'depreciation_date': datetime(2012, 12, 31, 0, 0), 'current_year_accumulated_value': 5500.0,
             'readonly': False, 'depreciation_value': 1000.0, 'accumulated_value': 5500.0, 'exceptional_value': 0.0, 'base_value': 12000.0,
             'previous_years_accumulated_value': 0.0, 'book_value': 6500.0},
            {'book_value_wo_exceptional': 5500.0, 'depreciation_date': datetime(2013, 1, 31, 0, 0), 'current_year_accumulated_value': 1000.0,
             'readonly': False, 'depreciation_value': 1000.0, 'accumulated_value': 6500.0, 'exceptional_value': 0.0, 'base_value': 12000.0,
             'previous_years_accumulated_value': 5500.0, 'book_value': 5500.0},
            {'book_value_wo_exceptional': 4500.0, 'depreciation_date': datetime(2013, 2, 28, 0, 0), 'current_year_accumulated_value': 2000.0,
             'readonly': False, 'depreciation_value': 1000.0, 'accumulated_value': 7500.0, 'exceptional_value': 0.0, 'base_value': 12000.0,
             'previous_years_accumulated_value': 5500.0, 'book_value': 4500.0},
            {'book_value_wo_exceptional': 3500.0, 'depreciation_date': datetime(2013, 3, 31, 0, 0), 'current_year_accumulated_value': 3000.0,
             'readonly': False, 'depreciation_value': 1000.0, 'accumulated_value': 8500.0, 'exceptional_value': 0.0, 'base_value': 12000.0,
             'previous_years_accumulated_value': 5500.0, 'book_value': 3500.0},
            {'book_value_wo_exceptional': 2500.0, 'depreciation_date': datetime(2013, 4, 30, 0, 0), 'current_year_accumulated_value': 4000.0,
             'readonly': False, 'depreciation_value': 1000.0, 'accumulated_value': 9500.0, 'exceptional_value': 0.0, 'base_value': 12000.0,
             'previous_years_accumulated_value': 5500.0, 'book_value': 2500.0},
            {'book_value_wo_exceptional': 1500.0, 'depreciation_date': datetime(2013, 5, 31, 0, 0), 'current_year_accumulated_value': 5000.0,
             'readonly': False, 'depreciation_value': 1000.0, 'accumulated_value': 10500.0, 'exceptional_value': 0.0, 'base_value': 12000.0,
             'previous_years_accumulated_value': 5500.0, 'book_value': 1500.0},
            {'book_value_wo_exceptional': 500.0, 'depreciation_date': datetime(2013, 6, 30, 0, 0), 'current_year_accumulated_value': 6000.0,
             'readonly': False, 'depreciation_value': 1000.0, 'accumulated_value': 11500.0, 'exceptional_value': 0.0, 'base_value': 12000.0,
             'previous_years_accumulated_value': 5500.0, 'book_value': 500.0},
            {'book_value_wo_exceptional': 0.0, 'depreciation_date': datetime(2013, 7, 31, 0, 0), 'current_year_accumulated_value': 6500.0,
             'readonly': False, 'depreciation_value': 500.0, 'accumulated_value': 12000.0, 'exceptional_value': 0.0, 'base_value': 12000.0,
             'previous_years_accumulated_value': 5500.0, 'book_value': 0.0},
        ]
        self._test_depreciation_board(kwargs, result)
