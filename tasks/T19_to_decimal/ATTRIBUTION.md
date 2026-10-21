# Attribution

This task is original work created for this experiment. It does not adapt code from an external benchmark.

The package converts amounts to exact decimals, rounds to cents and units, sums and averages amounts, applies percentages and renders money text. The injected defect converts floats through their binary approximation, so half-cent values round downwards while text inputs remain exact.
