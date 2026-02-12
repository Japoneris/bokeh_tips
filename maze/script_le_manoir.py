"""
Part 1: Create hashes for all pages.
Export to keep track of it.

Part 2: Create bokeh div/script

"""

import argparse
import hashlib
import json
import os

import bokeh_gen_button as bgb

if __name__ == "__main__":
    parser = argparse.ArgumentParser("Generating a maze out of your story")
    parser.add_argument("graph", type=str, help="The input graph. Check the example.")
    parser.add_argument("name", type=str, help="Give a name to your folder.")
    parser.add_argument("--header", type=str, help="Path to the yaml header.",
                       default="header_manoir.txt")
    
    parser.add_argument("--seed", type=str, help="Seed for unique hashes.",
                       default="42")
    
    args = parser.parse_args()
    
    PATH_header = args.header

    # Create repository to generate pages.
    PATH_OUT = "gen/"
    book_ID = "{}/".format(args.name).replace("//", "/")
    
    os.makedirs(PATH_OUT, exist_ok=True)
    os.makedirs(PATH_OUT +   "md/" + book_ID, exist_ok=True)
    os.makedirs(PATH_OUT + "include/" + book_ID, exist_ok=True)
    
    
    # Load the graph
    
    graph = None
    with open(args.graph, "r") as fp:
        graph = json.load(fp)

    #print(graph)
    
    ##############
    # Gen hashes #
    ##############
    seed = args.seed
    
    dic_hash = {}
    for ID in graph:
        dic_hash[ID] = hashlib.md5((seed + str(ID)).encode()).digest().hex()
        
    print(json.dumps(dic_hash, indent=True))
    
    ###############
    # Gen buttons #
    ###############
    
    for ID, vals in graph.items():
        ID_hash = dic_hash[ID]
        
        next_LB = list(map(lambda x: x[1], vals["next"]))
        next_ID = list(map(lambda x: dic_hash[x[0]], vals["next"]))
        
        script, div = bgb.create_button_row(next_LB, next_ID)
        
        with open(PATH_OUT + "include/{}{}_div.txt".format(book_ID, ID_hash), "w") as fp:
            fp.write(div)
        
        with open(PATH_OUT + "include/{}{}_script.txt".format(book_ID, ID_hash), "w") as fp:
            fp.write(script)
            

    #############
    # Gen pages #
    #############
    
    data_header = None
    with open(PATH_header, "r") as fp:
        data_header = fp.read()
        
    for ID, ID_hash in dic_hash.items():
        
        include_div    = "{% include maze/" + book_ID + ID_hash + "_div.txt %}"
        include_script = "{% include maze/" + book_ID + ID_hash + "_script.txt %}"
        
        
        page = """{}
<center>
<h1> {} </h1>
</center>

{}

<center>
    {}
</center>

<html>
    {}
</html>
        """.format(data_header, ID, graph[ID]["text"], include_div, include_script)
        
        with open(PATH_OUT + "md/"+ book_ID  + ID_hash + ".md", "w") as fp:
            fp.write(page)
    
    #########
    # Index #
    #########
    page = """{}
    
This is where you journey start.

[Start !]({})

Or Go back to maze list [Link](/maze/)
    
    """.format(data_header, dic_hash["1"])
    
    with open(PATH_OUT + "md/"+ book_ID  + "index.md", "w") as fp:
            fp.write(page)
    
        
