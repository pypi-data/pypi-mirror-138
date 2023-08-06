# jutge
This is CLI judge to validate SQL and Java exercises.

It runs the provided code in a docker dedicated docker container and 
runs some tests to validate its correctness.

It supports:
- Output comparison.
- Unit tests (Only SQL for now).
- JSON results.
- Git integration.
    - Use Git tag.
    - Deadlines (using commit date).

## Install requeriments
```bash
git clone https://github.com/joapuiib/jutge jutge-joapuiib
python3.8 -m pip install jutge-joapuiib
```

## Example usage

```bash
$ check_repo.py -d dir/ repositories.csv

$ grade_repo.py testcase_file.yml directory/
```

## TODO
- Installation and usage
- Testcase files documentation
- YAML validators for each judge
- Jutge version requeriment in tests file
### SQL Judge
- Normalize output new line endings
- run\_object instead of run\_exercise and run\_test
