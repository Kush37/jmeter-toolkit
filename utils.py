import uuid
import xml.etree.ElementTree as ET
from xml.dom import minidom

# IMPORTANT: no colon (:)
PT_ID = "pt_id"


def new_id(prefix: str = "id") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"


def parse_xml(xml_string: str) -> ET.Element:
    return ET.fromstring(xml_string)


def prettify(elem: ET.Element) -> str:
    ET.indent(elem, space="  ")
    return ET.tostring(elem, encoding="unicode")
