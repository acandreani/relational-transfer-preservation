# Supplement S1. Which correct answers did the gates preserve?

Each row of `table_s1.csv` describes one comparison of two gates with the **same reference**: the predictor using only distance-specific counts (A-only). The 30 rows cross five fixed training seeds with three frequency regimes and two carrier positions. Rows reuse the same panel; they are not independent replications.

| Column | Meaning |
| --- | --- |
| seed | Training seed shared by the comparison; the architectures have different initial weights. |
| regime | R0: original conflict between evidence sources; R1: weaker conflict; R2: agreement. Only R0 and R1 enter the 20 conflict comparisons. |
| position | Carrier position, expressed as lag (4 or 8) from the answer. |
| contexts | Number of test inputs at this position in this comparison. |
| mlp_drops, transformer_drops | Inputs on which the indicated gate raised target negative log-likelihood (NLL) by more than 1e-10 relative to A-only. |
| shared_drops | Inputs counted as probability drops for **both** gates, matched by context ID. |
| mlp_strict_losses, transformer_strict_losses | Inputs on which A-only had a log-probability margin above 1e-12 over the other candidate and the indicated gate did not. This includes ties within tolerance; it is not a full-vocabulary top-1 error count. |
| mlp_mean_delta_nll, transformer_mean_delta_nll | Mean NLL of the indicated gate minus that of A-only, weighting contexts equally. NLL uses the normalized full vocabulary; a negative difference favors the gate. |

**Reproduce the figure and counts.** Place `reproduce.py` and `table_s1.csv` together and run `python3 reproduce.py` in a writable directory (Python 3.7+, standard library only). The script prints the number of conflict comparisons with at least one strict loss for each gate, checks the direction of each mean NLL difference, and regenerates `paired_gates.tikz`, the graphic included in the manuscript. In the article source package, compare the generated graphic with `figures/paired_gates.tex`; the article includes it without running Python. Figure 2A uses invented probabilities to explain the two outcomes. Figure 2B uses all five R0 rows at position 4; the abstract counts **rows with at least one loss** across both conflict regimes and positions, not individual losses pooled across rows.

**Source.** Column values are taken from the independently checked, reconstructed E5 report for the known-panel gate comparison, `saved_report_recovery_01/REPORT.json` (SHA-256: `642e71da42989a8d0b169d715add615570bb6a328c23d5678a4725a6ddf19b9a`). Its keys are seed/regime/position. For each key, the source fields are `contexts`, `A-only.{L,T}.nll_increases`, `A-only.all_overlap.both`, `A-only.{L,T}.strict_losses`, and `A-only.{L,T}.mean_delta_NLL`; L denotes the MLP. The supplement reproduces the reported summaries, not training or individual predictions.
