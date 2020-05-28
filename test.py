def chkList(lst):
    return len(set(lst)) == 1


if __name__ == "__main__":
    # Driver Code
    lst = ['G', 'T', 'G', 'G']

    if chkList(lst) == True:
        print("Equal")
    else:
        print("Not Equal")
