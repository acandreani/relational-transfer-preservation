"""Regenerate the manuscript's Figure 2 and summarize the 30 saved comparisons."""
import csv
from itertools import product
from pathlib import Path

here = Path(__file__).resolve().parent
with (here / "table_s1.csv").open(newline="", encoding="utf-8") as stream:
    rows = list(csv.DictReader(stream))

keys = [(r["seed"], r["regime"], r["position"]) for r in rows]
expected = set(product(map(str, range(20261017, 20261022)), ("R0", "R1", "R2"), ("4", "8")))
if len(rows) != len(expected) or set(keys) != expected:
    raise ValueError("Expected one comparison per seed, regime and position.")

for arm in ("mlp", "transformer"):
    losses = lambda r: int(r[f"{arm}_strict_losses"]) > 0
    conflict = [r for r in rows if r["regime"] in {"R0", "R1"}]
    print(f"{arm}: strict losses in {sum(map(losses, conflict))}/{len(conflict)} conflict comparisons.")
    improved = sum(float(r[f"{arm}_mean_delta_nll"]) < 0 for r in rows)
    print(f"{arm}: lower mean NLL than distance-specific counts in {improved}/{len(rows)} comparisons.")

shown = sorted((r for r in rows if (r["regime"], r["position"]) == ("R0", "4")),
               key=lambda r: r["seed"])
entries = [f"{r['seed']}/{r['shared_drops']}/{r['mlp_strict_losses']}/"
           f"{r['transformer_strict_losses']}/{-0.72 - 0.54*i:.2f}" for i, r in enumerate(shown)]
template = r"""
\begin{tikzpicture}[x=1cm,y=1cm,font=\sffamily\footnotesize]
 \node[anchor=west,text=ink,font=\sffamily\small\bfseries] at (0,4.30) {A\quad One input, two possible mixtures (invented probabilities)};
 \node[anchor=west] at (0,3.65) {Read across each row};
 \node at (5.7,3.65) {Correct answer};
 \node at (8.1,3.65) {Rival};
 \node[anchor=west] at (9.25,3.65) {Does the correct answer lead?};
 \draw[black!30] (0,3.35)--(14.55,3.35);
 \foreach \y/\rowname/\gold/\other/\outcome in {
    3.02/Distance-specific source/60/30/Yes (reference),
    2.50/After mixing: example 1/45/35/Yes (lead preserved),
    1.98/After mixing: example 2/45/45/No (tie: strict loss)}{
   \node[anchor=west] at (0,\y) {\rowname};
   \node at (5.7,\y) {\gold\%};
   \node at (8.1,\y) {\other\%};
   \node[anchor=west] at (9.25,\y) {\outcome};
 }
 \draw[black!30] (0,1.55)--(14.55,1.55);
 \node[anchor=west,text=ink,font=\sffamily\small\bfseries] at (0,0.78) {B\quad Observed predictions on 5,760 inputs per training seed};
 \node[anchor=east] at (1.7,0) {Training seed};
 \node[anchor=east,align=right] at (5.0,0) {Probability fell\\under both gates};
 \node[anchor=west,text=ink] at (5.6,0) {MLP: strict losses};
 \node[anchor=west,text=accent] at (9.0,0) {Transformer: strict losses};
 \foreach \seed/\shared/\mlp/\lost/\y in {@ROWS@}{
   \ifnum\seed=20261019 \fill[ink!7] (-.1,\y-.23) rectangle (14.55,\y+.23); \fi
   \node[anchor=east] at (1.7,\y) {\seed};
   \node[anchor=east] at (5.0,\y) {\shared};
   \node[text=ink] at (7.1,\y) {\mlp};
   \fill[accent] (9.05,\y-.095) rectangle ({9.05+0.008*\lost},\y+.095);
   \node[anchor=west,text=accent] at ({9.13+0.008*\lost},\y) {\lost};
 }
\end{tikzpicture}
""".lstrip("\n")
Path("paired_gates.tikz").write_text(template.replace("@ROWS@", ",".join(entries)), encoding="utf-8")
