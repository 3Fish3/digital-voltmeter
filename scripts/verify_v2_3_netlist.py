"""Compare exported KiCad XML with the controlled connection blueprint.

Read-only verification; no KiCad file edits and no electrical safety guarantee.
"""
import argparse
import json
import math
from pathlib import Path

import defusedxml.ElementTree as ET


def verify(blueprint_path, netlist_path, inventory_path=None):
    try:
        blueprint = json.loads(blueprint_path.read_text())
    except (OSError, ValueError) as exc:
        raise ValueError(f"Cannot read blueprint: {blueprint_path}") from exc
    root = ET.parse(netlist_path).getroot()
    if root is None:
        raise ValueError("Empty exported netlist")
    components = blueprint["components"]
    expected_refs = {c["reference"] for c in components}
    actual_components = root.findall("./components/comp")
    actual_refs = {c.attrib["ref"] for c in actual_components}
    if len(expected_refs) != len(components) or actual_refs != expected_refs:
        raise ValueError("Reference set mismatch or duplicate blueprint reference")
    by_reference = {c.attrib["ref"]: c for c in actual_components}
    inventory_path = inventory_path or netlist_path.parent / "component-inventory.json"
    try:
        inventory_rows = json.loads(inventory_path.read_text())
    except (OSError, ValueError) as exc:
        raise ValueError(f"Cannot read MCP symbol inventory: {inventory_path}") from exc
    inventory = {c["reference"]: c for c in inventory_rows}
    declarations = blueprint.get("power_declarations", [])
    declaration_refs = {d["reference"] for d in declarations}
    if len(declarations) != len(declaration_refs) or declaration_refs & expected_refs:
        raise ValueError("Duplicate or conflicting source declarations")
    if len(inventory_rows) != len(inventory) or set(inventory) != expected_refs | declaration_refs:
        raise ValueError("MCP inventory references do not match blueprint")
    if declarations:
        try:
            labels = json.loads((inventory_path.parent / "label-inventory.json").read_text())
        except (OSError, ValueError) as exc:
            raise ValueError("Cannot read MCP label inventory") from exc
        for declaration in declarations:
            marker = inventory[declaration["reference"]]
            if declaration["lib_id"] != "power:PWR_FLAG" or marker["lib_id"] != declaration["lib_id"]:
                raise ValueError("Invalid source marker symbol")
            if marker["value"] != "PWR_FLAG" or marker.get("footprint"):
                raise ValueError("Invalid source marker value or footprint")
            if not all(math.isclose(marker[k], declaration[k], abs_tol=1e-6) for k in ("x", "y")):
                raise ValueError("Source marker position mismatch")
            # Markers are omitted from native XML. Verify their separate MCP identity
            # and the explicit label at the declared stub end; ERC remains a separate check.
            if not any(label["text"] == declaration["net"]
                       and math.isclose(label["x"], declaration["label_x"], abs_tol=1e-6)
                       and math.isclose(label["y"], declaration["label_y"], abs_tol=1e-6)
                       for label in labels):
                raise ValueError("Source declaration label mismatch")
    for component in components:
        exported = by_reference[component["reference"]]
        if exported.findtext("value") != component["value"]:
            raise ValueError(f"Value mismatch: {component['reference']}")
        source = exported.find("libsource")
        if source is None:
            raise ValueError(f"Missing symbol identity: {component['reference']}")
        expected_library, expected_part = component["lib_id"].split(":", 1)
        if source.attrib["part"] != expected_part:
            raise ValueError(f"Symbol part mismatch: {component['reference']}")
        # KiCad XML emits an empty library prefix for these custom embedded parts.
        # Do not waive identity: verify the full lib_id against a separate MCP inventory.
        if source.attrib["lib"] and source.attrib["lib"] != expected_library:
            raise ValueError(f"Symbol library mismatch: {component['reference']}")
        if inventory[component["reference"]]["lib_id"] != component["lib_id"]:
            raise ValueError(f"MCP symbol identity mismatch: {component['reference']}")
    footprints = {c.attrib["ref"]: c.findtext("footprint") for c in actual_components if c.findtext("footprint")}
    if footprints:
        raise ValueError(f"Unexpected assigned footprints: {footprints}")
    expected = {(c["reference"], str(pin)): net for c in components for pin, net in c["pins"].items() if net is not None}
    disconnected = {(c["reference"], str(pin)) for c in components for pin, net in c["pins"].items() if net is None}
    actual = {}
    net_members = {}
    for net in root.findall("./nets/net"):
        name = net.attrib["name"]
        members = {(n.attrib["ref"], n.attrib["pin"]) for n in net.findall("node")}
        net_members[name] = members
        for pin in members:
            if pin in actual:
                raise ValueError(f"Pin appears on multiple nets: {pin}")
            actual[pin] = name.rsplit("/", 1)[-1]
    mismatches = [(pin, net, actual.get(pin)) for pin, net in expected.items() if actual.get(pin) != net]
    if mismatches:
        raise ValueError(f"Pin/net mismatches: {mismatches}")
    extras = set(actual) - set(expected) - disconnected
    if extras:
        raise ValueError(f"Unexpected pins in netlist: {extras}")
    for name, members in net_members.items():
        for pin in members & disconnected:
            if len(members) != 1:
                raise ValueError(f"NC pin connected to another pin: {pin} on {name}")
    for pin in disconnected:
        if pin not in actual:
            raise ValueError(f"NC pin absent from exported netlist: {pin}")
    return {"status": "connection blueprint matches export; not safety/accuracy/ERC pass",
            "component_count": len(components), "named_net_count": len(set(expected.values())),
            "wired_pin_count": len(expected), "intentional_nc_count": len(disconnected),
            "assigned_footprints": 0, "power_declaration_count": len(declarations)}


def main():
    base = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--blueprint", type=Path, default=base / "hardware/v2.3/connections-draft.json")
    parser.add_argument("--netlist", type=Path, default=base / ".tmp/v2.3-validation/voltmeter-v2.3-draft.xml")
    parser.add_argument("--inventory", type=Path, default=base / ".tmp/v2.3-validation/component-inventory.json")
    args = parser.parse_args()
    print(json.dumps(verify(args.blueprint, args.netlist, args.inventory), indent=2))


if __name__ == "__main__":
    main()
