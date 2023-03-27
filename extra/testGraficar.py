import pandas as pd
import matplotlib.pyplot as plt
data = [1,2,3,4,5]
test = pd.DataFrame (data,columns = ["numero"])
print (test)
test.plot()
plt.show()
