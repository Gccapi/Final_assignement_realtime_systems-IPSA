# Real-Time Scheduling Project - IPSA

## Project Overview
Analysis of a 7-task periodic system under non-preemptive scheduling.
- Task 1 (T1) WCET: Determined experimentally on hardware (WSL/Ubuntu).
- Optimization: Implementation of an optimized SJF with a 3s safety window.

## Hardware Measurement Results (T1)
- Min: 0.646354 s
- Q1 (25%): 0.656072 s
- Q2 (Médiane): 0.662474 s
- Q3 (75%): 0.669712 s
- Max (WCET mesuré): 0.925961 s
- WCET (+20%): 1.111153 s
- U: 0.7486
  
## Scheduling Performance
- EDF Waiting Time: 111.112s
- Optimized SJF Waiting Time: 101.112s
- Status: All deadlines met (including T5).
