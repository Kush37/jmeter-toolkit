import xml.etree.ElementTree as ET
from .utils import parse_xml, prettify, new_id, PT_ID


def add_header_manager(jmx_xml: str, sampler_id: str, headers: dict):
    if not headers:
        return jmx_xml

    root = parse_xml(jmx_xml)

    sampler = next(e for e in root.iter("HTTPSamplerProxy") if e.attrib.get(PT_ID) == sampler_id)

    parent, idx = None, None
    for e in root.iter():
        children = list(e)
        for i, c in enumerate(children):
            if c is sampler:
                parent, idx = e, i
                break
        if parent:
            break

    tree = parent[idx + 1]

    mgr = ET.Element(
        "HeaderManager",
        {
            "guiclass": "HeaderPanel",
            "testclass": "HeaderManager",
            "testname": "HTTP Header Manager",
            "enabled": "true",
            PT_ID: new_id("hdr"),
        },
    )

    coll = ET.SubElement(mgr, "collectionProp", {"name": "HeaderManager.headers"})

    for k, v in headers.items():
        e = ET.SubElement(coll, "elementProp", {"elementType": "Header"})
        ET.SubElement(e, "stringProp", {"name": "Header.name"}).text = k
        ET.SubElement(e, "stringProp", {"name": "Header.value"}).text = v

    tree.append(mgr)
    tree.append(ET.Element("hashTree"))

    return prettify(root)
