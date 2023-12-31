# Inpost recruitment task

**The task should be performed according to the following information:** \
![image](https://github.com/Maksymilian-Plywaczyk/inpost-recruitment-task/assets/65869609/d0a72f31-8ed3-44fe-8dd6-ac27a9c99a10)

## Getting started
 1. Clone the repository from GitHub (using HTPS):\
	`git clone https://github.com/Maksymilian-Plywaczyk/inpost-recruitment-task.git`
 2. Create a virtual environment to isolate our package dependencies locally\
	 `python -m venv venv`\
	 `source venv/bin/activate` or on Windows `venv/Scripts/activate`
 3. Install list of dependencies from `requirements.txt`\
	`pip install -r requirements.txt`
 4. Feel free to use this app :)

## TODO LIST
**Task1**
 - [x] For a given model, check whether it is a laptop or a computer
desktop. Then calculate the "cost-effectiveness ratio", which
is represented by the equation inn the result, add the model name.
<p align="center">
$wskaźnik = {{ram + hd \over price} * speed}$
</p>

 **Task2**
 - [x] Create two promotional sets containing the sum of the price reduced by 10%
and information about the devices:
    -  PC + PRINTER
    -  LAPTOP + PRINTER

## Implementation
**Task1**
 - [x] I decide to round "cost-effectiveness ratio" to two decimal numbers, to avoid long numbers and get better visiualization of results.

 **Task2**
 - [x] Here I hope that my implementation will be transparent, because I decide to create three independent dataframes, with first, second products and promo price. I belive that this gives better visiualization and user which would like to check results can find very quickly what file presents.

In both cases, I'm trying to achieve future-proof concepts like: not defining just these two sets presents in requirement task, but user can make own sets with for example: PC+LAPTOP. 