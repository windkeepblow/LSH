from lsh import LSH

model = LSH(3, 2, 2)
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
