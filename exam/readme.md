# Exam Generator

Suppose you have some students.
You want them to do a quizz with 5 - 10 questions.
They will have their grade at the end of the quizz.

What you do not want is to allow student to hack your html page.
A naive implem would be "Question 1: Answer b, 2 points".
Therefore, a good cheating student would look at your javascript, and see which answer gives the points.

Here, we prevent this kind of cheating: we precompute overall answer hashes, and assign to each a score.

For more info, look at [my blog article](https://gaelle-candel.neocities.org/book/2023/07/25/Exam.html) on the topic.

# Script

`python3 QCM_generator.py inputs/graph_quant.json  --md5_path="md5.js"`

Here, we use the `md5.js` script within this folder to get the MD5 hash function available.

This file comes from this [blog](https://ourcodeworld.com/articles/read/1547/how-to-create-md5-hashes-in-javascript) / [Github](https://github.com/blueimp/JavaScript-MD5/tree/master/js)





# TODO

- [ ] Modify bokeh div style. This is way too small
