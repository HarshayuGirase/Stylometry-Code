import sys,os
import string

def get_cdf(L):
	fin=open('slice'+str(L)+'/author_keys.txt','r')
	aid_cnt={}
	for l in fin:
		split_str=l.rstrip('\n').split('\t')
		key=split_str[1]
		aid=key.split('_')[0]
		try:
			aid_cnt[aid]+=1
		except KeyError:
			aid_cnt[aid]=1
	fin.close()
	cdf=[0.0 for i in range(20)]
	for aid in aid_cnt:
		cnt=aid_cnt[aid]
		if cnt<20:
			cdf[cnt]+=1
	for i in range(1,20):
		cdf[i]=cdf[i]+cdf[i-1]
	for i in range(20):
		cdf[i]=cdf[i]/len(aid_cnt)
	return cdf

def main():
	cdf_200=get_cdf(200)
	cdf_500=get_cdf(500)
	cdf_800=get_cdf(800)
	fout=open('cdf_article_slice_cnt.txt','w')
	for i in range(20):
		fout.write(str(i)+'\t'+str(cdf_200[i])+'\t'+str(cdf_500[i])+'\t'+str(cdf_800[i])+'\n')
	fout.close()
if __name__ == '__main__':
	main()