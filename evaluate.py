from agent import app
from eval_helpers import reset_logs,trigger_fault

TEST_CASES = [
    {"fault": "crash",  "expect": ["database", "connection"]},
    {"fault": "errors", "expect": ["upstream", "error"]},
    {"fault": "slow",   "expect": ["slow", "latency"]},
]

SYSTEM = """You are an incident response agent.
When given an alert, investigate using your tools:
- read_logs: to see recent errors and warnings
- get_metrics: to see request, error and warning counts
Find the root cause. Reply with:
Root cause: <one sentence>
Evidence: <what supports it>"""

def run_one(fault):
    
    reset_logs()
    trigger_fault(fault)
    result = app.invoke({
        "messages": [
            ("system", SYSTEM),
            ("user", "Alert: users report problems on the /data endpoint. Investigate.")
        ]
    })
    return result["messages"][-1].text.lower()

def check(answer,expected):
    return any(word in answer for word in expected)

if __name__ == "__main__":
    passed = 0
    for case in TEST_CASES:
        answer = run_one(case["fault"])
        ok = check(answer,case["expect"])
        passed += ok
        print(f"[{case['fault']}] {'PASS' if ok else 'FAIL'}")
        print(f"   answer: {answer[:120]}...")
    total = len(TEST_CASES)
    print(f"\nAccuracy: {passed}/{total} = {passed/total*100:.0f}%")
        
        