---
title: Manufacturing Automation & Analysis Tools
description: Software tools and automation systems built for vehicle inspection and test equipment at Subaru of Indiana Automotive.
order: 1
thumbnail: work/subaru.png
thumbnail_alt: subaru
thumbnail_class: contain
---
At Subaru, I work on the automated inspection and test equipment that evaluates every vehicle after it leaves the assembly line. This includes systems for headlight aim, wheel alignment, thermal inspection, and exterior light verification. Alongside maintaining and improving these systems, I've built several software tools to make the equipment easier to monitor, analyze, and improve.

## Inspection Dashboard

I built a web application that gives engineers visibility into how the automated inspection equipment is performing across the entire tester line. The backend is written in Python, pulling data from SQL databases and processing requests for filtered views and generated graphs.

The main page shows every piece of equipment on the line with failure counts and percentages over a configurable time window. Individual equipment pages go deeper with detailed breakdowns and time-series graphs for spotting trends, identifying recurring failures, and tracking the impact of changes. There are also investigation tools like vehicle-specific reports that pull all test data for a single unit, and an embedded calculator for adjusting equipment settings.

The goal was to replace the previous approach of manually querying databases and building spreadsheets every time someone wanted to understand what was happening on the line. Now engineers can get answers in seconds instead of hours.

## PLC Communication & Automation

I write Python scripts that communicate with multiple Mitsubishi Q-series PLCs over Ethernet using the SLMP protocol. One system reads from four PLCs simultaneously to detect when a new vehicle arrives at a station, looks up the vehicle's configuration from a table based on its control number, determines the correct number of bumper clips for that model, and sends the result back to the PLC so it can be displayed to associates on the line.

I also write and modify the PLC programs themselves in GX Works, adding features and improving logic for the inspection equipment.

## Statistical Process Control

I developed statistical models to better control headlight aiming and wheel alignment equipment. For headlight aim, I built an EWMA-based control system that predicts equipment drift from noisy measurement data and automatically calculates precise setting adjustments, replacing the previous reactive method of guess-and-check corrections.

For wheel alignment, I investigated station-to-station measurement differences using a two-way unbalanced OLS regression model built entirely in Excel with LINEST and dummy variable encoding. This analysis identified that calibration methods which zero out on a jig don't reliably transfer to wheeled vehicles across stations, a finding that changed how the team approaches calibration and alignment verification.