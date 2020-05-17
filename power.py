from CPU.cpu import cpu
import sys

if len(sys.argv) != 2:
    print("Usage: python power.py [On/Off]")
    exit(1)

cpui = cpu()
if sys.argv[1] == 'On':
    cpui.run()

if sys.argv[1] == 'Off':
    cpui.down()
