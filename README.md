---
title: Meta AI OpenEnv Smart Farm
emoji: 🚜
colorFrom: green
colorTo: yellow
sdk: docker
app_port: 7860
tags:
  - openenv
---

# SmartFarm OpenEnv
An agricultural simulation for precision irrigation agents.

## 1. Environment Overview
This environment simulates soil moisture dynamics. Agents must balance water usage against crop health.

## 2. Specification
- **Action Space:** `water_volume` (float 0.0-1.0), `fertilizer_type` (int).
- **Observation Space:** `soil_moisture`, `crop_health`, `is_dead`.

## 3. Tasks
1. **Survival (Easy):** Keep plant alive for 15 days.
2. **Efficiency (Medium):** Maintain 0.7 moisture with minimal water.
3. **Drought (Hard):** Survive 30 days with high evaporation.

## 4. How to Run
Build: `docker build -t smartfarm .`
Run: `docker run -p 7860:7860 smartfarm`