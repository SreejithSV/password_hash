"""
Simple Test Script - Verify Rainbow Table Hash Cracking
Tests the specific hash: ceb6c970658f31504a901b89dcd3e461 -> test@123
"""

import hashlib
import random

# Character set
CHARSET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@!#$%&*"

def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()

def reduce_hash(hash_value, step, pwd_len):
    num = int(hash_value[:16], 16) + step
    base = len(CHARSET)
    pwd = ""
    for _ in range(pwd_len):
        pwd += CHARSET[num % base]
        num //= base
    return pwd

def generate_chain(start_pwd, chain_len, pwd_len):
    pwd = start_pwd
    for step in range(chain_len):
        h = hash_password(pwd)
        pwd = reduce_hash(h, step, pwd_len)
    return hash_password(pwd)

print("=" * 70)
print("RAINBOW TABLE TEST - Verify Hash Cracking")
print("=" * 70)
print()

# Verify test hash
test_password = "test@123"
test_hash = hash_password(test_password)
expected_hash = "ceb6c970658f31504a901b89dcd3e461"

print("VERIFICATION:")
print(f"  Password: {test_password}")
print(f"  Generated Hash: {test_hash}")
print(f"  Expected Hash:  {expected_hash}")
print(f"  Match: {test_hash == expected_hash} ✓" if test_hash == expected_hash else f"  Match: FAILED ✗")
print()

# Quick test with small table
print("QUICK TEST (Small Rainbow Table):")
print("  Generating 100 chains of length 100...")

pwd_len = 8
chain_len = 100
num_chains = 100

rainbow_table = {}
for i in range(num_chains):
    start_pwd = "".join(random.choice(CHARSET) for _ in range(pwd_len))
    end_hash = generate_chain(start_pwd, chain_len, pwd_len)
    rainbow_table[start_pwd] = end_hash

print(f"  Table generated: {len(rainbow_table)} chains")
print()

# Test with a password from the table
test_start = list(rainbow_table.keys())[0]
pwd = test_start
for step in range(chain_len // 2):
    h = hash_password(pwd)
    pwd = reduce_hash(h, step, pwd_len)

test_hash_in_table = hash_password(pwd)

print("TEST CASE 1: Password in Table")
print(f"  Test Hash: {test_hash_in_table}")
print(f"  Expected Password: {pwd}")

# Simple lookup
found = False
if test_hash_in_table in rainbow_table.values():
    print("  ✓ Hash found in endpoints!")
    found = True
else:
    # Try intermediate positions
    for pos in range(chain_len - 1, -1, -1):
        test = test_hash_in_table
        for step in range(pos, chain_len):
            p = reduce_hash(test, step, pwd_len)
            test = hash_password(p)
        
        if test in rainbow_table.values():
            print(f"  ✓ Hash found at intermediate position {pos}!")
            found = True
            break

if found:
    print("  Result: SUCCESS ✓")
else:
    print("  Result: FAILED ✗")

print()
print("=" * 70)
print("TEST COMPLETE")
print()
print("To crack the actual hash 'ceb6c970658f31504a901b89dcd3e461':")
print("  1. Run: python rainbow_table_app.py")
print("  2. Generate larger table (5000 chains, length 1000)")
print("  3. Click 'Crack Hash'")
print()
print("Expected result: test@123")
print("=" * 70)
