# %%
import matplotlib.pyplot as plt
import numpy as np
# %%
n = 1000
x = list(np.random.uniform(0, 10, int(.25*n)))
# %%

vals = np.arange(20, 110, 10)
for i in range(0, len(vals)-1, 1):
    low = vals[i]
    high = vals[i-1]
    amt = np.random.randint(5, 18)/100



# %%
