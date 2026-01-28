import xml.etree.ElementTree as ET
from .utils import parse_xml, prettify, new_id, PT_ID


def add_thread_group(jmx_xml: str, name: str, num_threads: int, ramp_time: int, loops: int = 1):
    root = parse_xml(jmx_xml)
    tg_id = new_id("tg")

    test_plan = root.find(".//TestPlan")

    parent, idx = None, None
    for e in root.iter():
        children = list(e)
        for i, c in enumerate(children):
            if c is test_plan:
                parent, idx = e, i
                break
        if parent:
            break

    tree = parent[idx + 1]

    tg = ET.Element(
        "ThreadGroup",
        {
            "guiclass": "ThreadGroupGui",
            "testclass": "ThreadGroup",
            "testname": name,
            "enabled": "true",
            PT_ID: tg_id,
        },
    )

    ET.SubElement(tg, "stringProp", {"name": "ThreadGroup.num_threads"}).text = str(num_threads)
    ET.SubElement(tg, "stringProp", {"name": "ThreadGroup.ramp_time"}).text = str(ramp_time)

    loop = ET.SubElement(tg, "elementProp", {"name": "ThreadGroup.main_controller", "elementType": "LoopController"})
    ET.SubElement(loop, "stringProp", {"name": "LoopController.loops"}).text = str(loops)

    tree.append(tg)
    tree.append(ET.Element("hashTree"))

    return prettify(root), tg_id
