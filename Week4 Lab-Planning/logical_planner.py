from collections import deque

class Action:
    def __init__(self, name, pre_pos, pre_neg, eff_pos, eff_neg):
        self.name = name
        self.pre_pos = frozenset(pre_pos)
        self.pre_neg = frozenset(pre_neg)
        self.eff_pos = frozenset(eff_pos)
        self.eff_neg = frozenset(eff_neg)

    def is_applicable(self, state):
        return self.pre_pos.issubset(state) and state.isdisjoint(self.pre_neg)

    def apply(self, state):
        return (state - self.eff_neg) | self.eff_pos

def solve_planning_problem(initial_state, goal_state, actions):
    initial_state = frozenset(initial_state)
    goal_state = frozenset(goal_state)
    
    frontier = deque([(initial_state, [])])
    visited = {initial_state}

    while frontier:
        current_state, plan = frontier.popleft()

        # Check if the goal propositions are a subset of the current state
        if goal_state.issubset(current_state):
            return plan

        for action in actions:
            if action.is_applicable(current_state):
                next_state = frozenset(action.apply(current_state))
                if next_state not in visited:
                    visited.add(next_state)
                    frontier.append((next_state, plan + [action.name]))

    return None

if __name__ == "__main__":
    # Domain definition
    actions = [
        Action("Move(A, B)", ["At(Robot, A)"], [], ["At(Robot, B)"], ["At(Robot, A)"]),
        Action("Move(B, A)", ["At(Robot, B)"], [], ["At(Robot, A)"], ["At(Robot, B)"]),
        Action("Move(B, C)", ["At(Robot, B)"], [], ["At(Robot, C)"], ["At(Robot, B)"]),
        Action("Move(C, B)", ["At(Robot, C)"], [], ["At(Robot, B)"], ["At(Robot, C)"]),
        Action("PickUp(Package, A)", ["At(Robot, A)", "At(Package, A)"], [], ["Holding(Package)"], ["At(Package, A)"]),
        Action("PickUp(Package, B)", ["At(Robot, B)", "At(Package, B)"], [], ["Holding(Package)"], ["At(Package, B)"]),
        Action("PickUp(Package, C)", ["At(Robot, C)", "At(Package, C)"], [], ["Holding(Package)"], ["At(Package, C)"]),
        Action("Drop(Package, A)", ["At(Robot, A)", "Holding(Package)"], [], ["At(Package, A)"], ["Holding(Package)"]),
        Action("Drop(Package, B)", ["At(Robot, B)", "Holding(Package)"], [], ["At(Package, B)"], ["Holding(Package)"]),
        Action("Drop(Package, C)", ["At(Robot, C)", "Holding(Package)"], [], ["At(Package, C)"], ["Holding(Package)"]),
    ]

    # Test A: Solvable Problem
    initial_state = ["At(Robot, A)", "At(Package, A)"]
    goal_state = ["At(Package, C)"]
    plan = solve_planning_problem(initial_state, goal_state, actions)
    print("Test A Plan:", plan)

    # Test B: Impossible Problem (Remove PickUp actions)
    impossible_actions = [a for a in actions if not a.name.startswith("PickUp")]
    plan_imp = solve_planning_problem(initial_state, goal_state, impossible_actions)
    print("Test B Plan:", "No plan found" if plan_imp is None else plan_imp)
