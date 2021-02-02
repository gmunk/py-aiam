# py-aiam

## Introduction

An unofficial implementation of the algorithms and data-structures presented in the seminal work on 
artificial intelligence–**Artificial Intelligence: A Modern Approach**.

This project does not aim to do a better job than what is already done in the official repository
complementing the book, the code here is more like an educational enterprise, a playground even.

The plan is to go through the book and implement all the various algorithms and data-structures presented,
the official codebase is occasionaly referenced to help development 
but in general the code here is as unique as possible.

## Implemented Algorithms

| Algorithm / Data-structure          | Implementation | Test                |
| ----------------------------------- | -------------- | ------------------- |
| Table Driven Agent                  | ✅             | ✅                 |
| Reflex Vacuum Agent                 | ✅             | ✅                 |
| Simple Reflex Agent                 | ✅             | ✅                 |
| Best-first Search (Uniform-cost)    | ✅             | ✅                 |
| Breadth-first Search                | ✅             | ✅                 |
| Depth-first Search                  | ✅             | ✅                 |
| Depth-limited Search                | ✅             | ✅                 |
| Iterative-deepening Search          | ✅             | ✅                 |
| Bidirectional best-first Search     | ❌             | ❌                 |


## Tests
This project aims to cover its codebase with unit tests which are the recommended way to experiment and 
actually confirm what was implemented. Testing relies on the built-in unittest module.

In order to run the project's tet suite do the following:

1. Clone this repository
2. `cd /path/to/where/you/cloned/the/repo`
3. `python -m unittest`