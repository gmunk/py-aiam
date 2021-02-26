# py-aiam

## Introduction

An unofficial implementation of the algorithms and data-structures presented in the seminal work on 
artificial intelligence–**Artificial Intelligence: A Modern Approach**.

This project does not aim to do a better job than what is already done in the official repository
complementing the book, the code here is more like an educational enterprise, a playground even.

The plan is to go through the book and implement all the various algorithms and data-structures presented,
the official codebase is occasionaly referenced to help development 
but in general the code here is as unique as possible.

## Requirements and Set-up guide
The project requires **python 3**, it will **not work on python 2**, since python 2 is no longer supported that shouldn't be a
big issue. The precise version that the project is being developed on is 3.9.1. This is a fairly recent one (in Q1/2021), 
but it is possible that the code will work on older versions. There is a plan to test with other versions, when that happens
this section will be updated.

The following table shows which versions of python have been tested.

| **Version** | **Status** |
| ----------- | ---------- |
| 3.9.1       | ✅         |

The easiest and cleanest way to install 3.9.1 is to use **pyenv and pyenv-virtualenv**. After these two are installed,
clone this repository and follow the steps below.

Install python 3.9.1 with pyenv 

`pyenv install 3.9.1`

Create a new virtualenv, associated with the newly installed 3.9.1

`pyenv virtualenv 3.9.1 py-aiam-3.9.1`

Go to where you cloned this repository 

`cd <where-this-repo-was-clonse>`

Set the local version and environment for this folder.

`pyenv local py-aiam-3.9.1`

Right now the code does not have any dependencies, if that changes, this guide will be updated.

## Implemented Algorithms

| **Algorithm / Data-structure**          | **Implementation** | **Test**                | **Location**                                             |
| --------------------------------------- | ------------------ | ----------------------- | -------------------------------------------------------- |
| Table Driven Agent                      | ✅                 | ✅                     | [agent.py](agent.py)                                      |
| Reflex Vacuum Agent                     | ✅                 | ✅                     | [agent.py](agent.py)                                      |
| Simple Reflex Agent                     | ✅                 | ✅                     | [agent.py](agent.py)                                      |
| Best-first Search (Uniform-cost)        | ✅                 | ✅                     | [uninformed_search.py](search/uninformed_search.py)       |
| Uniform-cost Search                     | ✅                 | ✅                     | [uninformed_search.py](search/uninformed_search.py)       |
| Breadth-first Search                    | ✅                 | ✅                     | [uninformed_search.py](search/uninformed_search.py)       |
| Depth-first Search                      | ✅                 | ✅                     | [uninformed_search.py](search/uninformed_search.py)       |
| Depth-limited Search                    | ✅                 | ✅                     | [uninformed_search.py](search/uninformed_search.py)       |
| Iterative-deepening Search              | ✅                 | ✅                     | [uninformed_search.py](search/uninformed_search.py)       |
| Bidirectional best-first Search         | ✅                 | ❌                     | [uninformed_search.py](search/uninformed_search.py)       |
| Genetic algorithm                       | ✅                 | ✅                     | [complex_search.py](search/complex_search.py)             |


## Tests
This project aims to cover its codebase with unit tests which are the recommended way to experiment and 
actually confirm what was implemented. Testing relies on the built-in unittest module.

In order to run the project's tet suite do the following:

1. Clone this repository
2. `cd /path/to/where/you/cloned/the/repo`
3. `python -m unittest`