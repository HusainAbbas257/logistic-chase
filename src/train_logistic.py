import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LogisticRegression
import joblib
from sklearn.pipeline import make_pipeline
print('libs loaded...')
# load
df=pd.read_csv(f'data/{input('enter file name->')}.csv')

x=df[["ai x", "ai y", "ai vx",'ai vy',"human x", "human y", "human vx",'human vy']].values
# for different directions
ys=[df['up'].values,
    df['left'].values,
    df['down'].values,
    df['right'].values]

print('data loaded...')


print('training...')
models=[make_pipeline(PolynomialFeatures(degree=2),LogisticRegression()) for i in range(4)]
for i in range(4):
    models[i].fit(x,ys[i])
joblib.dump(models, f"models/{input('save to ->')}.pkl")
print('trained')

for y,model in zip(ys,models):
    plt.scatter(x[:,0], x[:,1], c=y)
    print('accuracy:',model.score(x,y))
    plt.show()