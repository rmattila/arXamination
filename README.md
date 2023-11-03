# prompt-arXamination

Efficiently perform a first-pass examination of arXiv papers for essential research quality indicators

## Installation

Clone the repository:

```shell
git clone https://github.com/rmattila/prompt-arXamination.git 
```

Navigate to the project directory:

```shell
cd prompt-arXamination 
```

Create a virtual environment (optional but recommended):

```shell
conda create -n arxamination-env
conda activate arxamination-env
```

Install the project's dependencies:

```shell
pip install -r requirements.txt
```

Next, install the arxamination package itself. This step is necessary for users who want to run the command-line tool:

```shell
pip install .
```

## Usage

Run the arxamination tool with the arXiv article ID as a command-line argument. For example:

```shell
arxamination 1706.03762
```

This command-line tool will fetch and analyze the specified arXiv article.