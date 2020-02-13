## Requirements:
1. Python 3
2. Tensorflow
3. Pandas
4. Seaborn
5. Keras
6. Matplotlib

## Getting Started:

1. Install miniconda to simplify everything
```bash
brew cask install miniconda
```

2. Install the required packages:
````bash
conda install -y pandas seaborn tensorflow==1.15 keras matplotlib jupyter
````

3. Pre process the data
```bash
python3 reset.py && \
python3 preprocessing.py && \
python3 aggregator.py
```

4. If you are running visual studio code
```bash
python3 -m pip install --upgrade pip && \
pip3 install jupyter
```
5. Run the actual model
```bash
python3 thesis.py
```