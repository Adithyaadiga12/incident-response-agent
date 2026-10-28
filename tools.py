from langchain_core.tools import tool

@tool
def read_logs(lines:int = 20) -> str:
    """Read the most recent lines from the service log file.
    Use this to see errors and warnings from the service."""
    
    try:
        with open("app.log","r") as f:
            all_lines = f.readlines()
        log_lines = all_lines[-lines:]
        return "".join(log_lines)
    
    except FileNotFoundError:
        return "Log file not found."
    
@tool
def get_metrics() -> str:
    """Get service health metrics: total requests, error count, warning count.
    Use this to see how healthy the service is overall."""
    try:
        with open("app.log",'r') as f:
            all_lines = f.readlines()
    except FileNotFoundError:
        return "Log file not found."
    
    requests = sum(1 for l in all_lines if "GET /data called" in l)
    errors = sum(1 for l in all_lines if "ERROR" in l)
    warning = sum(1 for l in all_lines if "WARNING" in l)
    
    return f"Requests: {requests},Errors:{errors},Warnings:{warning}"
    

    
if __name__ == "__main__":
    print(read_logs.invoke({"lines": 10}))
    print(get_metrics.invoke({}))
    