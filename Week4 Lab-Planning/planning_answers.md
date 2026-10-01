# Laboratory – Logical Reasoning for Planning

## Task 0: Understand the Planning Problem
(a) **Initial state I**: `{At(Robot, A), At(Package, A)}`
(b) **Goal G**: `{At(Package, C)}`
(c) **Actions available**: `Move(X, Y)`, `PickUp(Package, X)`, `Drop(Package, X)`
(d) 
*   **Move(X, Y)**: Pre: `At(Robot, X)`, Eff: `At(Robot, Y)`, `¬At(Robot, X)`
*   **PickUp(Package, X)**: Pre: `At(Robot, X)`, `At(Package, X)`, Eff: `Holding(Package)`, `¬At(Package, X)`
*   **Drop(Package, X)**: Pre: `At(Robot, X)`, `Holding(Package)`, Eff: `At(Package, X)`, `¬Holding(Package)`

**Question**: Starting from `I`, is `PickUp(Package, A)` applicable? Yes, because both preconditions are in `I`. Is `Drop(Package, C)` applicable? No, because `At(Robot, C)` and `Holding(Package)` are absent.

## Task 1: Construct a Plan by Hand
| State | Facts |
| :--- | :--- |
| S0 | At(Robot, A), At(Package, A) |
| S1 | At(Robot, A), Holding(Package)  *(after PickUp(Package, A))* |
| S2 | At(Robot, B), Holding(Package)  *(after Move(A, B))* |
| S3 | At(Robot, C), Holding(Package)  *(after Move(B, C))* |
| S4 | At(Robot, C), At(Package, C)  *(after Drop(Package, C))* |

## Task 4: Logic and Search
**Question**: 
Current state
↓
Check action preconditions
↓
**Apply action effects (Logical Reasoning)**
↓
Generate successor state
↓
Search over alternatives
↓
Goal?

## Task 8: Connect Prolog to Logical Reasoning
**Explain why the query succeeds**: The fact `wet_road` is asserted. The rule `slippery :- wet_road` deduces that it is slippery. Finally, the rule `reduce_speed :- slippery` deduces `reduce_speed`. 
**Logical Sequence**: `wet_road ⇒ slippery ⇒ reduce_speed`.

## Reflection Questions
1.  **Why specify preconditions and effects?** To give the LLM a formal mathematical model of state transition, reducing ambiguity and preventing it from hallucinating invalid game rules.
2.  **Example of error?** The planner might have the robot pick up the package from across the warehouse without moving there first.
3.  **Why is a "reasonable" plan not necessarily valid?** A sequence might look human-readable but violate a strict logical dependency (e.g., dropping the package twice).
4.  **What did the LLM contribute?** It converted the set-theoretic logic into functional Python code (set unions/differences) and implemented BFS.
5.  **What did you verify independently?** The state transitions—whether the negative effects correctly removed propositions and positive effects added them.
6.  **Where is logical reasoning used?** In checking preconditions (`state ⊨ Pre`) and applying state effects.
7.  **How is planning related to search?** Planning is just graph search where the nodes are logical states and edges are the valid logical actions connecting them.
