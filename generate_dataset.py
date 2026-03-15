import pandas as pd
import numpy as np
np.random.seed(42)
data=[]
for i in range(1000):
    left=np.random.randint(0,100)
    right=np.random.randint(0,100)
    front=np.random.randint(0,100)
    speed=np.random.randint(0,100)
    if front<15:
        action="stop"
    elif left<right:
        action="right"
    elif right<left:
        action="left"
    else:
        action="forward"
    data.append([left,right,front,speed,action])
df=pd.DataFrame(data,columns=["left_sensor","right_sensor","front_sensor","speed","action"])
df.to_csv("dataset.csv",index=False)
print("Data set generated Successfully")
