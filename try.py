def divide (a,b):
    try:
        result = a/b
    except ZeroDivisionError: 
        print("Error, cannot divide by zero")
    else:
        print(result)

divide(10,0)

