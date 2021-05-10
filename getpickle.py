import pickle

final_spot_dict = {
    (772, 212, 945, 436): 1
}
with open('spot_dict.pickle', 'wb') as handle:
    pickle.dump(final_spot_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)