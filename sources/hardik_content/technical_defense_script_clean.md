# Thesis Presentation Script

Target rate: 130 wpm
Estimated core words: 1817
Estimated core time: 839 seconds

## Slide 1. Dependence Analysis of For-Loop Nests in Maple
Estimated words: 49
Estimated time: 23 seconds

This talk is now a technical defense rather than a short supervisor summary. The contribution is a Maple command called IsParallelizable. It reuses Maple's existing loop-analysis front end and changes the final decision step so loop-level parallelization is decided by integer feasibility rather than by rational over-approximation alone.

## Slide 2. Technical structure of the defense
Estimated words: 60
Estimated time: 28 seconds

I will keep the defense technical. First I will give the formal dependence language and the exact constraint system we need to solve. Second I will show how that system is built inside Maple and why ZPolyhedralSets is the correct backend. Third I will show the actual command, the algorithm in the source, and running examples from the validated bundle.

## Slide 3. Marc's formal definition of data dependence
Estimated words: 69
Estimated time: 32 seconds

Marc asked for the formal dependence definitions from his slides, so I start with them directly. A data dependence needs three ingredients: the same memory location, at least one write, and an execution path from the earlier statement to the later one. I also want the lecture notation on the screen, because the next slide uses the I of S and O of S sets exactly as he does.

## Slide 4. Dependence taxonomy used in Marc's slides
Estimated words: 40
Estimated time: 18 seconds

This is the exact taxonomy from Marc's lecture deck. I want it visible because Maple's command checks every relevant pair where at least one side is a write, which is exactly the common structure behind these three classes.

## Slide 5. From statement dependence to loop-level blocking
Estimated words: 63
Estimated time: 29 seconds

Marc's next move in the lecture is the loop dependence theorem, and that is the bridge I need here. Once dependence is phrased as the existence of two legal index vectors that hit the same location with one write, Maple can specialize the question to one loop level by forcing the first difference to occur exactly where that level would be blocked.

## Slide 6. Maple already supplies the front half of the analysis
Estimated words: 46
Estimated time: 21 seconds

The thesis does not replace Maple's front end. A procedure is normalized by CreateLoop into a ForLoop object. IterationSpace gives the affine legality conditions, ArrayReferences gives the memory accesses that matter, and DependenceCone gives a rational summary. The missing piece was the final loop-level decision.

## Slide 7. Legality plus same-memory equations
Estimated words: 52
Estimated time: 24 seconds

The meeting notes say this directly: dependencies can be computed by solving systems of linear inequalities. In our setting, one system combines source legality, target legality, equal-access constraints, and the lexicographic blocker for the loop level under test. That is why the mathematics is part of the core argument, not extra ornament.

## Slide 8. The level-l blocker and the resulting system
Estimated words: 39
Estimated time: 18 seconds

This is the exact system shape. For one source-target reference pair and one loop level, the blocker adds the first-difference condition on top of legality and same-memory constraints. That produces one candidate witness set for the level under test.

## Slide 9. Constraint families for one pair and one loop level
Estimated words: 36
Estimated time: 17 seconds

Here are the constraint families in compact form. Once initialization has been applied, the system is affine in the loop variables and the distance variables. That is the structure Maple eventually hands to the integer backend.

## Slide 10. The exact decision rule
Estimated words: 53
Estimated time: 24 seconds

This is the exact criterion. For one source-target reference pair and one loop level, I build a two-iteration system and ask whether it has an integer solution. If it does, that level is blocked by a real execution witness. If it does not, then this pair does not prevent parallelization at that level.

## Slide 11. What ZPolyhedralSets represents
Estimated words: 61
Estimated time: 28 seconds

Marc also asked for a presentation of the ZPolyhedralSets package. The key point is modest but essential: it is already Maple's library for integer points of polyhedral sets. That is exactly the semantic domain of loop iterations, so the thesis does not invent a new solver. It wires Maple's loop analysis to the solver that already matches the problem.

## Slide 12. How the algorithm calls ZPolyhedralSets
Estimated words: 35
Estimated time: 16 seconds

This is the concrete call pattern the implementation uses. Maple builds a ZPolyhedralSet from the normalized constraints and then asks IntegerPointDecomposition whether any integer points remain. That is the exact backend handoff in the code.

## Slide 13. DependenceCone is a rational over-approximation
Estimated words: 57
Estimated time: 26 seconds

This is the exact research gap. DependenceCone is useful, but it is a rational summary rather than a final oracle for loop-level safety. In the parity case the cone reports d equals three halves, which is legal in rational space but impossible as an actual iteration distance. That is enough to motivate a separate integer decision layer.

## Slide 14. IsParallelizable at one loop level
Estimated words: 51
Estimated time: 24 seconds

Marc asked what the algorithm behind IsParallelizable actually is. This is the high-level answer. The command normalizes the input, applies initialization, selects only the reference pairs that can matter for dependence, then for each loop level builds the exact two-iteration integer system and asks ZPolyhedralSets whether it has any integer point.

## Slide 15. Public Maple interface
Estimated words: 49
Estimated time: 23 seconds

The implementation result is a public Maple command, not a worksheet-only experiment. It accepts either a ForLoop or a procedure that CreateLoop can normalize, and it returns the safe loop variables from outermost to innermost. The code keeps Maple's existing representation and changes only the final decision backend.

## Slide 16. Pseudocode: top-level IsParallelizable workflow
Estimated words: 52
Estimated time: 24 seconds

This pseudocode gives the top-level control flow. The input is normalized to a ForLoop, initialization is applied to the legality surface, relevant same-array pairs are collected, and each loop level is tested separately. A loop variable is returned only if the search fails to find any blocking integer witness at that level.

## Slide 17. Pseudocode: pair-level blocking test
Estimated words: 51
Estimated time: 24 seconds

This pseudocode is the technical core. For one source-target pair and one level, Maple constructs a two-iteration system with legality, equal-access constraints, and the first-difference blocker. The pair blocks the level if and only if that system has an integer point. This is the implementation-level realization of the theorem stated earlier.

## Slide 18. Pseudocode: backend call into ZPolyhedralSets
Estimated words: 46
Estimated time: 21 seconds

This is the final backend handoff expressed as pseudocode. Maple normalizes the affine relations, constructs a ZPolyhedralSet over loop and distance variables, and invokes IntegerPointDecomposition. The implementation interprets a nonempty result as existence of a real blocking witness, which is exactly the semantic test we need.

## Slide 19. Worked example anchor: the heat equation loop nest
Estimated words: 55
Estimated time: 25 seconds

I now switch from the generic algorithm to one complete loop nest. heat_eq is the right anchor because it is a real two-dimensional dependence pattern with a nontrivial answer: the outer level is blocked while the inner level is safe. That lets the rest of the talk show the entire decision pipeline end to end.

## Slide 20. heat_eq after CreateLoop: ForLoop data and relevant accesses
Estimated words: 71
Estimated time: 33 seconds

After CreateLoop, Maple has a ForLoop object with variables i and j and the iteration-space relations 1 less than or equal to i less than or equal to m and 1 less than or equal to j less than or equal to n. ArrayReferences exposes one write A[i, j] and three relevant reads on the same array. Those are the exact program objects from which the witness systems are built.

## Slide 21. heat_eq witness system before choosing a loop level
Estimated words: 63
Estimated time: 29 seconds

This slide shows the raw witness construction for one read/write pair. Both source and target iterations must satisfy the legality surface, and equal-access equations force the two references to hit the same cell. For the southwest read against the write, the equal-access equations immediately imply a concrete distance candidate. The remaining issue is whether that candidate blocks level i or level j.

## Slide 22. Testing the outer level in heat_eq
Estimated words: 71
Estimated time: 33 seconds

Now I test the outer level. For level i, the blocker is simply di greater than or equal to 1. Maple checks both read-to-write and write-to-read orientations, so a genuine forward dependence witness appears for the north-neighbor access pattern. Because such an integer witness exists, the outer level is blocked. The important point is that the conclusion comes from the formal witness condition, not from a verbal appeal to stencil intuition.

## Slide 23. Testing the inner level in heat_eq
Estimated words: 68
Estimated time: 31 seconds

Now I test the inner level. For j to be blocked, Maple would need an integer witness with di equal to 0 and dj greater than or equal to 1. But every genuine dependence in heat_eq moves through the outer dimension first, so every candidate pair violates di equal to 0. Hence all pair-level systems are integer-empty for level j, and the inner loop is returned as safe.

## Slide 24. Interpreting Maple's two answers on heat_eq
Estimated words: 64
Estimated time: 30 seconds

This slide closes the worked example by putting the two Maple outputs side by side. DependenceCone gives a rational distance summary, here di equal to 1 with dj between minus 1 and 1. That is informative, but it does not itself answer which loop levels are safe. IsParallelizable adds the level-specific integer witness test and therefore resolves the actual parallelization question as j only.

## Slide 25. DependenceCone is a rational baseline, not the final oracle
Estimated words: 60
Estimated time: 28 seconds

After the heat-equation walkthrough, I can now isolate the research gap cleanly. DependenceCone is not wrong; it is a rational over-approximation baseline. In parity_case, it reports d equals three halves, which is a perfectly valid rational summary but not a realizable integer iteration distance. So it stops short of the final question, and IsParallelizable supplies the missing integer decision layer.

## Slide 26. Bucket C examples: conservative cone, correct integer answer
Estimated words: 58
Estimated time: 27 seconds

This table makes the strict-improvement section comparative rather than anecdotal. parity_case is the canonical one-dimensional example, frac2d_case shows the same failure mode inside a true loop nest, and stride3_frac_case shows that the issue is about integrality more generally, not about one specific stride pattern. In each case, the cone is conservative while the integer witness set is empty.

## Slide 27. Why Bucket C fails in rational space but succeeds over Z
Estimated words: 62
Estimated time: 29 seconds

This slide explains the mechanism rather than merely listing examples. Rational projection can preserve a fractional distance vector that satisfies the relaxed system over the rationals. But the final loop-level question is whether any integer iteration pair realizes that same system. When the lattice intersection is empty, the rational blocker is an artifact of over-approximation, and the integer test correctly rejects it.

## Slide 28. Control example: wavefront recurrence remains blocked
Estimated words: 56
Estimated time: 26 seconds

A control example is essential after Bucket C. In the wavefront case, there are genuine integer witnesses, so the algorithm returns the empty safe set. This shows that the backend change is not simply a mechanism for allowing more loops. It is a mechanism for distinguishing real blockers from rational artifacts while preserving standard blocked answers.

## Slide 29. What the control example proves
Estimated words: 57
Estimated time: 26 seconds

This is the methodological point of the control example. A convincing decision procedure cannot only show where it says yes more often. It must also show that it still says no when real blockers exist. So the talk pairs Bucket C with a wavefront control specifically to establish both strict improvement and preservation of expected negative answers.

## Slide 30. Validated evidence boundary
Estimated words: 49
Estimated time: 23 seconds

The claim I defend is intentionally narrow and reproducible. The frozen bundle contains twenty-three pinned cases, and the April second rerun confirms that the canonical artifacts still pass. Broader regression and literature-backed cases support the engineering story, but they do not enlarge the formal claim beyond the frozen surface.

## Slide 31. Dominance statement over the frozen bundle
Estimated words: 59
Estimated time: 27 seconds

This slide states the strongest evidence-backed comparative claim. Across the frozen bundle, there is no validated case where DependenceCone is less pessimistic than IsParallelizable. Bucket A and Bucket B agree, and Bucket C shows strict pessimism only in the rational baseline. I keep that claim bounded to the defended frozen surface rather than overselling it as a universal theorem.

## Slide 32. Current decision boundary is explicit
Estimated words: 57
Estimated time: 26 seconds

The scope boundary matters in a technical defense. Branch conditions are not yet modeled, relevant array subscripts must stay linear after initialization, and the analysis still depends on the top-level access surface exposed by ArrayReferences. The validated claim is therefore the frozen bundle and its rerun, not a claim about every benchmark family Maple might eventually analyze.

## Slide 33. Technical conclusion
Estimated words: 58
Estimated time: 27 seconds

The technical conclusion is precise. Maple's existing loop-analysis front end was already strong enough. The missing piece was the final decision rule. By replacing rational over-approximation at the last step with integer emptiness, Maple can now answer which loop levels are actually safe to parallelize, and the frozen evidence bundle validates that claim inside an explicit boundary.
