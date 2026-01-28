import xml.etree.ElementTree as ET
from urllib.parse import urlparse
from .utils import parse_xml, prettify, new_id, PT_ID


def add_http_sampler(jmx_xml: str, txn_id: str, name: str, method: str, url: str):
    root = parse_xml(jmx_xml)

    txn = next(e for e in root.iter("TransactionController") if e.attrib.get(PT_ID) == txn_id)

    parent, idx = None, None
    for e in root.iter():
        children = list(e)
        for i, c in enumerate(children):
            if c is txn:
                parent, idx = e, i
                break
        if parent:
            break

    tree = parent[idx + 1]

    sampler_id = new_id("sampler")
    parsed = urlparse(url)

    sampler = ET.Element(
        "HTTPSamplerProxy",
        {
            "guiclass": "HttpTestSampleGui",
            "testclass": "HTTPSamplerProxy",
            "testname": name,
            "enabled": "true",
            PT_ID: sampler_id,
        },
    )

    ET.SubElement(sampler, "stringProp", {"name": "HTTPSampler.domain"}).text = parsed.hostname or ""
    ET.SubElement(sampler, "stringProp", {"name": "HTTPSampler.path"}).text = parsed.path or "/"
    ET.SubElement(sampler, "stringProp", {"name": "HTTPSampler.method"}).text = method

    tree.append(sampler)
    tree.append(ET.Element("hashTree"))

    return prettify(root), sampler_id
