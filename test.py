# [[print("*", end="") if j<i-1 else print("*") for j in range(i)] for i in range(1,int(input())+1)]
from utils.DataManager import DataManager

data = """1		10853	도전과창조-기업가정신	001		중핵	2	2	0	교양대학>>교양	1		미래520(목3,4)					ABCDF	김기선			
2		10853	도전과창조-기업가정신	002		중핵	2	2	0	교양대학>>교양	1		미래520(수5,6)					ABCDF	김기선			
3		10853	도전과창조-기업가정신	003		중핵	2	2	0	교양대학>>교양	1		미래520(목5,6)					ABCDF	김상준			
4		10853	도전과창조-기업가정신	004		중핵	2	2	0	교양대학>>교양	1		미래520(금5,6)					ABCDF	김상준			
5		10853	도전과창조-기업가정신	005		중핵	2	2	0	교양대학>>교양	1		미래521(수5,6)					ABCDF	김성민			
6		10853	도전과창조-기업가정신	006		중핵	2	2	0	교양대학>>교양	1		미래104(월7,8)					ABCDF	김영출	"""
print(DataManager.textToData(data))
data2 = "1		10853	도전과창조-기업가정신	001		중핵	2	2	0	교양대학>>교양	1		미래520(목3,4)					ABCDF	김기선			"
print(DataManager.check_splited_text(data2.split("\t")))