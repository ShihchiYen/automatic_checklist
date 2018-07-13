import time

#建立班別的清單變數
schedule = {}
#建立出勤資料的清單變數
attendance = {}
#建立班表的字典變數
shift = {}

final = []

year = input("請輸入比對年份: ")
month = input("請輸入比對月份(1-12): ")
daystart = input("請輸入比對起始日: ")
dayend = input("請輸入比對結束日: ")
datelen = len(month) + len(dayend) + 6

#打開班別檔案
with open("schedule.txt", "r") as f:
	#將班別檔案整理成一個名叫schedule的字典，範例{班別:{in或out:時間}}}，放進schedule裡
	for d in f:
		#將班別全改為大寫，刪除最後的換行符號
		temporary = d.upper().strip("\n")
		#open開啟的檔案都為字串型別，將型別轉為清單，\t為分隔符號
		temporary = temporary.split("\t")
		#在schedule字典中該班別下建立c/in字典
		schedule[temporary[0]] = {"c/in":temporary[1]}
		#在schedule字典中該班別下建立c/out字典
		schedule[temporary[0]]["c/out"] = temporary[2]
		#刪除用不到的變數
		del temporary
# print(schedule.keys())
# print(schedule["A"])

#打開出勤資料
with open("attendance.txt", "r") as f:
	#將出勤資料整理成一個名叫attendance的字典，範例{部門:{姓名:(日期, 打卡紀錄)}}，放進attendance裡
	for d in f:
		#將出勤資料全改為大寫，刪除最後的換行符號
		temporary = d.upper().strip("\n")
		#open開啟的檔案都為字串型別，將型別轉為清單，\t為分隔符號
		temporary = temporary.split("\t")
		#將打卡紀錄的日期複製出來，刪除前後空白，插入成為第三個元素
		temporary.insert(2,temporary[2][0:datelen].strip())

		#如果在attendance沒有該部門的key，建立{部門:{姓名:(日期, 打卡紀錄)}}，日期與打卡記錄是清單
		if temporary[0] not in attendance:
			attendance[temporary[0]] = {temporary[1]:[temporary[2]]}
			attendance[temporary[0]][temporary[1]].extend([temporary[3]])
		#如果在attendance的該部門下，沒有該姓名的key，建立{姓名:(日期, 打卡紀錄)}，日期與打卡記錄是清單
		elif temporary[1] not in attendance[temporary[0]]:
			attendance[temporary[0]][temporary[1]] = [temporary[2]]
			attendance[temporary[0]][temporary[1]].extend([temporary[3]])
		#attendance裡有該部門，且已有該姓名的key，建立(日期, 打卡紀錄)，日期與打卡記錄是清單
		else:
			attendance[temporary[0]][temporary[1]].extend([temporary[2]])
			attendance[temporary[0]][temporary[1]].extend([temporary[3]])
		#刪除用不到的變數
		del temporary
# print(attendance.keys())
# print(attendance["OUR COMPANY"].keys())
# print(attendance["OUR COMPANY"]["HANNAH"])

#打開班表
with open("shift.txt", "r") as f:
	#將班表整理成一個名叫shift的字典，範例{名字:{日期:班別}}，放進shift裡
	for d in f:
		#將班表全改為大寫，刪除最後的換行符號
		temporary = d.upper().strip("\n")
		#open開啟的檔案都為字串型別，將型別轉為清單，\t為分隔符號
		temporary = temporary.split("\t")
		#為了在班表裡，將每個人的班別都加上日期，所需數字變數
		number = int(daystart) - 1
		#為班表中每個人建立一個暫時的字典
		dicttemp = {}
		#將日期為key，班別為值，放進暫時字典
		for a in temporary[int(daystart):int(dayend)+1]:
			number += 1
			#將日期為key，班別為值，放進暫時字典
			dicttemp[month + "/" + str(number) + "/" + year] = a
		#用每個人的名字當作key，日期與班別組成的字典當作值放入shift
		shift[temporary[0]] = dicttemp
		#刪除用不到的變數
		del number; del dicttemp; del temporary
# print(shift.keys())
# print(shift["ZOE"])

#從attendance拿出部門
for a in attendance:
	coutstamp = 0
	#從attendance[a]拿出姓名
	for b in attendance[a]:
		indextemp = -1
		#從attendance[a][b]拿出日期
		for c in attendance[a][b][0:len(attendance[a][b]):2]:
			#如果目前拿出姓名存在shift裡
			if b in shift:
				indextemp += 2
				barray = time.strptime((attendance[a][b][indextemp]), "%m/%d/%Y %I:%M:%S %p")
				bstamp = int(time.mktime(barray))
				# if len(schedule[shift[b][c]]["c/in"]) < 10:
				# 	#今天休假
				# 	final.append([a, b, c, shift[b][c], "\n"])
				if coutstamp != 0:
					if coutstampdown < bstamp < coutstampup:
						if bstamp >= coutstamp:
							#下班正常
							final.append([a, b, attendance[a][b][indextemp], yestodayshift, "c/out", "\n"])
							continue
						else:
							#下班早退
							final.append([a, b, attendance[a][b][indextemp], yestodayshift,"c/out", "早退" + str(abs(int((coutstamp - bstamp)/60))) + "分鐘\n"])
							continue
				if len(schedule[shift[b][c]]["c/in"]) >= 10:
					yestodayshift = shift[b][c]
					cin = c + " " + schedule[shift[b][c]]["c/in"]
					cinarray = time.strptime(cin, "%m/%d/%Y %I:%M:%S %p")
					cinstamp = int(time.mktime(cinarray))
					cinstampup = cinstamp + 12600
					cinstampdown = cinstamp - 12600
					cout = c+ " " + schedule[shift[b][c]]["c/out"]
					coutarray = time.strptime(cout, "%m/%d/%Y %I:%M:%S %p")
					coutstamp = int(time.mktime(coutarray))
					coutstampup = coutstamp + 12600
					coutstampdown = coutstamp - 12600
				if "AM" in schedule[shift[b][c]]["c/out"] and "PM" in schedule[shift[b][c]]["c/in"]:
					coutstamp += 86400
					coutstampup = coutstamp + 12600
					coutstampdown = coutstamp - 12600
				if cinstampdown < bstamp < cinstampup:
					if bstamp <= cinstamp + 59:
						#上班正常
						final.append([a, b, attendance[a][b][indextemp], shift[b][c], "c/in", "\n"])
						continue
					else:
						#上班遲到
						final.append([a, b, attendance[a][b][indextemp], shift[b][c],"c/in", "遲到" + str(abs(int((cinstamp - bstamp)/60))) + "分鐘\n"])
						continue
				if coutstampdown < bstamp < coutstampup:
					if bstamp >= coutstamp:
						#下班正常
						final.append([a, b, attendance[a][b][indextemp], shift[b][c], "c/out", "\n"])
						continue
					else:
						#下班早退
						final.append([a, b, attendance[a][b][indextemp], shift[b][c],"c/out", "早退" + str(abs(int((coutstamp - bstamp)/60))) + "分鐘\n"])
						continue

				#找不到資料
				final.append([a, b, attendance[a][b][indextemp], "n/a", "n/a", "班表中查無資料\n"])
#從shift拿出姓名
for a in shift.keys():
	#從shift[a]拿出日期
	for b in shift[a].keys():
		if shift[a][b] != "OFF" and shift[a][b] != "事假" and shift[a][b] != "病假" and shift[a][b] != "年假" and shift[a][b] != "公假" and shift[a][b] != "喪假" and shift[a][b] != "" and shift[a][b] != " " and shift[a][b] != "	":
			inyes = False
			outyes = False
			for c in final:
				if c[1] == a:
					dep = c[0]
					if "AM" in schedule[shift[a][b]]["c/out"] and "PM" in schedule[shift[a][b]]["c/in"]:
						btemp = b.split("/")
						btemp[1] = str(int(btemp[1]) + 1)
						btemp  = "/".join(btemp)
						if btemp in c[2]:
							print(month + "/" + dayend + "/" + year)
							if c[4] == "c/out":
								outyes = True
						#排除下班打卡時間已超過核對時間
						if btemp == month + "/" + str(int(dayend)+1) + "/" + year:
							outyes = True
					elif b in c[2]:
						if c[4] == "c/out":
								outyes = True
					if b in c[2]:
						if c[4] == "c/in":
							inyes = True 
			if inyes == False:
				final.append([dep, a, b, shift[a][b], "c/in", "上班沒打卡\n"])
			if outyes == False:
				final.append([dep, a, b, shift[a][b], "c/out", "下班沒打卡\n"])
		else:
			for d in attendance:
				if a in attendance[d]:
					final.append([d, a, b, shift[a][b], "n/a", "\n"])

with open("final.txt", "w") as f:
	for a in final:
		f.write(",".join(a))