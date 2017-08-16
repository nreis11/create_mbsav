import eq_values
import yaml_parser
import sys

if len(sys.argv) > 1:
    yaml_file = sys.argv[1] + '.yaml'
else:
    print("Please supply yaml name as argv. Ex: <Industries>")
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

template = '''
<?xml version="1.0" encoding="UTF-8" ?>
<saved version="3">
\t<external_site>
\t\t<chkParentsSelectable>0</chkParentsSelectable>
\t\t<chkOutputParents>0</chkOutputParents>
\t\t<optCategories>{0}</optCategories>
\t\t<optIndustries>{1}</optIndustries>
\t\t<optStates>{2}</optStates>
\t\t<optCountries>{3}</optCountries>
\t\t<categories><![CDATA[
<NODES>{4}</NODES>
\t\t]]></categories>
\t</external_site>
        '''.format(
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