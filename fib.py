# This function generates Fibonacci numbers
def fib(n):
    # Initialize variables
    a, b = 0, 1
    # Create a list to store the Fibonacci sequence
    fib_list = []
    # Loop through n times and generate the Fibonacci sequence
    for i in range(n):
        # Append the current value of a to the list
        fib_list.append(a)
        # Update the values of a and b
        a, b = b, a + b
    # Return the list of Fibonacci numbers
    return fib_list