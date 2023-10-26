# Delete inconsistencies of the INGV's node with DWG

This script performs a series of database operations to synchronize two sets of station items, one from 'DGW' and the other from 'INGV'. The main goal is to ensure that the station items in both databases are consistent, and any differences are addressed, by deleting repeated station items from the INGV node.

## Installation

Clone and change into the repository using `git clone https://github.com/DuarteArribas/correctIngvNode`, `cd correctIngvNode`. Make sure you have Python (this project was built for version 3.11.4, but older should still work) installed and pip as well.

Install the requirements in requirements.txt using `pip install -r requirements.txt`.

## Before running

Before running the program, make sure you edit the `conf.cfg` file with the appropriate IP, Database Name, Username and Password of the respective servers.

## Running

To run the program, type:

```python
python correctIngvNode.py [-h] [-d]

h | Help : Display help and usage
d | Delete : Remove files (Default is to display the planned removal only)
```

If ran without the `-d` flag, it will only print and save to a `commands` file, the planned removal. To actual remove files, the `-d` flag should be used.

## Troubleshooting

If you have trouble installing `psycopg2`, I did too! In that case, please also install the following if you haven't already:

```bash
sudo apt install libpq-dev python3-dev
sudo apt install build-essential
```

It worked for me [src](https://stackoverflow.com/questions/5420789/how-to-install-psycopg2-with-pip-on-python).
