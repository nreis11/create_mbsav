from __future__ import absolute_import, print_function
import eq_values
import yaml_parser
import sys
assert sys.version_info >= (2,7)
testing = False

# Testing functions
if len(sys.argv) > 2 and sys.argv[2] == '-t':
    import debug
    testing = True

if len(sys.argv) > 1:
    yaml_file = sys.argv[1]
else:
    print("Please supply yaml name as argv. Ex: <Industries.yaml>")
    exit(0)

print("Importing", yaml_file)
board_data = yaml_parser.parse_yaml(yaml_file)

eq_categories = ['Categories', "Industries", "States", "Countries"]
eq_bools = ["False"] * len(eq_categories)

print("\nWhich category are you importing?")
for idx, category in enumerate(eq_categories, start=1):
    print(idx, category)

category = 999
while category not in range(len(eq_categories)):
    try:
        category = int(input("\nNumber: ")) - 1
    except Exception:
        print('Please type a valid number.')

eq_bools[category] = "True"

def check_options(option):
    """Handles boolean options for output"""
    while True:
        if sys.version_info >= (3,0):
            choice = input(option + '(Y or N): ').upper()
        else:
            choice = raw_input(option + '(Y or N): ').upper()

        if choice == 'Y':
            return 1
        elif choice == 'N':
            return 0
        else:
            print('That is not a valid answer. Y or N? ')

parents_selectable = check_options("Parents selectable?")
output_parents = check_options("Output parents?")

template = '''
<?xml version="1.0" encoding="UTF-8" ?>
<saved version="3">
\t<external_site>
\t\t<chkParentsSelectable>{0}</chkParentsSelectable>
\t\t<chkOutputParents>{1}</chkOutputParents>
\t\t<optCategories>{2}</optCategories>
\t\t<optIndustries>{3}</optIndustries>
\t\t<optStates>{4}</optStates>
\t\t<optCountries>{5}</optCountries>
\t\t<categories><![CDATA[
<NODES>{6}</NODES>
\t\t]]></categories>
\t</external_site>
'''.format(
    parents_selectable, output_parents,
    eq_bools[0], eq_bools[1],
    eq_bools[2], eq_bools[3],
    board_data
    ).strip()

category_choice = 'eq_{0}_data'.format(eq_categories[category]).lower()
output = template + eq_values.data[category_choice]

try:
    with open("output.mbsav", 'w+') as f:
        f.write(output)
except Exception:
    print("An error occured writing to output.mbsav.")
else:
    print("output.mbsav successfully created.")

if testing:
    debug.verify_output("output.mbsav", "testfile.mbsav")
    debug.count_tags(board_data)
