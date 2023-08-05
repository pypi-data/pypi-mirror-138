# Grade Mage

Auto grader for online quiz.

Use the following command to ensure all the tests are passed:

```
pytest
```

Then execute the following command t generate the wheel:

```
python3 setup.py sdist bdist_wheel
```

Upload the module to test server:

```
python3 -m pip install --upgrade twine
python3 -m twine upload --skip-existing --repository testpypi dist/*
```

Distribute the module to production server:

```
python3 -m twine upload --repository pypi dist/*
```