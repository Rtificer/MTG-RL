def obtainpositiveinteger(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value > 0:
                return value
            else:
                print(f"{value} is not a valid input. Please input a positive integer.")
        except ValueError:
            print("Please input an integer value.")