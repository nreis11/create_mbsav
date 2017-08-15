import re
# Parse yaml
# Create node with caption, key, tag, parentkey

# <NODE Caption="Plumber" Key="eq1" Tag="55" ParentKey=""/>

class Node(object):

    def __init__(self, props={}):
        for attr, value in props.items():
            setattr(self, attr, value)
        self.has_children = False

    def __str__(self):
        if self.has_children:
            closing_tags = '</NODE>' * self.closing_tags
            return closing_tags + '<NODE Caption="{0}" Key="{1}" Tag="{2}" ParentKey="{3}">'.format(
                self.caption, self.key, self.tag, self.parent_key)
        else:
            return '<NODE Caption="{0}" Key="{1}" Tag="{2}" ParentKey="{3}"/>'.format(
                self.caption, self.key, self.tag, self.parent_key)

def open_yaml(filename):
    try:
        file = open(filename)
    except IOError:
        print("File not found. Please check and try again")
        exit(0)
    return file

def create_node(caption, key, tag, parent_key, closing_tags):
    return Node({
    "caption": caption,
    "key": key,
    "tag": tag,
    "parent_key": parent_key,
    "closing_tags": closing_tags
    })

def get_tier(line):
    tier_match = re.search(r'^\s*', line)
    tier = (len(tier_match.group()) // 4) + 1
    return tier

def get_value(line, label=False):
    if label:
        value = re.search(r':\s*[\'"]?([^\'"]*)[\'"]?', line)
    else:
        value = re.search(r'^\s*[\'"]?([^\'"]*)[\'"]?:', line)

    if value:
        return value.group(1)
    print("No values found. Please check your yaml and try again.")
        

def get_parent_key(curr_tier, parents):
    if curr_tier > 1:
        parent_key = parents[curr_tier - 1]
    else:
        parent_key = ''
    return parent_key

def parse_yaml(filename):
    file = open_yaml(filename)
    key = 0
    parents = {}
    prev_tier, curr_tier = 1, 1
    closing_tags = 0
    board_data = ''
    nodes = []
    for num, line in enumerate(file, start=1):
        if num % 2:
            # Parse value
            curr_tier = get_tier(line)
            key += 1
            eqkey = 'eq' + str(key)
            parents[curr_tier] = eqkey
            parent_key = get_parent_key(curr_tier, parents)
            tag = get_value(line)
        else:
            # Parse label
            caption = get_value(line, True)
            diff = 0
            if curr_tier < prev_tier:
                diff = prev_tier - curr_tier
                closing_tags -= diff
            elif curr_tier > prev_tier:
                # Prev node needs to be open
                closing_tags += 1
                nodes[-1].has_children = True
            node = create_node(caption, eqkey, tag, parent_key, diff)
            nodes.append(node)
            # print(node)
            prev_tier = curr_tier
    for node in nodes:
        board_data += str(node)
    # print("Closing tags", closing_tags)
    board_data += '</NODE>' * closing_tags
    debug(board_data)
    return board_data
    # return ''.join(map(lambda node: print(node), nodes))

def debug(data):
    open_tag = '">'
    close_tag = '</NODE>'
    print("Open tags:", data.count(open_tag))
    print("Close tags:", data.count(close_tag))




