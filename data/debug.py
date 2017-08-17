import filecmp

# Testing functions 
# Testfile = doccafe/Types.yaml

def verify_output(file1, file2):
    """Compares the output with the testfile to see if they are equal"""
    print("\n\n***TESTING***")
    if filecmp.cmp(file1, file2, shallow=False):
        print("Output verified")
    else:
        print("Output is not equal to test file (doccafe/Types.yaml)!")
        print("1 n n")

def count_tags(data):
    """Verifies equal opening and closing tags for all board nodes"""
    open_tag = '">'
    close_tag = '</NODE>'
    print("Open tags:", data.count(open_tag))
    print("Close tags:", data.count(close_tag))
