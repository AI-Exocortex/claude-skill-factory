# ZOMBIES - Test Case Discovery Heuristic

Two dimensions guide test planning:

**ZOM axis** (simple → complex):
- **Z** - Zero: empty, null, none, initial state
- **O** - One: single item, first transition
- **M** - Many: multiple items, more complex scenarios

**BIE considerations** (apply at each ZOM level):
- **B** - Boundary: edge cases, limits, off-by-one
- **I** - Interface: does the API make sense as it emerges?
- **E** - Exceptions: error conditions, invalid inputs

**S** - Simple scenarios, simple solutions (applies throughout)

## How to use

1. Start with Zero - test the object in its initial state
2. Progress through One, then Many
3. At each level, consider Boundaries, Interface clarity, and Exceptions
4. Keep solutions simple - hard-coded values are fine early on, generalize later

## Example: Testing a stack

```
[TEST] New stack is empty                                <- Z
[TEST] Push one item, stack is not empty                 <- O
[TEST] Push and pop returns the item                     <- O + I
[TEST] Pop from empty stack throws                       <- Z + E
[TEST] Push multiple, pop returns in LIFO order          <- M
[TEST] Push to capacity, then push throws                <- B + E
```

---
Source: [TDD Guided by ZOMBIES](https://blog.wingman-sw.com/tdd-guided-by-zombies) by James Grenning
