# April Peer Presentation Script

Target rate: 130 wpm
Estimated words: 2746
Estimated time: 21.1 minutes

## Slide 1. Exact Loop-Level Parallelization in Maple
Estimated words: 154
Estimated time: 71 seconds

This is a fresh April version of the talk. I am using Adam's presentation as the model for structure rather than content: start with context, introduce the representation, walk through the algorithm, then show evidence and limits. The content here is my Maple thesis work. The contribution is a command, IsParallelizable, that keeps Maple's existing loop-analysis front end but changes the final loop-level decision so it is based on integer feasibility instead of rational over-approximation alone. I would also say explicitly that this version is not trying to imitate Adam's topic. The useful thing from Adam is the discipline of explaining one technical object at a time. That means the audience should always know what role the current slide plays: representation, algorithm step, evidence, or limitation. I will frame this as a reset from the previous direction: the deck is now about the thesis contribution, presented with a cleaner peer-talk structure.

## Slide 2. The talk follows a technical walkthrough
Estimated words: 140
Estimated time: 65 seconds

The structure is deliberately close to Adam's rhythm. I first give the high-level setup, then the data representation, then the algorithmic walkthrough, and only then the performance-style evidence and limitations. The difference is the content. Instead of hypergraph transversals, the object here is dependence analysis for Maple loop nests and the exact question of which loop levels can be safely parallelized. This roadmap also sets expectations about depth. I am not going to race through every theorem and every implementation detail from the defense deck. Instead, I am choosing the same kind of paced technical story Adam used: enough background to make the algorithm meaningful, then one concrete path through the implementation, then evidence. I will use this slide to promise the audience a path through the talk, so they know each later technical slide has a specific job.

## Slide 3. The parallelization question is level-specific
Estimated words: 156
Estimated time: 72 seconds

The core issue is that loop parallelization is not just asking whether some dependence exists. It is asking whether a specific loop level is blocked by an actual pair of iterations. Maple already has the front half of the analysis: it can normalize a loop, describe the legal iteration space, and collect array references. The thesis adds the exact decision layer that asks whether a blocking witness exists in integer iteration space for the level under test. This distinction is important because a dependence summary can be true and still not answer the question a programmer cares about. The programmer wants to know whether a specific loop index can run in parallel. That makes the unit of analysis a loop level, not the entire nest and not the whole dependence cone. I will give a small verbal example here: two loop iterations can both exist, but only one level may be responsible for the ordering problem.

## Slide 4. Marc's dependence definition gives the test shape
Estimated words: 133
Estimated time: 61 seconds

Marc's formal dependence definition is the bridge into the algorithm. A data dependence needs same memory, at least one write, and a legal execution path. In the implementation, those become source legality, target legality, equal-access equations, and a condition that fixes where the first loop-index difference occurs. This is why the talk can stay technical without drifting into implementation detail too early. I should keep this slide connected to Marc's lecture language. The formal definition is not decoration. It tells us exactly what the generated constraint system has to encode. If any of same memory, one write, or legal ordering is missing, then the solver is answering the wrong question. I will say that this is why the implementation checks read-write, write-read, and write-write cases, rather than treating all pairs uniformly.

## Slide 5. Maple supplies the front half of the analysis
Estimated words: 136
Estimated time: 63 seconds

This is the representation slide in Adam's sense: what data structures are actually being passed around. Maple normalizes a procedure into a ForLoop object. From there, IterationSpace gives the affine legality conditions, and ArrayReferences gives the reads and writes. IsParallelizable is intentionally conservative about scope: it uses these existing objects and focuses on the final question of whether an integer blocking witness exists for each loop level. The reason to show the pipeline is to avoid making the thesis sound larger or vaguer than it is. Maple already has machinery for parsing and representing loop nests. The new work starts after that machinery has produced the objects needed to ask the exact loop-level question. I will pause on each pipeline box long enough to show that the command is reusing Maple's native analysis objects.

## Slide 6. The model is a two-iteration system
Estimated words: 152
Estimated time: 70 seconds

For one source-target reference pair and one loop level, the command builds a two-iteration system. One copy of the loop variables describes the source instance, another describes the target instance, and the constraints force both to be legal and to touch the same memory cell. The level-specific blocker then says that this is the first loop level where the target is ordered after the source in a way that prevents parallel execution. In the talk I would slow down here and make the two copies of the loop variables concrete. One copy is the earlier or source execution instance and one copy is the later or target execution instance. The equal-access constraints tie them together by forcing the two array subscripts to name the same cell. I will describe the two-iteration system as a witness search: if the witness exists, the level is blocked; otherwise it is not blocked by that pair.

## Slide 7. Decision rule for one loop level
Estimated words: 143
Estimated time: 66 seconds

This is the core algorithm in compact form. For each loop level, the command checks every relevant source-target access pair. It builds the legality constraints, the equal-access constraints, and the first-difference condition for the level. Then it asks a single yes-or-no question: does this system have an integer point? If yes, that loop level is blocked by a real execution witness. If no pair produces a witness, the level is reported safe. This pseudocode is the center of the talk. The nested loops over levels and reference pairs are deliberately simple. The complexity is hidden in building the correct system and in asking the backend over integers. That simplicity is useful because it makes the correctness argument easier to explain. I will walk through the pseudocode line by line, because this is the easiest place for the audience to verify the algorithmic shape.

## Slide 8. Reference pairs are filtered before solving
Estimated words: 146
Estimated time: 67 seconds

Before the backend query, the implementation keeps only access pairs that can create a dependence. A read-read pair is not a dependence because neither side writes. The command also keeps the claim inside the supported affine loop surface. That scope control matters for the talk: the result is not that every Maple program is now solved, but that this class of loop-level dependence decisions is handled exactly over integer iteration space. The filtering step also explains why the command is not just throwing every possible pair at a solver. It uses the dependence semantics first, then uses integer feasibility second. That order matters for performance and for clarity, because the backend query should only be asked for pairs that could actually change the answer. I will connect this filtering to both correctness and cost: it avoids irrelevant queries and keeps the evidence tied to dependence semantics.

## Slide 9. ZPolyhedralSets is the integer backend
Estimated words: 141
Estimated time: 65 seconds

Marc specifically asked for the role of ZPolyhedralSets, and this is the cleanest way to present it. Loop iterations are integer points. The blocker system is a system of affine constraints over those integer variables. So Maple builds a ZPolyhedralSet and asks whether any integer point remains. The command is not inventing a solver; it is connecting Maple's loop-analysis representation to the backend whose domain matches the question. This is where I would connect the command back to Maple rather than presenting ZPolyhedralSets as a separate mathematical tool. The backend is already in the ecosystem, and the thesis uses it because loop iterations are integer points. That makes the integration feel natural instead of bolted on. I will emphasize that the backend question is existence, not enumeration; the command only needs to know whether at least one integer point remains.

## Slide 10. DependenceCone is useful but rational
Estimated words: 138
Estimated time: 64 seconds

This is the main contrast. DependenceCone is useful, but its output is rational. That is appropriate for a cone summary, but it is not the same thing as proving that a real pair of integer loop iterations blocks a level. In the parity-style cases, the rational analysis can keep a fractional distance that cannot be an actual iteration distance. IsParallelizable resolves that final question by checking the integer system. The comparison should be respectful to DependenceCone. It is not wrong for doing its job. The point is that its job is a rational dependence summary, while IsParallelizable has a different job: a final safety decision for loop levels. The difference in domain is what creates the improvement. I will avoid making DependenceCone sound like a failed tool. It is the right baseline, but not the final safety oracle.

## Slide 11. The parity mechanism explains the improvement
Estimated words: 134
Estimated time: 62 seconds

The parity case is the simplest way to explain why the backend matters. A rational projection can preserve a distance like three halves. As a rational object, that is perfectly legal. As a loop distance between two integer iterations, it is impossible. When the integer feasibility query is empty, the command rejects the blocker. That is the strict improvement over treating the rational summary as the final answer. This mechanism is the cleanest explanation of the false-blocker issue. A fractional value can survive rational reasoning, but the loop program will never execute at a fractional iteration. Once the audience accepts that, the need for an integer backend becomes intuitive rather than merely formal. I will make the fractional-distance example slow and concrete, because it is the shortest route to the intuition behind the thesis.

## Slide 12. Worked example: heat_eq starts from Maple objects
Estimated words: 137
Estimated time: 63 seconds

For the worked example, the current defense deck uses heat_eq because it walks through the full pipeline. The point of the slide is not only the final safe loop variable. It is that Maple starts from the same ForLoop representation, extracts accesses, builds the pairwise systems, and then makes a separate decision for each loop level. That makes the implementation easier to defend because the example lines up with the algorithm. The example section should feel like Adam's algorithm walkthrough: we do not only state that the command works, we show how the input travels through the analysis. The audience sees the representation, the pairwise constraints, and the separate decisions, so the final output is earned. I will use heat_eq as the running example that turns the abstract constraint language into something visibly produced by Maple.

## Slide 13. The blocker is level-specific in heat_eq
Estimated words: 140
Estimated time: 65 seconds

The key teaching point in heat_eq is that loop levels must be tested separately. One level can be blocked because there is a real source-target pair that creates a dependence witness. Another level can be safe because no such integer witness exists under the first-difference condition for that level. This is why the command returns safe variables rather than only saying whether the loop nest has any dependence at all. I would emphasize that the same loop nest can produce different answers at different levels. That is the practical reason for returning safe variables. A single yes-or-no answer for the whole nest would lose useful information, especially when an inner level remains parallelizable after an outer level is blocked. I will stress that different levels can have different answers, which is why the command returns a set of safe variables.

## Slide 14. What IsParallelizable returns
Estimated words: 127
Estimated time: 59 seconds

The user-facing part is intentionally simple. The command accepts either a ForLoop or a procedure that Maple can normalize through CreateLoop. It returns the loop variables that are safe, ordered from outermost to innermost. The backend details are important for the defense, but the command surface is about the practical question a Maple user asks: which loop levels can I parallelize? This interface slide keeps the result concrete. It tells the audience what they would call, what kind of input is accepted, and how to read the output. The implementation can be mathematically detailed, but the command has to land as a usable Maple feature. I will keep the interface slide practical and avoid exposing more backend notation than a Maple user needs to use the command.

## Slide 15. Validation stays tied to the frozen bundle
Estimated words: 134
Estimated time: 62 seconds

The evidence slide needs to be careful. The current technical defense ties the claim to a frozen 23-case bundle and a dated pass rerun. Within that surface, there is no validated case where DependenceCone is less pessimistic than IsParallelizable, and there are strict-improvement cases where integer reasoning rejects a false rational blocker. That is the claim the April deck should make, without turning it into an unsupported universal theorem. The validation slide should be delivered with restraint. The right claim is strong but bounded: on the frozen evidence surface, the integer method preserves validated answers and exposes strict improvements over rational pessimism. I should avoid implying that untested program classes have already been handled. I will state the validation date and bundle idea as process evidence: this deck should be auditable, not just persuasive.

## Slide 16. The strict-improvement cases are the headline evidence
Estimated words: 125
Estimated time: 58 seconds

The evidence should be presented in two parts. First, agreement cases show that the command preserves standard answers and does not incorrectly remove real dependences. Second, the strict-improvement cases show where rational pessimism is too strong. This makes the result credible: the command is not simply more optimistic everywhere, it is more precise where the integer feasibility question rules out a false blocker. The important balance is that strict improvement is not just optimism. The agreement and control cases show that real dependences remain real dependences. The improvement cases matter because they are paired with that control surface, so the story is precision rather than wishful parallelization. I will say that strict improvement means fewer false blocks, not a willingness to ignore true dependence witnesses.

## Slide 17. Optimizations and precision have tradeoffs
Estimated words: 139
Estimated time: 64 seconds

Adam's talk included lessons about optimizations that did not always behave the same way across cases. The equivalent lesson here is about precision. Integer feasibility is the right semantic test for loop iterations, but the claim is still bounded by the supported affine surface and the validated examples. That boundary is not a weakness to hide. It is what keeps the technical claim defensible. This lesson slide mirrors Adam's habit of explaining what the experiments taught, not only what the algorithm does. Here the lesson is that exactness belongs at the semantic boundary where Maple decides safety. Earlier rational summaries are useful, but they should not be forced to answer an integer execution question. I will use this slide to show what I learned from the April reset: the narrative must make the exact decision layer obvious.

## Slide 18. Scope control keeps the claim defensible
Estimated words: 118
Estimated time: 54 seconds

This slide prevents overclaiming. Inside the deck are affine loops, Maple's ForLoop representation, array-reference constraints, and ZPolyhedralSets integer feasibility. Outside the deck are nonlinear indexing, arbitrary side effects, and performance or correctness claims that have not been validated. That lets the presentation be strong without being brittle. The limits should stay visible because they protect the contribution. It is better to say clearly that the current deck covers affine loop nests and validated examples than to imply a broader result. That gives reviewers a precise target for technical criticism and keeps the final thesis claim defensible. I will present the limits before questions, so scope concerns are answered by the deck itself rather than patched on afterward.

## Slide 19. Future work follows from the same architecture
Estimated words: 122
Estimated time: 56 seconds

The future work follows naturally from the architecture. The front end can stay Maple's loop representation, and the exact integer decision can be improved independently. The near-term direction is better validation, clearer diagnostics, and better traces for why a level is blocked. The longer-term direction is expanding the supported program surface and connecting the command more directly to parallelization workflows. The future-work slide should not introduce a new thesis. It should show that the current architecture has room to grow. Better diagnostics, broader examples, and more program shapes all build on the same separation between Maple's front-end representation and the exact integer decision layer. I will keep future work tied to the existing architecture instead of proposing disconnected research directions.

## Slide 20. Closing claim
Estimated words: 131
Estimated time: 60 seconds

The closing claim is deliberately compact. Maple already has useful dependence infrastructure. The thesis contribution is to turn that into an exact loop-level parallelization decision by asking the right integer feasibility question. For the April version, Adam's structure gives the talk a clear technical arc, but the content stays anchored in the current Maple technical defense and the frozen validation surface. The closing should return to the three-part story: Adam supplied the presentation structure, the Maple defense supplied the content, and this fresh repo keeps the April work isolated until review. The final import back into Maple should happen only after the deck is reviewed and explicitly approved. I will close by reminding the audience that the repo isolation is also part of the process: review first, Maple import later.
