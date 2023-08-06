import os

def askIfSure(answer):
    if answer == "yes" or "y":
        os.system("shutdown -s")
    else:
        print("Sure, I won't!")