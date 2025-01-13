#!/env/python3



def euclidean_algo(a, b):
    while b != 0:
        r = a % b
        a = b
        b = r
    return a

def main():
    try:
        # Wait for 2 arguments as integers
        num1 = int(input("Enter the first integer: "))
        num2 = int(input("Enter the second integer: "))
        
        # Call the addition function
        gcd = euclidean_algo(num1, num2)
        print(f"The gdc of {num1} & {num2} = {gcd}")
    
    except ValueError:
        print("Error: Please enter valid integers.")

if __name__ == "__main__":
    main()
