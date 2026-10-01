# Laboratory Exercise – Search and A*

## Task 0: Understand the Search Problem
*   **State S:** The grid coordinates `(x, y)` of the robot.
*   **Actions A:** `Up`, `Down`, `Left`, `Right`.
*   **Transition T:** Given state `(x,y)` and action, returns the new adjacent coordinate.
*   **Initial state s0:** The coordinate marked by `S`.
*   **Goal G:** The coordinate marked by `G`.
*   **Cost c:** 1 for every movement.

(a) What information is necessary to specify a state?
The (x, y) coordinates of the agent.

(b) What makes an action invalid?
Moving out of grid bounds or moving into an obstacle (`#`).

(c) Is this a deterministic search problem?
Yes, every action has exactly one guaranteed outcome state.

(d) What would constitute a solution?
A sequence of valid coordinates starting from `s0` and ending at `G`.

## Task 5: Compare A* with Blind Search
| Measure | BFS | A* (Manhattan) |
| :--- | :--- | :--- |
| Solution found | Yes | Yes |
| Path length | 30 | 30 |
| States expanded | ~90 | ~65 |

(a) Did both algorithms find a solution? Yes.
(b) Did they find paths of the same length? Yes, both find the optimal shortest path.
(c) Which algorithm expanded fewer states? A*.
(d) Why might A* expand fewer states? Because the heuristic guides it toward the goal, avoiding exploration in opposite directions.

## Task 6: Investigate the Heuristic
The Manhattan distance is appropriate because the robot is restricted to horizontal and vertical movements, mirroring the grid's geometry perfectly.

1.  **h(n) = 0:** The algorithm degenerates into Dijkstra's Algorithm (equivalent to BFS on uniform cost graphs) and expands all nodes isotropically.
2.  **Euclidean distance:** Expands slightly more nodes than Manhattan because it underestimates the true grid distance more than Manhattan does.
3.  **Heuristic * 2:** It becomes a greedy search (inadmissible). It might expand fewer states but can return a suboptimal path length.

## Final Reflection
1.  **Why formulate before writing?** To rigorously define what states and transitions actually mean, saving confusion during implementation and ensuring correctness.
2.  **Informed search?** A* uses domain-specific knowledge (the heuristic) to estimate remaining cost, unlike BFS which searches blindly.
3.  **Choice of heuristic?** It balances speed vs optimality. An inadmissible heuristic sacrifices optimal paths for speed, while a weak heuristic explores too many states.
4.  **LLM Contribution:** The LLM provided the boilerplate priority queue setup and graph traversal code, allowing me to focus on verifying the logic and heuristic implementation.
5.  **Danger of unverified code:** An LLM might hallucinate inadmissible heuristics or incorrectly handle visited states, leading to infinite loops or suboptimal paths without warning.
