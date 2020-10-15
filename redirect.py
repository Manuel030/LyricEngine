# redirect stdout to variable
old_stdout = sys.stdout
new_stdout = io.StringIO()
sys.stdout = new_stdout
# print statement comes here
sentence = new_stdout.getvalue()  # sentence is the variable where string is stored
sys.stdout = old_stdout