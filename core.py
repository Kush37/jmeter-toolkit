import xml.etree.ElementTree as ET
from .utils import prettify


def create_empty_jmeter_script(test_plan_name: str) -> str:
    root = ET.Element(
        "jmeterTestPlan",
        {"version": "1.2", "properties": "5.0", "jmeter": "5.6.3"},
    )

    root_hash = ET.SubElement(root, "hashTree")

    ET.SubElement(
        root_hash,
        "TestPlan",
        {
            "guiclass": "TestPlanGui",
            "testclass": "TestPlan",
            "testname": test_plan_name,
            "enabled": "true",
        },
    )

    ET.SubElement(root_hash, "hashTree")

    return prettify(root)
