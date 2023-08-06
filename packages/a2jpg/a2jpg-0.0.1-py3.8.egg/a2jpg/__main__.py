"""entry point"""
import sys

from a2jpg.a2jpg import main

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))