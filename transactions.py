import xml.etree.ElementTree as ET
from .utils import parse_xml, prettify, new_id, PT_ID


def add_transaction_controller(jmx_xml: str, tg_id: str, name: str):
    root = parse_xml(jmx_xml)
    txn_id = new_id("txn")

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

    txn = ET.Element(
        "TransactionController",
        {
            "guiclass": "TransactionControllerGui",
            "testclass": "TransactionController",
            "testname": name,
            "enabled": "true",
            PT_ID: txn_id,
        },
    )

    tree.append(txn)
    tree.append(ET.Element("hashTree"))

    return prettify(root), txn_id
