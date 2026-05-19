import json
import importlib.util
import ast
import os
import sys

# -----------------------------
# Utility: detect hardcoding
# -----------------------------
def detect_hardcoding(source_code: str, test_inputs: list) -> bool:
    """
    Returns True if the solution appears to hardcode answers.
    We check if any test input or expected output appears literally in the code.
    """
    for x in test_inputs:
        if str(x) in source_code:
            return True
        if str(x * x) in source_code:
            return True
    return False


# -----------------------------
# Load the student's solution
# -----------------------------
def load_student_solution(path="solution.py"):
    """
    Dynamically imports the student's solution file.
    """
    spec = importlib.util.spec_from_file_location("student_solution", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# -----------------------------
# Hidden tests
# -----------------------------
HIDDEN_TESTS = [
    (2, 4),
    (5, 25),
    (10, 100),
    (13, 169),
    (25, 625),
]


# -----------------------------
# Run tests
# -----------------------------
def run_tests(solve_fn):
    results = []
    passed = 0

    for (inp, expected) in HIDDEN_TESTS:
        try:
            output = solve_fn(inp)
            ok = (output == expected)
        except Exception:
            ok = False
            output = None

        results.append({
            "input": inp,
            "expected": expected,
            "output": output,
            "passed": ok
        })

        if ok:
            passed += 1

    return passed, results


# -----------------------------
# Main grading logic
# -----------------------------
def main():
    # 1. Read student code
    if not os.path.exists("solution.py"):
        print(json.dumps({"error": "solution.py not found"}))
        return

    with open("solution.py", "r") as f:
        source = f.read()

    # 2. Hardcoding check
    test_inputs = [t[0] for t in HIDDEN_TESTS]
    hardcoded = detect_hardcoding(source, test_inputs)

    # 3. Load solution
    try:
        student_module = load_student_solution("solution.py")
        solve_fn = student_module.solve
    except Exception as e:
        print(json.dumps({
            "score": 0,
            "error": f"Failed to import solve(): {e}"
        }))
        return

    # 4. Run tests
    passed, results = run_tests(solve_fn)

    # 5. Compute score
    score = passed / len(HIDDEN_TESTS)

    # Hardcoding penalty
    if hardcoded:
        score = min(score, 0.2)

    # 6. Output JSON
    print(json.dumps({
        "score": score,
        "hardcoding_detected": hardcoded,
        "results": results
    }, indent=2))


if __name__ == "__main__":
    main()