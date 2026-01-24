import pickle
import pandas as pd

print("Loading existing pickles...")
with open("df.pkl", "rb") as f:
    df = pickle.load(f)

with open("indices.pkl", "rb") as f:
    indices = pickle.load(f)

print("Converting to standard Python types...")
# Convert DataFrame to list of dicts
movies_list = df.to_dict("records")

# Convert Series to dict
indices_dict = indices.to_dict()

print("Saving optimized pickles...")
with open("movies_list.pkl", "wb") as f:
    pickle.dump(movies_list, f)

with open("indices_dict.pkl", "wb") as f:
    pickle.dump(indices_dict, f)

print("Done! Created movies_list.pkl and indices_dict.pkl")
