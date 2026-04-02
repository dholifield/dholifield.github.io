---
title: Ergonomic Split Keyboard
description: "Designed a custom split keyboard end-to-end: PCB layout, firmware, and enclosure, optimized for ergonomics and minimal component count with a reversible PCB."
order: 2
thumbnail: projects/photos/kb-326.jpg
thumbnail_alt: Ergonomic Split Keyboard
---
A custom split mechanical keyboard, [split42](https://github.com/dholifield/split42), designed from scratch, from identifying the problem through PCB design, firmware, and planning for manufacturing. The goal was a compact, ergonomic keyboard with minimal component count and no compromises on feel.

![kb](photography/kb.jpg)

## Iterations

The project started out with a hand-wire protoype to test the layout and validate the ergonomics of a column stagger before committing to a custom PCB. This version was rough but functional, and confirmed that the split layout and key positioning felt right with some minor tweaks.

![prototype](projects/photos/proto.jpg)
![prototype back](projects/photos/proto_back.jpg)

From there I designed and fabricated the first PCB revision, which is what I'm using to type this right now. This version introduced the reversible PCB design described below.

The next revision is currently in progress with some major improvements: row concavity to follow natural finger motion, adjustable column positions for infinite user customization, and a modular design that allows adding and removing columns to fit users needs.

![next revision](projects/photos/new_kb.png)

## PCB Design

Designed the schematic and board layout in KiCad. The key constraint was a reversible PCB: a single board that works for both the left and right halves of the split, cutting fabrication cost and complexity in half.

![kb schemaic](projects/photos/pcb_schem.png)

![pcb](projects/photos/pcb_kicad.png)

Making the reversible design work required solving a few problems. The key switches have an asymmetric footprint, so I added extra through-holes to allow the switch to be installed in either orientation. One PCB layer is dedicated almost entirely to ground which simplified connecting the extra holes.

The I2C expander's (PCA9505) slim package meant it could be mounted facing the enclosure without issue. The microcontroller only lives on one half, so that mounting location was left empty on the other side.

The final piece was addressing. I added solder bridge pads that connect one of the expander's address pins either to power or ground. By bridging differently on each half, each expander gets a unique I2C address, allowing the firmware to distinguish left from right over the same bus.

## Firmware

The keyboard uses KMK firmware running on a Seeed RP2040 with CircuitPython. While KMK handles the mapping and HID layer, I wrote a custom key scanner tha interfaces with the I2C expanders. Rather than polling on a fixed interval, the scanner uses interrupt pins from the exapnders to detect state changes which is relay over to KMK. This reduces bus traffic and improves responsiveness.

## Process

The project followed a full product development cycle: identifying pain points with existing keyboards, iterative prototyping and testing, gathering feedback, and designing with manufacturing scalability in mind. The reversible PCB, minimal component count, and use of common parts were all deliberate choices to keep the design simple to assemble and cost-effective to produce.