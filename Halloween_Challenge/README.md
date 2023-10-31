**EXPERIMENTAL RESULTS: OUR METHOD VS BASELINE/BENCHMARK**

Experiments with different distances. Each tuple has the following format: (*#fitness_calls*, *cost*, *#steps*, *#steps_with_no_improvements_to_stop*). For each configuration, all the elements have been covered.

| Size | Density | BASELINE              | STEEPEST_ASCENT                | OURS (w/euclidean)  | OURS (w/cosine)     | OURS (w/manhattan) |
|:----:|:-------:|:----------------------|:-------------------------------|:--------------------|:--------------------|:-------------------|
| 100  | 0.3     | (1150, -9, 15, 1000)  | ($\infty$, -6, 5, $\infty$)    | (200, -6, 5, 50)    | (180, -6, 6, 50)    | (170, -6, 6, 40)   |
| 1000 | 0.3     | (2470, -14, 20, 2000) | ($\infty$, -12, 31, $\infty$)  | (443, -13, 12, 50)  | (380, -12, 12, 50)  | (246, -11, 11, 50) |
| 5000 | 0.3     | (6500, -18, 25, 4000) | ($\infty$, -13, 102, $\infty$) | (910, -16, 15, 100) | (448, -15, 15, 100) | (336, -16, 16, 50) |
| 100  | 0.7     | (150, -3, 6, 100)     | ($\infty$, -3, 3, $\infty$)    | (36, -3, 3, 15)     | (20, -3, 3, 10)     | (16, -3, 3, 5)     |
| 1000 | 0.7     | (400, -5, 6, 350)     | ($\infty$, -4, 4, $\infty$)    | (111, -4, 4, 50)    | (66, -5, 5, 20)     | (75, -4, 4, 40)    |
| 5000 | 0.7     | (1010, -7, 7, 1000)   | ($\infty$, -5, 5, $\infty$)    | (125, -6, 8, 50)    | (64, -6, 6, 20)     | (68, -6, 6, 40)    |

---

**EXPERIMENTAL RESULTS: OUR BEST RESULT VS CANDIDATES PRUNING**

Experiments testing the effectivness of candidates pruning. Each tuple in the modified version has the following format: (*#fitness_calls*, *cost*, *#steps*, *#steps_with_no_improvements_to_stop*, *ratio*). For each configuration, all the elements have been covered.


| Size | Density | OURS (w/manhattan) | OURS (w/manhattan + candidates pruning) |
|:----:|:-------:|:-------------------|:----------------------------------------|
| 100  | 0.3     | (170, -6, 6, 40)   | (110, -6, 6, 40, 0.50)                  |
| 1000 | 0.3     | (246, -11, 11, 50) | (205, -12, 12, 50, 0.75)                |
| 5000 | 0.3     | (336, -16, 16, 50) | (278, -16, 16, 60, 0.75)                |
| 100  | 0.7     | (16, -3, 3, 5)     | (13, -3, 3, 5, 0.75)                    |
| 1000 | 0.7     | (75, -4, 4, 40)    | (22, -5, 5, 5, 0.25)                    |
| 5000 | 0.7     | (68, -6, 6, 40)    | (26, -6, 6, 5, 0.50)                    |
