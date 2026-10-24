"""Resolve assigned V2.3 footprints and compare every pad number to the netlist pins.

This is a structural check only. It does not prove dimensional fit, solderability,
ERC, DRC, or electrical performance.
"""
from pathlib import Path
import argparse
import hashlib
import json
import os
import re
import xml.etree.ElementTree as ET


BASE = Path(__file__).resolve().parents[1]


def sexpr(text):
    tokens = re.findall(r'"(?:\\.|[^"\\])*"|[()]|[^\s()]+', text)
    stack = []
    root = None
    for token in tokens:
        if token == '(':
            node = []
            if stack:
                stack[-1].append(node)
            else:
                root = node
            stack.append(node)
        elif token == ')':
            if not stack:
                raise ValueError('unbalanced closing parenthesis')
            stack.pop()
        else:
            value = json.loads(token) if token.startswith('"') else token
            if not stack:
                raise ValueError('token outside expression')
            stack[-1].append(value)
    if stack or root is None:
        raise ValueError('unbalanced expression')
    return root


def children(node, name):
    return [item for item in node if isinstance(item, list) and item and item[0] == name]


def child(node, name):
    return next((item for item in node if isinstance(item, list) and item and item[0] == name), None)


def numbers(node, name):
    found = child(node, name)
    if not found:
        return None
    return [float(value) for value in found[1:]]


def project_libraries(project_dir):
    table = project_dir / 'fp-lib-table'
    if not table.is_file():
        return {}
    root = sexpr(table.read_text())
    libraries = {}
    for entry in children(root, 'lib'):
        name = child(entry, 'name')
        uri = child(entry, 'uri')
        if not name or not uri:
            continue
        libraries[name[1]] = uri[1].replace('${KIPRJMOD}', str(project_dir))
    return libraries


def footprint_file(libraries, footprint_id, system_root):
    if ':' not in footprint_id:
        raise ValueError(f'Footprint must use Library:Footprint form: {footprint_id}')
    library, name = footprint_id.split(':', 1)
    if library in libraries:
        directory = Path(libraries[library])
    else:
        directory = system_root / f'{library}.pretty'
    path = directory / f'{name}.kicad_mod'
    if not path.is_file():
        raise FileNotFoundError(f'Missing footprint: {footprint_id} ({path})')
    return path


def inspect_footprint(path):
    root = sexpr(path.read_text())
    pads = []
    for pad in children(root, 'pad'):
        number = str(pad[1])
        kind = pad[2]
        at = numbers(pad, 'at') or []
        size = numbers(pad, 'size') or []
        drill = numbers(pad, 'drill')
        if len(at) < 2 or len(size) < 2:
            raise ValueError(f'Pad {number} lacks position or size in {path}')
        if kind == 'thru_hole' and (not drill or drill[0] <= 0):
            raise ValueError(f'Through-hole pad {number} lacks a positive drill in {path}')
        pads.append({'number': number, 'type': kind, 'at_mm': at, 'size_mm': size,
                     'drill_mm': drill})
    if not pads:
        raise ValueError(f'Footprint has no pads: {path}')
    return pads


def verify(netlist, project_dir=BASE / 'hardware/v2.3',
           system_root=Path(os.environ.get('KICAD10_FOOTPRINT_DIR', '/usr/share/kicad/footprints'))):
    libraries = project_libraries(project_dir)
    root = ET.parse(netlist).getroot()
    records = []
    unassigned = []
    for component in root.findall('./components/comp'):
        ref = component.get('ref')
        footprint = component.findtext('footprint') or ''
        if not footprint:
            unassigned.append(ref)
            continue
        pin_numbers = sorted({pin.get('num') for pin in component.findall('./units/unit/pins/pin')})
        path = footprint_file(libraries, footprint, system_root)
        pads = inspect_footprint(path)
        pad_numbers = sorted({pad['number'] for pad in pads})
        missing = [pin for pin in pin_numbers if pin not in pad_numbers]
        if missing:
            raise ValueError(f'{ref}: symbol pins missing from footprint: {missing}')
        unused_pads = [pad for pad in pad_numbers if pad not in pin_numbers]
        records.append({
            'reference': ref,
            'footprint': footprint,
            'file': str(path),
            'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'symbol_pins': pin_numbers,
            'unused_pads': unused_pads,
            'pads': pads,
        })
    records.sort(key=lambda item: tuple((0, int(c)) if c.isdigit() else (1, c)
                                        for c in re.split(r'(\d+)', item['reference'])))
    return {
        'status': 'assigned footprints resolve and pad numbers match netlist pins; not PCB DRC or dimensional approval',
        'assigned_count': len(records),
        'unassigned_count': len(unassigned),
        'unassigned_references': sorted(unassigned),
        'components': records,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--netlist', type=Path,
                        default=BASE / '.tmp/v2.3-validation/voltmeter-v2.3-draft.xml')
    parser.add_argument('--project-dir', type=Path, default=BASE / 'hardware/v2.3')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = verify(args.netlist, args.project_dir)
    text = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    if args.output:
        args.output.write_text(text)
    print(text, end='')


if __name__ == '__main__':
    main()
