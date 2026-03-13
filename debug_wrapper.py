import sys
import traceback
import runpy

print("Starting debug wrapper...")
try:
    runpy.run_path("app.py", run_name="__main__")
except BaseException:
    print("Crashed! Writing log...")
    with open("crash.log", "w", encoding="utf-8") as f:
        f.write(traceback.format_exc())
    print("Log written.")
    sys.exit(1)
