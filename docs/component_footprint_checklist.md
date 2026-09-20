# Component - Footprint Checklist

| Component | Value | Footprint Assigned | Status |
|-----------|-------|--------------------|--------|
| U1        | ADC0832 | `Package_DIP:DIP-8_W7.62mm` | Validated (DIP-8 required) |
| U2        | 74AHCT125 | `Package_DIP:DIP-14_W7.62mm` | Validated (DIP-14 required) |
| U3        | MCP6002-xP | `Package_DIP:DIP-8_W7.62mm` | Validated (DIP-8 required) |
| FB1       | Ferrite_Bead | `Resistor_THT:R_Axial_DIN0207...` | Validated (Need part verification) |
| J4, J5    | Conn_01x04 | `Connector_PinSocket_2.54mm:PinSocket_1x04_P2.54mm_Vertical` | Validated |
| J6, J7, J8| Conn_01x02 | `TerminalBlock_Phoenix_MKDS-1,5-2_1x02_P5.00mm_Horizontal` | Validated |
| C1, C4, C5| 1uF, 1uF, 100nF | `Capacitor_THT:C_Disc_D5.0mm_W2.5mm_P5.00mm` | Validated |
| C6        | 100nF | `Capacitor_THT:C_Disc_D5.0mm_W2.5mm_P5.00mm` | Validated (Assigned by agent) |
| C2, C8    | 10uF | `Capacitor_THT:CP_Radial_D5.0mm_P2.00mm` | Validated (Polarized) |
| C7        | 100uF | `Capacitor_THT:CP_Radial_D6.3mm_P2.50mm` | Validated (Polarized) |
| R1..R14   | Resistors | `Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal` | Validated (All axial THT) |
| D1..D4    | 1N4148 | `Diode_THT:D_DO-35_SOD27_P7.62mm_Horizontal` | Validated |
| J1        | Blue Pill | **[None]** | **BLOCKED**: Withheld per instructions pending physical measurement. |

*Note: All components matching handoff requirements now have appropriate through-hole (THT) footprints except J1, which awaits physical measurement verification to prevent unverified physical mismatches.*
