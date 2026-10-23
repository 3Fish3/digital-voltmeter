#!/usr/bin/env python3
"""Inspection-only Blue Pill dual 20-pin SVG overlay; not a PCB footprint."""
import argparse
import math
from pathlib import Path

def render(center_mm, pitch_mm, count, nominal=False):
    if not all(math.isfinite(x) and x > 0 for x in (center_mm, pitch_mm)):
        raise ValueError("dimensions must be positive and finite")
    if not isinstance(count, int) or not 2 <= count <= 60:
        raise ValueError("pin count must be between 2 and 60")
    x0, x1, y0 = 20.0, 20.0 + center_mm, 24.0
    height = y0 + (count-1) * pitch_mm + 27
    width = max(85.0, x1 + 28)
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:.3f}mm" height="{height:.3f}mm" viewBox="0 0 {width:.3f} {height:.3f}">',
         '<title>Blue Pill pin-centre trial - NOT A FOOTPRINT</title>',
         f'<text x="3" y="5" font-size="3">{"NOMINAL PREVIEW - NOT MEASURED" if nominal else "MEASURED DIMENSIONS - VERIFY WITH BOARD"}</text>',
         '<text x="3" y="10" font-size="2.5">USB UP, TOP VIEW. Markers are centres, NOT drill sizes.</text>',
         f'<text x="3" y="14" font-size="2.5">Row centres {center_mm:.3f}mm, pitch {pitch_mm:.3f}mm, {count} pins/row</text>']
    for i in range(count):
        y=y0+i*pitch_mm
        for row,x in (("A",x0),("B",x1)):
            s.append(f'<circle data-row="{row}" data-pin="{i+1}" cx="{x:.3f}" cy="{y:.3f}" r=".35" fill="none" stroke="black" stroke-width=".18"/>')
    y=height-12
    s += [f'<path d="M{x0} {y} h10" fill="none" stroke="black" stroke-width=".4"/>',
          f'<text x="{x0+12}" y="{y+1}" font-size="2.5">10mm ruler: print 100%, no scaling</text>',
          f'<text x="3" y="{height-4}" font-size="2.3">NOT FOR PCB / DRILL / GERBER. SWD and USB clearance not represented.</text>', '</svg>']
    return '\n'.join(s)+'\n'

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--nominal-preview',action='store_true')
    p.add_argument('--center-mm',type=float)
    p.add_argument('--pitch-mm',type=float)
    p.add_argument('--pins-per-row',type=int)
    p.add_argument('--output',required=True,type=Path)
    a=p.parse_args(argv)
    if a.nominal_preview:
        if any(v is not None for v in (a.center_mm,a.pitch_mm,a.pins_per_row)):
            p.error('nominal mode cannot mix measured dimensions')
        center,pitch,count=15.24,2.54,20
    else:
        if any(v is None for v in (a.center_mm,a.pitch_mm,a.pins_per_row)):
            p.error('measured mode requires all three dimensions')
        center,pitch,count=a.center_mm,a.pitch_mm,a.pins_per_row
    try: content=render(center,pitch,count,a.nominal_preview)
    except ValueError as e: p.error(str(e))
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(content,encoding='utf-8')
    print(f'Wrote inspection-only SVG: {a.output}')
    return 0

if __name__=='__main__':
    raise SystemExit(main())
