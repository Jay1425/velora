#!/usr/bin/env python
"""
Velora Password Hash Generator
Utility script to generate secure password hashes for admin authentication
"""

from werkzeug.security import generate_password_hash
import getpass

def main():
    print("=" * 60)
    print("Velora Admin Password Hash Generator")
    print("=" * 60)
    print("\nThis tool generates a secure scrypt hash for your admin password.")
    print("The hash should be stored in your .env file as ADMIN_PASSWORD_HASH")
    print()
    
    # Get password from user
    while True:
        password = getpass.getpass("Enter admin password: ")
        password_confirm = getpass.getpass("Confirm password: ")
        
        if password != password_confirm:
            print("\n❌ Passwords don't match. Please try again.\n")
            continue
        
        if len(password) < 12:
            print("\n⚠️  Warning: Password should be at least 12 characters.")
            proceed = input("Continue anyway? (y/n): ")
            if proceed.lower() != 'y':
                continue
        
        break
    
    # Generate hash
    print("\nGenerating secure hash...")
    password_hash = generate_password_hash(password)
    
    # Display results
    print("\n" + "=" * 60)
    print("✅ Password hash generated successfully!")
    print("=" * 60)
    print("\nAdd this line to your .env file:")
    print("-" * 60)
    print(f"ADMIN_PASSWORD_HASH={password_hash}")
    print("-" * 60)
    print("\n⚠️  IMPORTANT:")
    print("   • Store this hash securely in your .env file")
    print("   • Never share the hash publicly")
    print("   • Keep a backup of your password securely")
    print("   • Add .env to .gitignore (already done)")
    print("\n")

if __name__ == "__main__":
    main()
