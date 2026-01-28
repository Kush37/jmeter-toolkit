import xml.etree.ElementTree as ET
from .utils import parse_xml, prettify, new_id, PT_ID


def add_think_time_between_transactions(jmx_xml: str, tg_id: str, think_time_ms: int = 5000):
    root = parse_xml(jmx_xml)

    tg = next(e for e in root.iter("ThreadGroup") if e.attrib.get(PT_ID) == tg_id)

    parent, idx = None, None
    for e in root.iter():
        children = list(e)
        for i, c in enumerate(children):
            if c is tg:
                parent, idx = e, i
                break
        if parent:
            break

    tree = parent[idx + 1]
    children = list(tree)

    i = 0
    while i < len(children):
        if children[i].tag == "TransactionController":
            flow = ET.Element(
                "TestAction",
                {
                    "guiclass": "TestActionGui",
                    "testclass": "TestAction",
                    "testname": f"Think Time ({think_time_ms} ms)",
                    "enabled": "true",
                    PT_ID: new_id("think"),
                },
            )

            ET.SubElement(flow, "intProp", {"name": "ActionProcessor.action"}).text = "1"
            ET.SubElement(flow, "stringProp", {"name": "ActionProcessor.duration"}).text = str(think_time_ms)

            children.insert(i + 2, flow)
            children.insert(i + 3, ET.Element("hashTree"))
            i += 2
        i += 1

    tree[:] = children
    return prettify(root)
