# Combinatorial optimization for Mixed Reality Interfaces
Optional pre-reads:
- Lindlbauer. 2022. The future of mixed reality is adaptive (https://dl.acm.org/doi/10.1145/3558191)
- Oulasvirta. 2017. User Interface Design with Combinatorial Optimization (https://ieeexplore.ieee.org/document/7807191)


# Instructions
I used Conda for installing packages, and IntelliJ PyCharm as python IDE. Feel free to use any other software, but those are the ones I can support during class.

1. Conda: Download and install Anaconda (https://www.anaconda.com/)
2. Start command prompt with conda access
    - Mac: regular terminal
    - Windows: “Anaconda prompt”
4. Create new conda environment  
`conda create -n compint_summerschool python=3.9`
5. Activate new conda environment  
`conda activate compint_summerschool` 

6. Create new Python project in Pycharm, interpreter is <conda compint_summerschool>  
Run **01-interpreter_test.py** to make sure environment is working
Output should be “Interpreter is working”

7. Install python packages in conda environment (in command prompt or IDE)
  - **Opencv**
      - In conda environment run:  
      `pip install opencv-python`
      - Run **02-webcam-test.py** in IDE to make sure this was successful. You should see a live view from your webcam.
      Don’t see camera image on Macbook, check https://stackoverflow.com/a/64636035
      - Run **03-opencv-faces-test.py**. You should see a live view from your webcam with your face detected and marked through a blue box.
  - **Gurobi**
    - In conda environment run:   
    `conda config --add channels https://conda.anaconda.org/gurobi`  
    `conda install gurobi`  
    - Run 04-gurobi-test.py in IDE to make sure this was successful. Output should be somethingt like“Restricted license - for non-production use only - expires yyy”

**Useful hints**
- Open conda prompt and type conda info --envs to figure out which environments you have already created
