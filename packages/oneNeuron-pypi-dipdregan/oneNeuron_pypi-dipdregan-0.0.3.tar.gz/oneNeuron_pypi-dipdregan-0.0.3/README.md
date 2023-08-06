# oneNeuron_pypi

## another -: 
##### Dipendra Pratap
## create direcotry inside directory
```bash
mkdirs src/oneNeuron
```
## create direcotry inside directory the directory create another directory
```bash
mkdirs -p src/oneNeuron
```
### create file inside directory 
```bash
touch src/oneNeuron/perceptron.py
```

# oneNeuron_pypi
oneNeuron_pypi



## How to use this

```python
from oneNeuron.perceptron import Perceptron

## get X and y and then use below commands
model = Perceptron(eta=eta, epochs=epochs)
model.fit(X, y)
```

# Reference -
[official python docs](https://packaging.python.org/tutorials/packaging-projects/)

[github docs for github actions](https://docs.github.com/en/actions/guides/building-and-testing-python#publishing-to-package-registries)