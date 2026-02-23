---
title: appa
description: >
  Open-source C++ chassis movement library for VEX robots. Odometry, PID control,
  pure pursuit, and boomerang navigation with a composable options API.
order: 3
thumbnail: photos/appa.svg
thumbnail_alt: appa
thumbnail_class: contain
---

Appa is a C++ library for autonomous robot control on VEX robots using the [PROS](https://pros.cs.purdue.edu) framework. It abstracts odometry, PID control, and path following into a clean API so teams can focus on strategy rather than low-level motion code.

## What it does

The library handles localization and movement for a differential drive chassis. Tracking runs asynchronously in the background using either two encoder wheels + IMU, or three encoder wheels. On top of that, it exposes movement commands:

- Relative and absolute distance moves
- Point-to-point navigation
- Pose-based movement via a boomerang controller
- Pure pursuit path following for smooth curves
- Heading and point-facing turns

## Options system

Movement parameters (speed, acceleration, PID gains, exit tolerances) are configured through composable options objects rather than long argument lists. Presets can be defined once and combined inline:

```cpp
chassis.move(24, FAST | PRECISE);
chassis.turn(90, SLOW);
```

## Extensibility

Custom localization and tracking systems can be dropped in by subclassing the abstract `Localization` and `Tracker` base classes. Only a `get()` method returning pose deltas is required.

## Install

```
pros c add-depot appa https://appa.odom.tech/appa.json
```
