# Sun Yield Calculator



In this repo, we provide some tools to:

- calculate yield of a solar panel given its angle; 
- calculate shade location given a sun angle.


You can check my related posts to get the associated explanations / equations used there:

- [I: Understanding sun angles](https://japoneris.neocities.org/tech/2022/08/11/Sun_1_trajectories.html)
- [II: Theoreticla yields](https://japoneris.neocities.org/tech/2022/08/11/Sun_2_panel_orientation.html)
- [III: "True" solar panel efficiency](https://japoneris.neocities.org/tech/2022/08/11/Sun_3_true_SP_efficiency.html)
- [IV: Shade from the trees](https://japoneris.neocities.org/tech/2022/08/11/Sun_4_shade_from_trees.html)


If you find any mistakes, feel free to contact me / suggest your corrections.



# Running the code

## Repo structure

The `.html` are already saved in the folder `/html/`.

In the `/scripts/` folder, you will find the scripts used to generate them, if you want to modify them for your own purpose.

Each script will output its corresponding `.html` directly into the corresponding folder.
To run them without error, please do:

1. `cd scripts/`
2. `python3 <my_bokeh_script.py>`

Because the scripts use the `bokeh.plotting.show()`, this will open directly the `.html` in your browser.


## Dependencies 

These tools are generated with `python3` and `bokeh`, leading to `js` objects embedded in an `.html`.

We do simple math using `numpy`, so any version may work.

[Bokeh](https://docs.bokeh.org/en/latest/) is a very nice visualization library.




# Sources 


[Photovoltaic Education](https://www.pveducation.org/pvcdrom/welcome-to-pvcdrom): A great source to learn about sun, in many aspects.
