from lsh import LSH
import cPickle as pickle

model = LSH(base_vec_num=3, iter_num=2, dimens=2)
vec_dict = {
    "a":[0.1,0.2],
    "b":[0.5,-0.2],
    "c":[-0.3,-0.1],
    "d":[1.0,0.0],
    "e":[-3,2],
    "f":[2,2]
}
model.build_lsh(vec_dict)
for name in model.get_candidate_set([0.3,0.9]):
    print name,
print ""

with open("model.pkl", 'wb') as fout:
    pickle.dump(model, fout)

with open("model.pkl", 'rb') as fin:
    dumped_model = pickle.load(fin)
    print "dumped model:"
    for name in dumped_model.get_candidate_set([0.3,0.9]):
        print name,
    print ""
