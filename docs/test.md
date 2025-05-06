# Neptune Robotics **XR‑300** Exploration Drone: Maintenance & Troubleshooting Guide
_Last updated: 2025‑05‑01_

## Overview
The **XR‑300** is a lightweight, modular drone designed for subterranean and industrial inspection.  
Its AI‑assisted navigation allows fully autonomous missions in GPS‑denied environments.

---

## Key Specifications
| Parameter | Value |
|-----------|-------|
| **Weight** | 3.4 kg |
| **Max Flight Time** | 6 hours |
| **Operating Temperature** | −20 °C – 50 °C |
| **Communication** | 5 GHz Wi‑Fi / L‑band |
| **Firmware** | v1.2.3 |

---

## Installed Modules
- **ONS‑X** – Optical Navigation Suite  
- **LAR‑2** – LiDAR Array  
- **TIM‑1** – Thermal Imaging Module  

---

## Troubleshooting

### Error Code **N14** — IMU Calibration Failure
**Cause**  
The Inertial Measurement Unit (IMU) failed to converge within expected tolerance after boot.

**Fix**  
1. Place the XR‑300 on a perfectly level surface.  
2. Power‑cycle the drone.  
3. In the *Neptune Control* app, run `calibrate_imu`.  
4. If the error persists, replace the IMU harness (part **IMU‑HRN‑X3**).

---

### Error Code **B42** — Battery Thermal Runaway Risk
**Cause**  
Temperature sensors detected unstable thermal rise (> 70 °C) inside Battery Pack #1.

**Fix**  
1. Land the drone immediately and power it off.  
2. Allow the battery to cool below 25 °C.  
3. Inspect for physical swelling; replace the pack if damaged.  

---

## FAQ

> **Q 1:** How do I perform a *factory reset*?  
> **A:** Hold the **Power** and **Function** buttons simultaneously for **7 seconds** until the status LED turns magenta.

> **Q 2:** What is the recommended battery cycle count?  
> **A:** Replace the battery after **300 full cycles** (0–100 %).

---

## Changelog
- **2025‑03‑01** – Added obstacle‑avoidance module support.  
- **2025‑01‑15** – Initial public release.
