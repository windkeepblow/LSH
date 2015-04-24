#-*- coding:utf-8 -*-
#Locality-Sensitive Hashing for cosine simialrity

import random
import sys
import math

class LSH:
    def __init__(self, base_vec_num, iter_num, dimens):
        self._base_vec_num = base_vec_num #基向量的数量, 空间切分的区间数量 = 2^(self._base_vec_num)
        self._iter_num = iter_num #进行多少轮的lsh操作, 避免误杀
        self._dimens = dimens #输入向量的维度 
    
        self._base_vec_li = [] #基向量, 每个元素是一组基向量
        self._hash_bucket_li = [] #hash桶, 每个元素是一组hash桶

    def build_lsh(self, vec_dict):
        sys.stderr.write("building base_vecs...\n")
        for i in range(self._iter_num):
            vec_li = []
            for j in range(self._base_vec_num):
                v = [(random.random()*2-1) for k in range(self._dimens)]
                vec_li.append(v)
            self._base_vec_li.append(vec_li)
            self._hash_bucket_li.append({})

        sys.stderr.write("hashing...")
        count = 0
        for name in vec_dict:
            for i in range(self._iter_num):
                hashKey = self.get_hash_key(self._base_vec_li[i], vec_dict[name])
                if hashKey in self._hash_bucket_li[i]:
                    self._hash_bucket_li[i][hashKey].add(name)
                else:
                    self._hash_bucket_li[i][hashKey] = set([name])
            count += 1
            if count % 100 == 0:
                sys.stderr.write("\rhashing...%d"%(count))
                sys.stderr.flush()
        sys.stderr.write("\n")

    def get_hash_key(self, base_vec, input_vec):
        hashKey = ""
        for k in base_vec:
            simi = self.similarity(input_vec, k)    
            if simi > 0:
                hashKey += "a" 
            else:
                hashKey += "b" 
        return hashKey 

    #To return the candidate set of names. Be careful about that it's possible to be empty.
    def get_candidate_set(self, vector):
        candi_names = set([])
        for i in range(self._iter_num):
            hashKey = self.get_hash_key(self._base_vec_li[i], vector)
            if hashKey in self._hash_bucket_li[i]:
                candi_names = candi_names | self._hash_bucket_li[i][hashKey]
        return candi_names 

    #cosine similarity
    #d1, d2 should not be 'zero vector'
    def similarity(self, d1, d2):
        hit = sum([(d1[i]*d2[i]) for i in range(len(d1))]) + 0.0
        sum1 = math.sqrt(sum([d1[k]*d1[k] for k in range(len(d1))]))
        sum2 = math.sqrt(sum([d2[k]*d2[k] for k in range(len(d2))]))
        if sum1 == 0 or sum2 == 0:
            return 0.0
        return hit / (sum1 * sum2)
