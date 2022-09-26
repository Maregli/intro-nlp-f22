from collections import defaultdict

def create_parent(node_dict, key, avail_vars, input_vars: dict, idx):
    content = node_dict[key]["content"]
    parent_content = []

    #Input nodes
    if not isinstance(content, list) == 1: #If we arrive at the end of unpacking
        if content in input_vars:
            node_dict[key]["value"] = input_vars[content] #Setting value to input
        else:
            node_dict[key]["value"] = content
        return node_dict, []

    #Operation nodes
    for i, cont in enumerate(content):
        if cont in ["+", "-", "*", "/", "^"]: #bivariate function
            parent_content.extend(content[:i])
            parent_content.extend(content[i+1:])
            operation = cont
            break
        elif cont in ["exp", "log", "sin", "cos"]: #univariate functions 
            parent_content = [content[1]]
            operation = cont
            break
        else:
            continue


    #Names for new keys, have to check if part of content is an input variable
    new_keys = []
    input_vars = list(input_vars.keys()) 
    for i, cont in enumerate(parent_content):
        if cont in input_vars: #If it is an input variable, key name = variable name
            new_keys.append(cont)
        else:
            new_keys.append(avail_vars[idx + i]) #If it is not an input, give it a name from the list

    #Adding parent keys, parent content and operation on the parents which is performed in current node
    node_dict[key]["parents"] = new_keys
    node_dict[key]["parent_contents"] = parent_content
    node_dict[key]["operator"] = operation

    #Creating parent nodes, adding their content and children
    for i, new_key in enumerate(new_keys):
        node = defaultdict()
        node["content"] = parent_content[i]
        node["children"] = [key]
        #Adding the created node as entry to the dict
        node_dict[new_key] = node
        #print("key: ", new_key, " | content", node["content"])
    

    #Return Dict and new_nodes
    return node_dict, new_keys


class Builder():

    def __init__(self, infix: list, in_vars: dict = {}):
        """
        infix: list of infix notation parse, e.g. [['exp', 2], '-', 3]
        in_vars: dict of input variables to ensure they are not used as intermediate or output variables
        RETURN: computation graph in a data structure of your choosing
        """

        ## some alphabetical vars to use as intermediate and output variables minus the input vars to avoid duplicates
        avail_vars = list(map(chr, range(97, 123))) + list(map(chr, range(945, 969)))
        if len(in_vars.keys()) > 0:
            avail_vars = set(avail_vars) - set(in_vars)
        self.avail_vars = sorted(list(set(avail_vars)), reverse=True)
        self.in_vars = in_vars
        self.infix = infix
        # Making a dictionary. The key is the node name chosen from avail_vars. Value is another dictionary with keys:
        # Parents: keynames of the parent nodes, set to None if input nodes
        # Children: keynames of the child nodes, set to None if output nodes
        # Value: Is value of node resulting from forward pass. Beginning None, will be filled when forward pass is initialized. 
        # Operator: Operator sign, to map node to an operator class in the forward pass
        # Content: Is the infix content of the node, as sanity check
        keys = ["output"]
        node_dict = defaultdict(None, {"output": {"content": infix, "children": None}})
        while len(keys) > 0:
            key = keys[0]
            node_dict, new_keys = create_parent(node_dict, key = key, avail_vars = self.avail_vars, input_vars=self.in_vars, idx = len(node_dict.keys())-1)
            keys.extend(new_keys) #appending keys to key list
            keys = keys[1:] #removing key I just worked on from new keys
        self.graph = node_dict
if __name__ == '__main__':
   pass