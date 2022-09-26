from operations import *
class Executor():

    def __init__(self, graph: dict, in_vars: dict = {}):
        """
        graph: computation graph in a data structure of your choosing
        in_vars: dict of input variables, e.g. {"x": 2.0, "y": -1.0}
        """
        self.graph = graph
        self.in_vars = in_vars
        self.fn_map = {"log": Log(), "exp": Exp(), "+": Add(), "-": Sub(), "^": Pow(), "sin": Sin(), "*": Mult(), "/": Div()}
        self.output = -1
        self.derivative = {}

    ## forward execution____________________________

    def forward(self):
        graph = self.graph
        in_vars = self.in_vars
        map_dict = self.fn_map
        starter_nodes = []

        # 1 go over all nodes by iterating over their keys
        # 2 check if a key has a value already, if it does remove it from current node list
        # 3 if the key has no value check if all its parents have values. If not continue with loop
        # 4 If all parents have a value continue to do operation
        current_nodes = list(graph.keys())
        i = 0
        while graph["output"].get("value") == None:
            for key in current_nodes:
                if graph[key].get("value") != None: 
                    current_nodes.remove(key)
                    #If they already have values, forward doesn't need to work on those nodes anymor
                else: #All nodes that don't already have values
                    operation = graph[key].get("operator")
                    operator = map_dict[operation]
                    parents = graph[key].get("parents") #Look for parents of nodes
                    parent_values = []
                    for parent in parents: #Make a list of the parents values
                        parent_values.append(graph[parent].get("value"))
                    if None not in parent_values: #If all parents have arguments, you can do operation
                        a = parent_values[0]
                        b = None
                        if len(parents) == 2: #Only for bivariate functions
                            b = parent_values[1]
                        graph[key]["value"] = operator.f(a,b)
                        current_nodes.remove(key)
                        
                    else: #If some parents don't have a value yet
                        continue
                        
        print("Output created")
        self.output = graph["output"].get("value")

    ## backward execution____________________________

    def backward(self, ):
        #Initializing Variables
        graph = self.graph
        in_vars = self.in_vars
        map_dict = self.fn_map

        #Initializing input
        graph["output"]["df"] = 1
        current_nodes = ["output"]

        #Creating df for nodes
        while len(current_nodes) >0:
            parent_list = []

            #Filling out parent df
            for key in current_nodes:
                #Check if this is an input node
                parents = graph[key].get("parents")
                if parents == None:
                    continue

                #Find the operation done in the current node
                operation = graph[key]["operator"]
                operator = map_dict[operation]

                #Finding parent arguments and assign the df value:
                parents = graph[key]["parents"]
                df_before = graph[key]["df"] #Is the derivative of current before

                if len(parents) == 1:
                    parent_a = parents[0] #Parent node, that supplied argument a
                    a = graph[parent_a]["value"]
                    df = operator.df(a)*df_before
                    if graph[parent_a].get("df") == None: #If there already exists a derivative from different path, add them up
                        graph[parent_a]["df"] = df
                    else:
                        graph[parent_a]["df"] = graph[parent_a]["df"] + df
                    
                elif len(parents) == 2:
                    parent_a = parents[0]
                    parent_b = parents[1]
                    a = graph[parent_a]["value"]
                    b = graph[parent_b]["value"]
                    df = [df*df_before for df in operator.df(a,b)]
                    if graph[parent_a].get("df") == None: #If there already exists a derivative from different path, add them up
                        graph[parent_a]["df"] = df[0]
                    else:
                        graph[parent_a]["df"] = graph[parent_a]["df"] + df[0]
                    if graph[parent_b].get("df") == None: #If there already exists a derivative from different path, add them up
                        graph[parent_b]["df"] = df[1]
                    else:
                        graph[parent_b]["df"] = graph[parent_b]["df"] + df[1]
                    
                #Appending parent keys, to parents list for next layer
                parent_list.extend(parents)

            #Initializing nodes for next layer
            current_nodes = parent_list

        #Output dictionary of input vars with their df
        self.derivative = {}
        for key in list(in_vars.keys()):
            self.derivative[key] = graph[key]["df"]
        print("Derivatives Created")
if __name__ == '__main__':
    pass