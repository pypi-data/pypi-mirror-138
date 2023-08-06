# calcalc
This is a calculator for evaluating string expressions (e.g. '2*sin(3/5)', 'mass of the sun in kg'). The statement can be computed either locally or through querying WolframAlpha. 

To install using pip: `pip install calcalc-toy`. There are two ways to interact:

### Usage 1: from command line

Examples (inside the `CalCalc` folder): 

This command evaluate a simple expression locally with the `-s` argument:

```bash
$ python CalCalc.py -s '2*sin(3)'
0.2822400161197344
```

This command calculates the mass of the moon through Wolfram with the `-w` argument. The result is displayed as a plain text:

```bash
$ python CalCalc.py -w 'mass of the moon in kg'
7.3459×10^22 kg (kilograms)
```

If we want to display a float instead, use the `--float` flag:

```bash
$ python CalCalc.py -w 'mass of the moon in kg' --float
7.3459e+22
```

### Usage 2: inside python script/ipython

After `pip install`, import the calculator like this:

```python
from calcalc.CalCalc import calculate
```

We can evaluate a simple expression locally:

```python
In [1]: calculate('2*sin(3/5)+log(7)')
Out[2]: 3.075195095845384
```

We can evalute a Wolfram query using `local=False`:

```python
In [1]: calculate('mass of the moon in kg', local=False)
Out[2]: 7.3459e+22
```

The default Wolfram output using python script/ipython is converted float to facilitate further computations (opposite to the command line behavior described above). To display a string instead, use `return_float=False`:

```python
In [1]: calculate('mass of the moon in kg', local=False, return_float=False)
Out[2]: '7.3459×10^22 kg (kilograms)'
```

