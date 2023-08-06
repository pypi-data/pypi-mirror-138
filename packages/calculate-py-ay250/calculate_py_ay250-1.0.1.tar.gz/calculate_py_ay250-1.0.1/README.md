# calculate_py_ay250
Project that evaluates mathematical expressions, including calls to the wolfram alpha api. 
Built for UC Berkeley's AY 250 python data science course.

Main function is calculate, which can be called in two ways. First, from the command line:

```bash
$ python CalCalc.py -w 'mass of the moon in kg'
7.3459e+22
```

AND, from within Python

```python
>>> from CalCalc import calculate
>>> calculate('mass of the moon in kg',  return_float=True) * 10
>>> 7.3459e+23

