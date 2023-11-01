**EXPERIMENTAL RESULTS: OUR METHOD VS BASELINE/BENCHMARK**

Experiments with different distances comparing against the BASELINE (random_tweaking) and the BENCHMARK (steepest_ascent). Each tuple has the following format: (*#fitness_calls*, *cost*, *#steps*, *#steps_with_no_improvements_to_stop*), along with [*comparison_with_baseline*]. For each configuration, all the elements have been covered.

| Size | P       | BASELINE              | BENCHMARK                      | OURS (w/euclidean)             | OURS (w/cosine)                 | OURS (w/manhattan)             |
|:----:|:-------:|----------------------:|-------------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|
| 100  | 0.3     | (1150, -9, 15, 1000)  | ($\infty$, -6, 5, $\infty$)    | (200, -6, 5, 50) [**x5.8**]    | (180, -6, 6, 50) [**x6.4**]     | (170, -6, 6, 40) [**x6.8**]    |
| 1000 | 0.3     | (2470, -14, 20, 2000) | ($\infty$, -12, 31, $\infty$)  | (443, -13, 12, 50) [**x5.6**]  | (380, -12, 12, 50) [**x6.5**]   | (246, -11, 11, 50) [**x10.0**] |
| 5000 | 0.3     | (6500, -18, 25, 4000) | ($\infty$, -13, 99, $\infty$)  | (910, -16, 15, 100) [**x7.1**] | (448, -15, 15, 100) [**x14.5**] | (336, -16, 16, 50) [**x19.3**] |
| 100  | 0.7     | (150, -3, 6, 100)     | ($\infty$, -3, 3, $\infty$)    | (36, -3, 3, 15) [**x4.2**]     | (20, -3, 3, 10) [**x7.5**]      | (16, -3, 3, 5) [**x9.4**]      |
| 1000 | 0.7     | (400, -5, 6, 350)     | ($\infty$, -4, 4, $\infty$)    | (111, -4, 4, 50) [**x3.6**]    | (66, -5, 5, 20) [**x6.1**]      | (75, -4, 4, 40) [**x5.3**]     |
| 5000 | 0.7     | (1010, -7, 7, 1000)   | ($\infty$, -5, 5, $\infty$)    | (125, -6, 8, 50) [**x8.1**]    | (64, -6, 6, 20) [**x15.8**]     | (68, -6, 6, 40) [**x14.9**]    |

---

**EXPERIMENTAL RESULTS: OUR BEST RESULT VS CANDIDATES PRUNING**

Experiments testing the effectivness of candidates pruning. Each tuple in the modified version has the following format: (*#fitness_calls*, *cost*, *#steps*, *#steps_with_no_improvements_to_stop*, *ratio*), along with [*comparison_with_baseline*]. For each configuration, all the elements have been covered.


| Size | Density | OURS (w/manhattan)             | OURS (w/manhattan + candidates pruning) |
|:----:|:-------:|-------------------------------:|----------------------------------------:|
| 100  | 0.3     | (170, -6, 6, 40) [**x6.8**]    | (110, -6, 6, 40, 0.50) [**x10.5**]      |
| 1000 | 0.3     | (246, -11, 11, 50) [**x10.0**] | (205, -12, 12, 50, 0.75) [**x12.0**]    |
| 5000 | 0.3     | (336, -16, 16, 50) [**x19.3**] | (278, -16, 16, 60, 0.75) [**x23.4**]    |
| 100  | 0.7     | (16, -3, 3, 5) [**x9.4**]      | (13, -3, 3, 5, 0.75) [**x11.5**]        |
| 1000 | 0.7     | (75, -4, 4, 40) [**x5.3**]     | (22, -5, 5, 5, 0.25) [**x18.2**]        |
| 5000 | 0.7     | (68, -6, 6, 40) [**x14.9**]    | (26, -6, 6, 5, 0.50) [**x38.8**]        |
