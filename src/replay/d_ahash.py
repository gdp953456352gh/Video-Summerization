#encoding:utf-8
import cv2
import numpy as np

#��ֵ��ϣ�㷨
def aHash(img):
    #����Ϊ8*8
    img=cv2.resize(img,(8,8),interpolation=cv2.INTER_CUBIC)
    #ת��Ϊ�Ҷ�ͼ
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    #sΪ���غͳ�ֵΪ0��hash_strΪhashֵ��ֵΪ''
    s=0
    hash_str=''
    #�����ۼ������غ�
    for i in range(8):
        for j in range(8):
            s=s+gray[i,j]
    #��ƽ���Ҷ�
    avg=s/64
    #�Ҷȴ���ƽ��ֵΪ1�෴Ϊ0����ͼƬ��hashֵ
    for i in range(8):
        for j in range(8):
            if  gray[i,j]>avg:
                hash_str=hash_str+'1'
            else:
                hash_str=hash_str+'0'            
    return hash_str
#��ֵ��֪�㷨
def dHash(img):
    #����8*8
    img=cv2.resize(img,(9,8),interpolation=cv2.INTER_CUBIC)
    #ת���Ҷ�ͼ
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    hash_str=''
    #ÿ��ǰһ�����ش��ں�һ������Ϊ1���෴Ϊ0�����ɹ�ϣ
    for i in range(8):
        for j in range(8):
            if   gray[i,j]>gray[i,j+1]:
                hash_str=hash_str+'1'
            else:
                hash_str=hash_str+'0'
    return hash_str
#Hashֵ�Ա�
def cmpHash(hash1,hash2):
    n=0
    #hash���Ȳ�ͬ�򷵻�-1�����γ���
    if len(hash1)!=len(hash2):
        return -1
    #�����ж�
    for i in range(len(hash1)):
        #�������n����+1��n����Ϊ���ƶ�
        if hash1[i]!=hash2[i]:
            n=n+1
    return n
img1=cv2.imread('1.png')
img2=cv2.imread('2.png')
hash1= aHash(img1)
hash2= aHash(img2)
print(hash1)
print(hash2)
n=cmpHash(hash1,hash2)
print('��ֵ��ϣ�㷨���ƶȣ�',n)
hash1= dHash(img1)
hash2= dHash(img2)
print(hash1)
print(hash2)
n=cmpHash(hash1,hash2)
print('��ֵ��ϣ�㷨���ƶȣ�',n)