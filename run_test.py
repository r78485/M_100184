import os
import sys

# redirect stdout and stderr
with open('test_output.txt', 'w') as f:
    sys.stdout = f
    sys.stderr = f
    try:
        import test_qr
        print("Success")
    except Exception as e:
        import traceback
        traceback.print_exc()
