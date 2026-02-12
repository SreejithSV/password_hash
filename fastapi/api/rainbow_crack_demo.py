"""
Rainbow Table Hash Cracker - Command Line Version
Demonstrates cracking the test hash: ceb6c970658f31504a901b89dcd3e461 -> test@123
"""

import hashlib
import random
import time
import sys

# Character set
CHARSET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@!#$%&*"

def hash_password(password):
    """Generate MD5 hash"""
    return hashlib.md5(password.encode()).hexdigest()

def reduce_hash(hash_value, step, pwd_len):
    """Reduction function"""
    num = int(hash_value[:16], 16) + step
    base = len(CHARSET)
    pwd = ""
    for _ in range(pwd_len):
        pwd += CHARSET[num % base]
        num //= base
    return pwd

def generate_chain(start_pwd, chain_len, pwd_len):
    """Generate rainbow chain"""
    pwd = start_pwd
    for step in range(chain_len):
        h = hash_password(pwd)
        pwd = reduce_hash(h, step, pwd_len)
    return hash_password(pwd)

def crack_hash(target_hash, rainbow_table, chain_len, pwd_len):
    """Crack hash using rainbow table"""
    print(f"\n[*] Searching for hash: {target_hash}")
    print(f"[*] Checking {len(rainbow_table)} chains...")
    
    # Check endpoints
    if target_hash in rainbow_table.values():
        print("[+] Found in endpoints!")
        for start_pwd, end_hash in rainbow_table.items():
            if end_hash == target_hash:
                pwd = start_pwd
                for step in range(chain_len):
                    h = hash_password(pwd)
                    if h == target_hash:
                        return pwd, True
                    pwd = reduce_hash(h, step, pwd_len)
                return pwd, True
    
    # Check intermediate positions
    print("[*] Checking intermediate positions...")
    for pos in range(chain_len - 1, -1, -1):
        if pos % 100 == 0:
            print(f"[*] Checking position {pos}/{chain_len}")
        
        test_hash = target_hash
        for step in range(pos, chain_len):
            pwd = reduce_hash(test_hash, step, pwd_len)
            test_hash = hash_password(pwd)
        
        if test_hash in rainbow_table.values():
            print(f"[+] Found match at position {pos}!")
            for start_pwd, end_hash in rainbow_table.items():
                if end_hash == test_hash:
                    pwd = start_pwd
                    for step in range(chain_len):
                        h = hash_password(pwd)
                        if h == target_hash:
                            return pwd, True
                        pwd = reduce_hash(h, step, pwd_len)
    
    return None, False

def main():
    print("=" * 60)
    print("RAINBOW TABLE HASH CRACKER - DEMONSTRATION")
    print("=" * 60)
    
    # Configuration
    pwd_len = 8
    chain_len = 1000
    num_chains = 5000
    
    print(f"\n[CONFIG]")
    print(f"  Password Length: {pwd_len}")
    print(f"  Chain Length: {chain_len}")
    print(f"  Number of Chains: {num_chains}")
    print(f"  Character Set: {len(CHARSET)} characters")
    
    # Generate rainbow table
    print(f"\n[GENERATION PHASE]")
    print(f"Generating rainbow table with {num_chains} chains...")
    
    rainbow_table = {}
    start_time = time.time()
    
    for i in range(num_chains):
        start_pwd = "".join(random.choice(CHARSET) for _ in range(pwd_len))
        end_hash = generate_chain(start_pwd, chain_len, pwd_len)
        rainbow_table[start_pwd] = end_hash
        
        if (i + 1) % 500 == 0:
            print(f"  Progress: {i + 1}/{num_chains} chains generated")
    
    gen_time = time.time() - start_time
    total_hashes = num_chains * chain_len
    hash_rate = total_hashes / gen_time
    
    print(f"\n[STATISTICS]")
    print(f"  Generation Time: {gen_time:.2f} seconds")
    print(f"  Total Hashes Computed: {total_hashes:,}")
    print(f"  Hash Rate: {hash_rate:,.0f} hashes/second")
    print(f"  Table Size: {len(rainbow_table):,} endpoints")
    print(f"  Memory Used: {sys.getsizeof(rainbow_table) / 1024:.2f} KB")
    
    # Test cracking
    print(f"\n[CRACKING PHASE]")
    target_hash = "ceb6c970658f31504a901b89dcd3e461"
    expected_pwd = "test@123"
    
    print(f"Target Hash: {target_hash}")
    print(f"Expected Password: {expected_pwd}")
    
    crack_start = time.time()
    password, success = crack_hash(target_hash, rainbow_table, chain_len, pwd_len)
    crack_time = time.time() - crack_start
    
    print(f"\n[RESULTS]")
    if success:
        print(f"  ✓ SUCCESS!")
        print(f"  Password Found: {password}")
        print(f"  Crack Time: {crack_time:.2f} seconds")
        print(f"  Match: {password == expected_pwd}")
    else:
        print(f"  ✗ FAILED")
        print(f"  Password not found in rainbow table")
        print(f"  Time Spent: {crack_time:.2f} seconds")
        print(f"\n  Note: The password might not be in the table.")
        print(f"  Try increasing the number of chains or regenerating the table.")
    
    # Additional test with known password in table
    print(f"\n[VALIDATION TEST]")
    print("Testing with a password guaranteed to be in the table...")
    
    # Pick a random chain
    test_start, test_end = list(rainbow_table.items())[0]
    
    # Reconstruct to get a password in the middle
    pwd = test_start
    for step in range(chain_len // 2):
        h = hash_password(pwd)
        pwd = reduce_hash(h, step, pwd_len)
    
    test_hash = hash_password(pwd)
    print(f"Test Hash: {test_hash}")
    print(f"Expected Password: {pwd}")
    
    found_pwd, found = crack_hash(test_hash, rainbow_table, chain_len, pwd_len)
    
    if found:
        print(f"\n  ✓ Validation PASSED")
        print(f"  Found Password: {found_pwd}")
    else:
        print(f"\n  ✗ Validation FAILED")
    
    print("\n" + "=" * 60)
    print("DEMONSTRATION COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    main()
