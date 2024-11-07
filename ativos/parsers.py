# Copyright (c) 2014, José Padilla <hello@jpadilla.com>
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.

# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.

# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# This file contains modified source code originally created by José Padilla.
# https://github.com/jpadilla/django-rest-framework-xml

import decimal
import zlib
from datetime import datetime
from xml.etree.ElementTree import Element

from defusedxml import ElementTree
from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest
from rest_framework.exceptions import ParseError
from rest_framework.parsers import BaseParser


def xml_convert(element: Element):
    """
    convert the xml `element` into the corresponding python object
    """

    children = list(element)
    if len(children) == 0:
        return element.text

    sub_tags = []

    for child in children:
        if child.tag not in sub_tags:
            sub_tags.append(child.tag)

    final_data = {}

    for tag in sub_tags:
        elements_with_same_tag = element.findall(tag)

        if len(elements_with_same_tag) > 1:
            data = []
            for child in elements_with_same_tag:
                data.append(xml_convert(child))

        else:
            data = xml_convert(elements_with_same_tag[0])

        final_data[tag] = data

    return final_data


def type_convert(value):
    """
    Converts the value returned by the XMl parse into the equivalent
    Python type
    """
    if value is None:
        return value

    try:
        return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        pass

    try:
        return int(value)
    except ValueError:
        pass

    try:
        return decimal.Decimal(value)
    except decimal.InvalidOperation:
        pass

    return value


class XMLParser(BaseParser):
    media_type = "application/xml"

    def parse(self, stream: WSGIRequest, media_type=None, parser_context=None):
        parser_context = parser_context or {}
        encoding = parser_context.get("encoding", settings.DEFAULT_CHARSET)
        parser = ElementTree.DefusedXMLParser(encoding=encoding)
        try:
            tree = ElementTree.parse(stream, parser=parser, forbid_dtd=True)
        except (ElementTree.ParseError, ValueError) as exc:
            raise ParseError("XML parse error - %s" % str(exc))
        data = xml_convert(tree.getroot())
        return data

class ZlibXMLParser(BaseParser):
    media_type = "application/x-compress-zlib"

    def parse(self, stream: WSGIRequest, media_type=None, parser_context=None):
        parser_context = parser_context or {}
        encoding = parser_context.get("encoding", settings.DEFAULT_CHARSET)
        parser = ElementTree.DefusedXMLParser(encoding=encoding)
        try:
            tree = ElementTree.fromstring(zlib.decompress(stream.read()))
        except (ElementTree.ParseError, ValueError) as exc:
            raise ParseError("XML parse error - %s" % str(exc))
        data = xml_convert(tree)
        return data
