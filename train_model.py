import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
data=pd.read_csv("dataset.csv")
X=data[["left_sensor","right_sensor","front_sensor","speed"]]
y=data["action"]
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=42)
models={"Logistic Regression":LogisticRegression(max_iter=200),"Decision Tree":DecisionTreeClassifier(),"Random Forest":RandomForestClassifier()}
best_model=None
best_accuracy=0
for name,model in models.items():
    model.fit(X_train,y_train)
    predictions=model.predict(X_test)
    acc=accuracy_score(y_test,predictions)
    print(name,"Accuracy:",acc)
    if acc>best_accuracy:
        best_accuracy=acc
        best_model=model
pickle.dump(best_model,open("car_model.pkl","wb"))
print("Best Model saved")