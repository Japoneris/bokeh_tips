"""
Everything in.

1. Load the graph
2. Generate hashes 
3. Create the bokeh buttons
4. Create the html
5. Add the md5 script in.
6. Save the file 
7. Include
"""

import argparse
import json
import hashlib
import os

import numpy as np


from bokeh.models    import RadioGroup, RadioButtonGroup, CustomJS, Button, Div
from bokeh.layouts   import column, row

# For export
from bokeh.resources import CDN
from bokeh.plotting  import figure, output_file, show
from bokeh.embed import file_html, components


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser("QCM generator")
    parser.add_argument("file")
    parser.add_argument("--title", default="test", type=str, 
                        help="HTML page name")
    parser.add_argument("--md5_path", default="/assets/js/md5.js", type=str,
            help="Where your md5 will be located in jekyll website")
    parser.add_argument("--seed", default="", type=str, 
                        help="Add a seed to prevent hash computability")
    args = parser.parse_args()
    
    ####################
    # Getting the file #
    ####################
    
    filename = args.file
    data = None
    with open(filename, "r") as fp:
        data = json.load(fp)
    
    n_question = len(data)
    print("Recovered {} questions".format(n_question))
    
    ########################
    # Computing the hashes #
    ########################
    
    
    
    n_answer = list(map(lambda x: len(x["answers"]), data))
    n_tot = np.prod(n_answer) # Number of different values
    v_good = list(map(lambda x: x["good"], data))
    
    def get_list(v):
        """
        From a number, return its decomposition.
        Do not modify location, as it uses components written just above
        
        :param v: integer
        :rparam: list of integer
        """
        lst = []
        for i in n_answer:
            lst.append(v%i)
            v = v//i

        return lst

    dic_scores = dict([(c, []) for c in range(n_question+1)])
    
    for i in range(n_tot):
        lst = get_list(i)
        # Get the score
        s = sum(map(lambda x: x[0] == x[1], zip(lst, v_good)))
        
        lst_str = str(lst)[1:-1].replace(" ", "")
        lst_hash = hashlib.md5(lst_str.encode()).digest().hex()
        
        dic_scores[s].append(lst_hash)
        
    #print(json.dumps(dic_scores, indent=True))
    
    ######################
    # Gen Bokeh Elements #
    ######################

    # Define Bokeh elements
    
    div = Div(text="""This is the start of the challenge.""",
        width=500, height=100,
        css_classes=["custom_bokeh_div"])
    
    radio_group = RadioGroup(labels=["Start !"], active=0)
    radio_group.js_on_change("active", CustomJS(code="""
        console.log('radio_group: active=' + this.active, this.toString())
    """))

    button_next = Button(label="OK", button_type="primary")
    
    counter = [-1] # Trick to get something modifiable in bokeh
    
    # Define Javascript Code 

    code_v2 = """
        
        var i = counter[0];
        
        
        if ((i >= 0) & (i < answers.length)) {
            var x = radio.active
            results[i] = x;
        }
        
        i = i+1;
        
        // Update radio buttons and question
        if ((i >= 0) & (i < answers.length)) {
            
            radio.labels = answers[i]; 
            div.text = text[i];
        
        } else if (i == answers.length) {
            radio.labels = []
            console.log(results)
            
            var x = md5(results)
            console.log(x)
            
            
            var score = 0;
            for (var j=0; j< hash_lists.length; j++) {
                if (hash_lists[j].includes(x)) {
                score = j;
                }
            }
            
            console.log("Score: ", score)
            
            var ttt = "<center> This is the end of the challenge <br>"
            ttt = ttt + "you obtained <h2>" + score + "</h2>"
            ttt = ttt + "<br> Click to get back to the start </center>"

            div.text = ttt;
            
            
        } else {
            radio.labels = []
            div.text = "This is the beginning of the challenge";
            i = -1
        }

        counter[0] = i;

    
    """
    
    code = """


    var x = radio.active
    console.log(x)

    var i = counter[0];
    if (i < answers.length) {
        results[i] = x;
    }

    // update
    i = i + dc;

    counter[0] = i;
    console.log('Counter:' + counter)

    if (i >= text.length) {
        // Cycle back to zero
        counter[0] = 0;
        i = 0;
    }

    // Update text in the main div
    div.text = text[i];


    if (i >= answers.length) {
        radio.labels = [];
        console.log(results)
        var x = md5(results)
        console.log(x)

    } else {
        radio.labels = answers[i]; // Change the labels
        }

    //window.open("https://some.url.com");

    """

    # Give input material
    
    text_questions = list(map(lambda x: x["text"], data))
    text_answers   = list(map(lambda x: x["answers"], data))
    results = [0 for _ in range(n_question)] # Vector to store results

    dico = {"radio": radio_group, 
              "div": div,
            "counter": counter,
              "text": text_questions,
            "answers": text_answers,
            "hash_lists": list(dic_scores.values()),
            "results": results
             }
    
    # Add interaction
    button_next.js_on_click(CustomJS(args=dico, code=code_v2))
    
    filename = "QCM_{}.html".format(args.title)
    output_file(filename=filename)

    show(column([div, radio_group, button_next]))

    ##############
    # Add md5.js #
    ##############
    # NOTE: The path may change for you !!! 

    page = None
    with open(filename, "r") as fp:
        page = fp.read()

    i = page.find("</head>")
    
    page = page[:i] + """
    <script type="text/javascript" src="{}"></script>
    """.format(args.md5_path) + page[i:]
    

    with open(filename, "w") as fp:
        fp.write(page)
