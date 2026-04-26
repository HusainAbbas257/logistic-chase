import pandas as pd
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LogisticRegression
from sklearn.multioutput import MultiOutputClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score
import joblib
from sklearn.pipeline import make_pipeline
print('libs loaded...')
# load
df=pd.read_csv(f'data/{input('enter file name->')}.csv')

df["dx"] = df["human x"] - df["ai x"]
df["dy"] = df["human y"] - df["ai y"]

df["dvx"] = df["human vx"] - df["ai vx"]
df["dvy"] = df["human vy"] - df["ai vy"]

x=df[["ai x", "ai y", "ai vx",'ai vy',"human x", "human y", "human vx",'human vy','dx','dy','dvx','dvy']].values
df["dist"] = ((df["dx"]**2 + df["dy"]**2)**0.5)
# for different directions
y=df[['up','left','down','right']]

print('data loaded...')


print('training...')
model = make_pipeline(StandardScaler(),MultiOutputClassifier(LogisticRegression(max_iter=500, solver='lbfgs')))
model.fit(x,y)
print('trained')
joblib.dump(model, f"models/{input('save to ->')}.pkl")
print('saved')

# removed the graph just because it was pointless
print('accuracy:',model.score(x,y))


# cross validation

scores = cross_val_score(model, x, y, cv=3)
print(scores)
print(scores.mean())