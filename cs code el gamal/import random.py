import random
def is_prime(n):#Fun check if number is prime
    if n < 2:#if Number is less than its not prime
        return False
    for i in range(2, int(n**0.5) + 1): # Loop from 2 to the square root of n
        if n % i == 0: # If n is dividble by i then its not prime
            return False
    return True# If no divisors found then n will be prime prime

def generate_prime(start=50, end=200):# Function that generates a random prime numberin the range
    primes = [n for n in range(start, end) if is_prime(n)]# Creates a list of prime numbers in the range
    return random.choice(primes)# Randomly selects one prime number from the list

def find_primitive_root(p):# finds a primitive root of a prime number p
    if p == 2:
        return 1
    required_set = {num for num in range(1, p) if is_prime(num)}#this line creates a set of prime number that are less than p
    for g in range(2, p):#loop over potential generators (g) from 2 to p-1
        actual_set = {pow(g, power, p) for power in range(1, p)}# Create a set of g raised to the power of 1 to p-1, modulo p
        if len(actual_set) == p - 1: # Check if g is a primitive root
            return g
    return None# Return None if there is no primitive root is found

def generate_keys(p, g):#defines a function named generate_keys that takes two parameters a prime number and g or a generator
    private_key = random.randint(2, p - 2)#genrates a random private key in between 2 and p-2
    h = pow(g, private_key, p)#Calculate public key h as g raised to private_key, then take modulo p.
    return (p, g, h), private_key#Return the public key (p, g, h) and the private key.

def encrypt(public_key, message):
    p, g, h = public_key # Get the values p, g, and h from the public key
    k = random.randint(2, p - 2)   # Choose a random number k between 2 and p-2 for encryption.
    c1 = pow(g, k, p)    # Calculate c1 as g raised to the power of k, then take modulo p.        
    c2 = (message * pow(h, k, p)) % p  # Calculate c2 as the message multiplied by h raised to the power of k, then take modulo p.
    return c1, c2

def decrypt(private_key, p, c1, c2):
    s = pow(c1, private_key, p)   # Calculate s as c1 raised to the power of the private key, then take modulo p.
    s_inv = pow(s, -1, p)      # Calculate the modular inverse of s beacuse its nedded for decryption 
    message = (c2 * s_inv) % p   # Recover the original message by multiplying c2 with the inverse of s, then take modulo p.
    return message


if __name__ == "__main__":# Check if this script is being run directly.
    p = generate_prime()# Generate a random prime number and store it in p.
    g = find_primitive_root(p)# Find a primitive root for the prime number p.
    
    if g is None:
        print(f"Failed to find a primitive root for prime number {p}")
        exit()
    
    print(f"Generated prime number (p): {p}")
    print(f"Primitive root (g): {g}")
    print("\nGenerating keys...")
    public_key, private_key = generate_keys(p, g)
    print("Public Key (p, g, h):", public_key)
    print("Private Key:", private_key)
    
    while True:
        print("\nOptions:")
        print("1. Encrypt a message")
        print("2. Decrypt a message")
        print("3. Exit")
        choice = input("Choose an option (1 or 2 or 3): ")
        
        if choice == "1":
            message = int(input(f"Enter a message (as an integer less than {p}): "))
            if message <= 0 or message >= p:
                print(f"Message must be more than 0 and less than {p}.")
            else:
                c1, c2 = encrypt(public_key, message)
                print(f"Encrypted message: (c1={c1}, c2={c2})")
        
        elif choice == "2":
            try:
                c1 = int(input("Enter c1: "))
                c2 = int(input("Enter c2: "))
                decrypted_message = decrypt(private_key, public_key[0], c1, c2)
                print(f"Decrypted message: {decrypted_message}")
            except ValueError:
                print("make sure that c1 and c2 are integers.")
        
        elif choice == "3":
            print("you left the menu")
            break
        
        else:
            print("Please select 1, 2, or 3.")