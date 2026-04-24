import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import joblib

print('libs loaded...')
# load
df=pd.read_csv(f'data/{input('enter file name->')}.csv')

x=df[["ai x", "ai y", "ai vx",'ai vy',"human x", "human y", "human vx",'human vy','w','a','s','d']].values
# for different directions
ys=[df['up'].values,
    df['left'].values,
    df['down'].values,
    df['right'].values]

print('data loaded...')



print('training...')
models=[LogisticRegression(max_iter=5000) for i in range(4)]
for i in range(4):
    models[i].fit(x,ys[i])
joblib.dump(models[i], f"models/{input('save to ->')}.pkl")
print('trained')

for y,model in zip(ys,models):
    plt.scatter(x[:,0], x[:,1], c=y)
    print('accuracy:',model.score(x,y))
    plt.show()