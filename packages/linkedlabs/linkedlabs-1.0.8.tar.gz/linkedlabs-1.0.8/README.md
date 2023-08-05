# linkedlabs
This project is created as a Generic solution to find most similar rows(or customers) in a given dataset using DNA matching Algorithms and Artificial Intelligence.

# Installation
Run the following to install:

```python
pip install linkedlabs
```

## Usage

```python
from linkedlabs import get_similarities
import pandas as pd
df = pd.read_pickle("your_pandas_dataframe.pkl") ## Any pandas dataframe
similarity_df = get_similarities(df)
```