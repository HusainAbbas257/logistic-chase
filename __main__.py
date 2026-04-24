import src.game as game
import pandas as pd


df = pd.DataFrame(game.mainloop(input('type of opponent->')), columns=["ai x", "ai y", "ai vx",'ai vy',"human x", "human y", "human vx",'human vy','w','a','s','d','up','left','down','right'])

df.drop_duplicates(inplace=True)
print('data retrieved->',df.shape)
df.to_csv(f"data/{input('Enter file name to be saved in:->')}.csv", index=False)