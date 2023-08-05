#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  February 09, 2022 Calvin Neumann
#  Initial Commit
#
#  Copyright (C) 2022 - Calvin Neumann
#  License:  AGPLv3
#
# This code is free software; you can redistribute it and/or
# modify it under the terms of the GNU AFFERO GENERAL PUBLIC LICENSE
# License as published by the Free Software Foundation; either
# version 3 of the License, or any later version.
#
# This code is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU AFFERO GENERAL PUBLIC LICENSE for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import xml.etree.ElementTree as ET
import re
import logging

logging = logging.getLogger('maue parser')

def _clean_value(value):
    """replaces empty strings with the value None.
    replaces the coordinates 0.000000 or 0.000000
    and the empty date/time object --.--.-------:--:-- with None

    Parameters
    ----------
    value : str
        value replace with None if necessary

    Returns
    -------
    string | None
        a string if value wasn't replaces by None
    """
    value = value.strip()
    if (not value or
        re.match(r'^0+[,\.]+0+$', value) or             # 0.000000 or 0,000000
        re.match(r'^--\.--\.-------:--:--$', value)):   # --.--.-------:--:--
        logging.debug('value "{}" replaced with None'.format(value))
        value = None
    return value

def _parse_einsatzdaten(xml):
    """parses the "Einsatzdaten" from the content of the xml file

    Parameters
    ----------
    xml : xml.etree.ElementTree.Element
        xml root Tree Element

    Returns
    -------
    dict 
        a dictionary with all "Einsatzdaten" details
    """
    root = xml.getroot()

    # parse field names
    header_childs = root.findall('Data')
    header = list(map(lambda el: el.attrib["header"], header_childs))
    if not len(header):
        logging.debug('no Data objects with header information found')
        logging.error('error parsing field names')
        raise KeyError('no Data Objects found')
    
    # parse values
    row_childs = root.findall('Row')
    row_child = [child for child in row_childs if len(child)][0]
    value_elements = row_child.findall('Column')
    if not len(value_elements):
        logging.debug('no Value objects found')
        logging.error('error parsing values')
        raise KeyError('no Value objects found')

    values = map(lambda el: el.attrib['value'], value_elements)
    values = list(map(_clean_value, values))

    # create dict
    if len(header) != len(values):
        logging.debug('count of header names don\'t match count of values - {} != {}'.format(len(header), len(values)))
        logging.error('error merging names and values')
        raise ValueError('len names must match len values - {} != {}'.format(len(header), len(values)))
    logging.debug('Einsatzdaten parsed')
    return dict(zip(header, values))

def _get_detail_table(xml, name):
    """extracts the table object with the name <name> from the xml file

    Parameters
    ----------
    xml : xml.etree.ElementTree.Element
        xml root Tree Element

    name : string
        name of detail table

    Returns
    -------
    xml.etree.ElementTree.Element 
        Tree Element of table
    """
    root = xml.getroot()

    # get table
    row_childs = root.findall('Row')
    if not len(row_childs):
        logging.debug('no Row element found')
        logging.error('error extracting detail table')
        raise KeyError('no Row object found')
    root = [child for child in row_childs if len(child)][0]
    table_childs = root.findall('Table')
    if not len(table_childs):
        logging.debug('no Table element found')
        logging.error('error extracting detail table')
        raise KeyError('no Table object found')    
    tables = [child for child in table_childs if child.attrib['name'] == name]

    if not tables:
        logging.debug('no Table with name {} found'.format(name))
        logging.error('error extracting detail table')
        raise KeyError('no table with name {} found'.format(name))

    logging.debug('detail table {} extracted'.format(name))
    return tables[0]

def _parse_detail_table(xml, name):
    """parses the details of a table from the content of the xml file

    Parameters
    ----------
    xml : xml.etree.ElementTree.Element
        xml root Tree Element

    name : string
        name of detail table

    Returns
    -------
    dict 
        a dictionary with all details from table with the name of the Parameter <name>
    """
    detail_list = None

    table = _get_detail_table(xml, name)

    # parse field names
    header_childs = table.findall('Data')
    header = list(map(lambda el: el.attrib["header"], header_childs))
    if not len(header):
        logging.debug('no Data objects with header information found')
        logging.error('error parsing field names')
        raise KeyError('no Data Objects found')

    # parse values
    row_childs = table.findall('Row')
    row_childs = [child for child in row_childs if len(child)]
    for row_child in row_childs:
        value_elements = row_child.findall('Column')
        values = map(lambda el: el.attrib['value'], value_elements)
        values = list(map(_clean_value, values))

        # init einsatzcode list
        if not detail_list:
            detail_list = []

        # create dict
        detail_list.append(dict(zip(header, values)))

    logging.debug('detail table {} parsed'.format(name))
    if detail_list:
        logging.debug('{} entries found'.format(len(detail_list)))
    else:
        logging.debug('no entries found')
    return detail_list

def parse(filename):
    """parses the maue file and returns its contents as a dictionary

    Parameters
    ----------
    filename : string
        filename or path to file

    Returns
    -------
    dict 
        a dictionary with content of maue file
    """
    alarm_dict = {}

    try:
        xml = ET.parse(filename)
    except FileNotFoundError as e:
        logging.error('file "{}" not found'.format(filename), exc_info=True)
        raise e

    alarm_dict['Einsatzdaten'] = _parse_einsatzdaten(xml)
    alarm_dict['Einsatzcodes'] = _parse_detail_table(xml, 'Einsatzcodes')
    alarm_dict['Patienten'] = _parse_detail_table(xml, 'Patienten')
    alarm_dict['Einsatzmittel'] = _parse_detail_table(xml, 'Einsatzmittel')
    alarm_dict['Meldungen'] = _parse_detail_table(xml, 'Meldungen')
    alarm_dict['Massnahmen'] = _parse_detail_table(xml, 'Massnahmen')

    logging.debug('{} successfully parsed'.format(filename))

    return alarm_dict
