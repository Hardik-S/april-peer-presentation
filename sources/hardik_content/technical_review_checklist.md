# Technical Review Checklist

## Marc Coverage

- Formal definitions of dependence: covered on Slides 3 to 5, including I(S_i), O(S_i), anti-dependence, true or flow dependence, output dependence, execution path, and the loop-dependence theorem from Marc's lecture deck.
- How to solve which levels are parallelizable technically: covered on Slides 7 to 10 via the exact level-l blocking theorem, constraint families, and per-level quantifier structure.
- Presentation of the ZPolyhedralSets package and backend role: covered on Slides 11 to 18 and tied to the pseudocode backend call.
- Algorithm behind IsParallelizable in pseudocode form: covered on Slides 16 to 18.
- Full worked example for one ForLoop nest: covered on Slides 19 to 24 with heat_eq.
- Bucket C examples where DependenceCone is conservative and IsParallelizable is correct: covered on Slides 25 to 27.
- Control example showing preservation of true blockers: covered on Slides 28 and 29.

## Verification

- Definition slides must stay aligned with Marc's lecture PDF and not paraphrase beyond the concepts explicitly used there.
- Pseudocode slides must not claim branch-condition handling or nonlinear index support.
- heat_eq slides must match the expected outputs in `Maple-main/CodeTools/ProgramAnalysis/tst/is_parallelizable.tst` and the comparison harness.
- Bucket C slides must match the expected outputs in `Maple-main/CodeTools/ProgramAnalysis/tst/is_parallelizable.tst` and the frozen March 17 bundle.
- Evidence slide must stay tied to the frozen 23-case bundle and dated PASS rerun.
- Script timing target is a full technical defense rather than the old short summary format.