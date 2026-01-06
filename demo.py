#!/usr/bin/env python3
"""
Demo script to run the game with predefined inputs for testing.
"""
import subprocess
import sys

# Predefined inputs: username, rock, paper, scissors
inputs = "DemoUser\nrock\npaper\nscissors\n"

# Run the main.py with inputs piped in
process = subprocess.run(
    [sys.executable, "main.py"],
    input=inputs,
    text=True,
    capture_output=True
)

print("STDOUT:")
print(process.stdout)
print("STDERR:")
print(process.stderr)
print("Return code:", process.returncode)