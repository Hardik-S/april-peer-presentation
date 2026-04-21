# Technical Content Map

Archived style source: `C:\Users\hshre\OneDrive\Documents\42 - Agents\Codex\Maple\old\Slide deck.pptx`
Target deck: `C:\Users\hshre\OneDrive\Documents\42 - Agents\Codex\Maple\submit\Defense\technical_defense_deck_clean.pptx`

## Slide Purpose

- Definitions and theorem: Slides 3 to 10 mirror Marc's lecture framing and then formalize the exact level-l blocking theorem, the constraint families, and the level-by-level decision rule.
- Baseline pipeline: Slides 11 to 15 keep the front-end pipeline, the baseline rational gap, and the public Maple interface visible before the pseudocode section.
- Pseudocode and backend: Slides 16 to 18 replace source excerpts with mathematically faithful pseudocode and keep the ZPolyhedralSets backend call explicit.
- Worked example: Slides 19 to 24 run heat_eq end to end: loop nest, ForLoop data, access pairs, witness constraints, outer-level blocking, inner-level safety, and interpretation of the two Maple outputs.
- Strict improvement and control: Slides 25 to 29 reposition DependenceCone as a rational baseline, compare three Bucket C cases, explain the fractional-witness mechanism, and preserve a blocked wavefront control example.
- Evidence boundary: Slides 30 to 33 tie the talk to the frozen 23-case bundle, state the observed dominance property, and keep the claim inside an explicit scope boundary.

## Primary Sources Used

- `C:\Users\hshre\Downloads\Dependence_Analysis_and_Parallelization.pdf` for the formal dependence-definition structure used on Slides 3 to 5: data dependence, I(S_i)/O(S_i), anti-dependence, true or flow dependence, output dependence, execution path, and the loop-dependence theorem.
- `meeting/Marc Meeting #6_original.txt` for the framing that dependence detection is solved through systems of linear inequalities and that ZPolyhedralSets is the relevant Maple backend.
- `Maple-main/CodeTools/ProgramAnalysis/src/IsParallelizable.mm` for the actual algorithm and implementation details.
- `Maple-main/CodeTools/ProgramAnalysis/tst/is_parallelizable.tst` for running examples and expected Maple outputs.
- `Maple-main/help/mw+tst/PolyhedralSets-ZPolyhedralSets_help.mw` for the package-level presentation of integer-point decomposition over Z-polyhedral sets.

## Notes

- The formal-definition section remains anchored to Marc Moreno Maza's local lecture PDF rather than reconstructed only from meeting notes.
- Presentation slides now use pseudocode instead of Maple source-code excerpts.
- The middle of the deck is now organized around a full heat_eq walkthrough rather than a brief example summary.
- The old deck was archived first and is used only as visual-style reference.