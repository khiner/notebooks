# Notebooks

These Jupyter notebooks, apart from a few random experiments, are attempts at comprehensive coverage of technical books to help me own the material as I read.

The parent folders are books, with usually one notebook per chapter. Almost all exercises are attempted and most have full solutions.
Most books also have a good amount of extra visualizations, explanations, experiments and animations.

I hope people get use out of these! Please create issues for any errors you find. Pull requests are very welcome :)

## Viewing the notebooks

To view these notebooks, I recommend using nbviewer. Simply add the GitHub path of the notebook like:

http://nbviewer.jupyter.org/github/${PATH}

For example,

http://nbviewer.jupyter.org/github/khiner/notebooks/blob/master/mathematics_of_the_dft/chapter_7_fourier_theorems_for_the_dft.ipynb

## Running the notebooks

Only Mac run instructions for now, but I believe running on Linux (and maybe even Windows?) should just require a different `pipenv` install.
Let me know via a GH issue if you run into problems here and I will fix.

### Mac

```bash
$ git clone git@github.com:khiner/notebooks.git && cd notebooks
$ xcode-select --install
$ brew install pipenv
$ pipenv install
$ pipenv shell
(notebooks)$ jupyter-notebook
```

I am taking a break from these notebooks as I don't have as much free time these days, but I hope to get back to these in earnest in the future.

