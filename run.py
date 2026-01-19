#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple launcher script for Page Maker
Just run: python3 run.py
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

# Import and run the main application
from page_maker import main

if __name__ == "__main__":
    print("Starting Page Maker...")
    print("If the GUI doesn't appear, make sure you have a display available.")
    print("For headless usage, see demo.py for examples.\n")
    
    try:
        main()
    except Exception as e:
        print(f"\nError: {e}")
        print("\nIf you see 'no display name' or similar errors, it means")
        print("you're running in a headless environment without GUI support.")
        print("\nYou can still use the demo.py script to generate HTML files:")
        print("  python3 demo.py")
        sys.exit(1)
