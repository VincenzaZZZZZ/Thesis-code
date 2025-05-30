def print_warning():
    print("NUCLEAR CORE UNSTABLE!!!")
    print("Quarantine is in effect.")
    print("Surrounding hamlets will be evacuated.")
    print("Anti-radiationsuits and iodine pills are mandatory.")

n = int(input("Please enter the number of repeating times: "))
for i in range(1, n):
    print_warning()
    print()