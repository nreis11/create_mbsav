import re
# Parse yaml
# Create node with caption, key, tag, parentkey

# <NODE Caption="Plumber" Key="eq1" Tag="55" ParentKey=""/>

class Node(object):

    def __init__(self, caption, key, tag, parent_key, tier):
        self.caption = caption
        self.key = key
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
            tier = get_tier(line)
            key += 1
            eqkey = 'eq' + str(key)
            parents[tier] = eqkey
            parent_key = get_parent_key(tier, parents)
            tag = get_value(line)
        else:
            # Parse label
            caption = get_value(line, True)
            node = Node(caption, eqkey, tag, parent_key, tier)
            nodes.append(node)
    board_data = create_board_data(nodes)
    # debug(board_data)
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
        # Debug
        # print('\t' * (node.tier - 1), idx + 1, str(node))
    # & needs to be encoded properly
    board_data = re.sub(r'&', '&amp;', board_data)
    return board_data + ('</NODE>' * closing_tags)

def debug(data):
    open_tag = '">'
    close_tag = '</NODE>'
    print("Open tags:", data.count(open_tag))
    print("Close tags:", data.count(close_tag))

