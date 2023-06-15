# CIX23:

## Setting Up Your Environment

 Create a virtual environment (optional, but recommended). This step helps isolate the dependencies of your notebooks from the system-level Python environment.

* You will find a guide 👉 [here](https://docs.conda.io/en/latest/miniconda.html) and [here](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/) on how to install Conda, as well as alternative methods for creating virtual environments on macOS, Windows and Linux:

### Creating a Conda Environment:
1. To create a new Conda environment, open a new command prompt or terminal and use the following command:
    ```sh
    conda create --name cix23 python=3.8
    ```
    Replace "cix23" with your desired environment name, 

2. Activate the new environment:
    * On macOS/Linux:
    ```sh
    conda activate cix23
    ```

    * On Windows:
    ```sh
    activate cix23
    ```
3. Install Requirements:

    First you need to install pipreqs library by running the following command:
    ```sh
    pip install pipreqs
    ```
    Now you can run the following command to install the required packages:

    ```sh
    pip install -r requirements.txt
    ```
    Once the installation is complete, all the packages specified in the requirements.txt file should be installed in your environment.


## Download resources for the tutorials
 *  Run the following command to download resources:

     ```sh
    wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1reyiD5YEmz6Z42J03GQG6-FDRUcrlF0W' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1reyiD5YEmz6Z42J03GQG6-FDRUcrlF0W" -O resources.zip && rm -rf /tmp/cookies.txt 
    ```
     Unzip resourses 

     ```sh
    unzip -q resources.zip
    ```

