# Maze Generator

When I was a child, I remember some books where in each chapter, you had some choice to do: open the door, drink the potion, or go back. Depending on your choice, you were asked to go to page x, y or z.


Here, this generator does the same, but instead of a book, you will have `html` pages.
More precisely, a `<script>` and a `<div>` that you can include in your `html` page.

## Why ?

With a book, you can always cheat: move to another page and avoid dying. Here, you cannot. We use hashes!

## Jekyll

My personal website is built with [jekyll](https://jekyllrb.com/).
Therefore, the script generate three things:

- Mardown pages, with all included in it
- `<div>` that need to be stored in the jekyll' `_includes` folder
- `<script>` that need to be stored in the jekyll' `_includes` folder




# Running the Script

## Command


`python3 maze_generator.py graphs/test_graph.json maze_xxx`

In Jekyll, to avoid the `_includes` folder to be randomly organized, it is preferable to store the maze divs and scripts in a dedicated folder.
Here, you will need to create a `_includes/maze/` folder to store all your maze, and then a dedicated one to store this one `_includes/maze/maze_xxx/`.  
So, replace `maze_xxx` by a suitable name.

As it generates jekyll-markdown page, you can customize the header (`header.txt` is an example: check if the layout exists !).





## Examples Available

There are two examples in this repo:

- `graphs/test_graph.json`: this is a short file with nothing interesting here, but it helps to understand the selected dataformat
- `graphs/le_manoir.json`: this is the graph corresponding to "Le manoir de l'enfer", *Steve Jackson*, found online.

## How to Include your Files

Suppose you run:

`python3 maze_generator.py graphs/test_graph.json ABC`

You must have here:

```txt
gen/
    md/
	ABC/
	    <many .md files with a yaml header>

    include/
	ABC/
	    <many .txt files with div and scripts>
```

In your jekyll website, you need to move the files in such a way you get:

```txt
_includes/
    maze/
        ABC/
	    <many .txt files with div and script>

any/path/in/your/website/
			<many .md files with a yaml header>
```

# Demo

## Prototype

If you want to play, click [here](https://gaelle-candel.neocities.org/maze/manoir/) (french book, sorry for that!)

## How it Works ?

Take a look at [this post](https://gaelle-candel.neocities.org/book/2023/07/24/Maze.html) to see how it works.






