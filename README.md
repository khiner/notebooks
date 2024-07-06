# Notebooks

These Jupyter notebooks, apart from a few random experiments, are attempts at comprehensive coverage of technical books to help me own the material as I read.

The parent folders are books, with usually one notebook per chapter. Almost all exercises are attempted and most have full solutions.
Most books also have a good amount of extra visualizations, explanations, experiments and animations.

I hope people get use out of these! Please create issues for any errors you find. Pull requests are very welcome :)

## Viewing the notebooks

To view and run these notebooks, I recommend using [colab](https://colab.research.google.com). Simply add the GitHub path of the notebook like:

https://colab.research.google.com/github/${PATH}

For example,

https://colab.research.google.com/github/khiner/notebooks/blob/master/mathematics_of_the_dft/chapter_7_fourier_theorems_for_the_dft.ipynb

_Note: These notebooks are all best viewed in light mode (not dark mode)_

## Running the notebooks

Only Mac run instructions for now, but I believe running on Linux (and maybe even Windows?) should just require a different `pipenv` install.
Let me know via a GH issue if you run into problems here and I will fix.

### Mac

```bash
$ git clone git@github.com:khiner/notebooks.git && cd notebooks
$ git submodule update --init --recursive
$ pip install -r requirements.txt
$ jupyter-notebook
```
