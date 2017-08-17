import re
# Create node with caption, key, tag, parentkey

# <NODE Caption="Plumber" Key="eq1" Tag="55" ParentKey=""/>

class Node(object):

    _KEY = 1

    def __init__(self, caption, tag, parent_key, tier):
        self.caption = caption
        self.key = 'eq' + str(self._KEY)
        self.__class__._KEY += 1
        self.tag = tag
        self.parent_key = parent_key
        self.tier = tier
        self.has_children = False

    def __str__(self):
        tail = '>' if self.has_children else '/>'
        return '<NODE Caption="{0}" Key="{1}" Tag="{2}" ParentKey="{3}"'.format(
            self.caption, self.key, self.tag, self.parent_key) + tail


def open_yaml(filename):
    try:
        file = open(filename)
    except IOError:
        print("File not found. Please check filename (Ex. <Countries.yaml>) and try again.")
        exit(0)
    return file

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
    print("No values found. Values and labels should be on alternating lines.")
    print("Please check your yaml and try again.")
        

def get_parent_key(curr_tier, parents):
    parent_key = parents[curr_tier - 1] if curr_tier > 1 else ''
    return parent_key

def check_for_empty_line(num, line):
    empty_line = re.search(r'^\s*$', line)
    if empty_line:
        print("Empty line found! Please remove empty line from yaml and try again.")
        print("Line:", num)
        exit(0)

def parse_yaml(filename):
    file = open_yaml(filename)
    parents = {}
    nodes = []
    for num, line in enumerate(file, start=1):
        check_for_empty_line(num, line)
        if num % 2:
            # Parse value
            tier = get_tier(line)
            parent_key = get_parent_key(tier, parents)
            tag = get_value(line)
        else:
            # Parse label
            caption = get_value(line, True)
            node = Node(caption, tag, parent_key, tier)
            parents[tier] = node.key
            nodes.append(node)
    board_data = create_board_data(nodes)
    return board_data

def create_board_data(nodes):
    closing_tags = 0
    board_data = ''
    last_node = nodes[-1]
    for idx, node in enumerate(nodes):
        if last_node == node:
            # print('\t' * (node.tier - 1), idx + 1, str(node))
            board_data += str(node)
            break
        next_node = nodes[idx + 1]
        diff = 0
        if node.tier < next_node.tier:
            node.has_children = True
            closing_tags += 1
        elif node.tier > next_node.tier:
            diff = node.tier - next_node.tier
            closing_tags -= diff
        board_data += str(node) + ('</NODE>' * diff)
        # print('\t' * (node.tier - 1), idx + 1, str(node))
    # & needs to be encoded properly
    board_data = re.sub(r'&', '&amp;', board_data)
    return board_data + ('</NODE>' * closing_tags)