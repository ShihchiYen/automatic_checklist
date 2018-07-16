import time

#建立班別的字典變數
schedule = {}
#建立出勤資料的字典變數
attendance = {}
#建立班表的字典變數
shift = {}
#最後要匯出的資料
final = []

year = input("請輸入比對年份: ")
month = input("請輸入比對月份(1-12): ")
daystart = input("請輸入比對起始日: ")
dayend = input("請輸入比對結束日: ")
nextday = input("請輸入比對結束日的隔天(m/d/yyyy): ")
lendate = int(len(month)) + int(len(dayend)) + 6

#打開班別檔案
with open("schedule.txt", "r") as f:
	#將班別檔案整理成一個名叫schedule的字典，範例{班別:{in或out:時間}}}，放進schedule裡
	for d in f:
		#將班別內容全改為大寫，刪除最後的換行符號
		temporary = d.upper().strip("\n")
		#open()開啟的檔案都為字串型別，將型別轉為清單，\t為分隔符號
		temporary = temporary.split("\t")
		#在schedule字典中建立鍵為該班別，值為{c/in:時間}的字典
		schedule[temporary[0]] = {"c/in":temporary[1]}
		#在schedule字典中該班別下建立鍵為c/out，值為時間的字典
		schedule[temporary[0]]["c/out"] = temporary[2]
		#刪除用不到的變數
		del temporary

#打開出勤資料
with open("attendance.txt", "r") as f:
	#將出勤資料整理成一個名叫attendance的字典，範例{部門:{姓名:(日期, 打卡紀錄)}}，放進attendance裡
	for d in f:
		#將出勤資料內容全改為大寫，刪除最後的換行符號
		temporary = d.upper().strip("\n")
		#open()開啟的檔案都為字串型別，將型別轉為清單，\t為分隔符號
		temporary = temporary.split("\t")
		#利用字串切片將打卡紀錄的日期部分拉出來，刪除前後空白，插入成為出勤資料第三個元素
		temporary.insert(2,temporary[2][0:lendate].strip())
		#如果在attendance(出勤資料)沒有該部門的key
		if temporary[0] not in attendance:
			#建立{部門:{姓名:(日期)}}，日期是清單
			attendance[temporary[0]] = {temporary[1]:[temporary[2]]}
			#將打卡紀錄extend到日期旁邊
			attendance[temporary[0]][temporary[1]].extend([temporary[3]])
		#如果在attendance(出勤資料)該部門下，沒有該姓名的key
		elif temporary[1] not in attendance[temporary[0]]:
			#在attendance(出勤資料)該部門字典中，建立{姓名:(日期)}，日期是清單
			attendance[temporary[0]][temporary[1]] = [temporary[2]]
			#將打卡紀錄extend到日期旁邊
			attendance[temporary[0]][temporary[1]].extend([temporary[3]])
		#attendance(出勤資料)裡有該部門，且已有該姓名的key
		else:
			#將日期extend到值的地方，範例{部門:{姓名:(值)}}
			attendance[temporary[0]][temporary[1]].extend([temporary[2]])
			#將打卡紀錄extend到日期旁邊
			attendance[temporary[0]][temporary[1]].extend([temporary[3]])
		#刪除用不到的變數
		del temporary

#打開班表
with open("shift.txt", "r") as f:
	#將班表整理成一個名叫shift的字典，範例{名字:{日期:班別}}，放進shift裡
	for d in f:
		#將班表全改為大寫，刪除最後的換行符號
		temporary = d.upper().strip("\n")
		#open()開啟的檔案都為字串型別，將型別轉為清單，\t為分隔符號
		temporary = temporary.split("\t")
		#為了在班表裡，將每天的班別都加上日期，所需的數字變數，初始為核對起始日-1
		number = int(daystart) - 1
		#為班表中每個人建立一個暫時的字典
		dicttemp = {}
		#把核對初始到結束的班別拿出來
		for a in temporary[int(daystart):int(dayend)+1]:
			#每拿出一個就加1
			number += 1
			#將日期為key，班別為值，放進暫時字典(日期是透過字串組合的)
			dicttemp[month + "/" + str(number) + "/" + year] = a
		#用每個人的名字當作key，上一步日期與班別組成的字典當作值放入shift
		shift[temporary[0]] = dicttemp
		#刪除用不到的變數
		del number; del dicttemp; del temporary

#開始核對打卡記錄是否正常，從attendance拿出部門
for a in attendance:
	#用來存放正確的下班時間數值
	coutstamp = 0
	#從attendance[部門]拿出姓名
	for b in attendance[a]:
		#之後要用的索引值暫存，初始-1
		indextemp = -1
		#從attendance[部門][姓名]拿出日期，因為日期放在清單中，且都是存在奇數位，所以用切片方式取出，取到清單總長度
		for c in attendance[a][b][0:len(attendance[a][b]):2]:
			#如果目前拿出姓名存在shift(班表)裡
			if b in shift:
				#每次索引直加初始為-1，所以加2後第一次是1
				indextemp += 2
				#把attendance[部門][姓名]中的打卡記錄取出轉為日期時間格式，因為打卡記錄都在偶數位，所以透過索引值暫存來取得
				barray = time.strptime((attendance[a][b][indextemp]), "%m/%d/%Y %I:%M:%S %p")
				#將上一步轉出的日期時間格式，轉為時間數值
				bstamp = int(time.mktime(barray))
				#如果coutstamp已經有值(用來存放正確的下班時間數值)，這部分主要用來核對跨日的打卡記錄，所以會有yestodayshift這個暫存
				if coutstamp != 0:
					#如果打卡記錄在下班時間附近
					if coutstampdown < bstamp < coutstampup:
						#如果打卡記錄等於或超過下班時間
						if bstamp >= coutstamp:
							#下班打卡正常，把資料放進final清單中，範例(部門, 姓名, 打卡記錄, 班別, c/out)
							final.append([a, b, attendance[a][b][indextemp], yestodayshift, "c/out", "\n"])
							continue
						#如果打卡記錄還沒到下班時間
						else:
							#下班打卡太早，把資料放進final清單中，範例(部門, 姓名, 打卡記錄, 班別, c/out, 早退幾分鐘)
							final.append([a, b, attendance[a][b][indextemp], yestodayshift,"c/out", "早退" + str(abs(int((coutstamp - bstamp)/60))) + "分鐘\n"])
							continue
				#如果利用目前的姓名與時間查詢到該班別的字串長度大於或等於10(表示有時間，沒有休假)
				if len(schedule[shift[b][c]]["c/in"]) >= 10:
					#記錄目前搜索到的班別(因為某些班別跨日，但是也是算這個班別，所以要先暫存)
					yestodayshift = shift[b][c]
					#利用目前這次的日期與班別的正確上班時間組合成字串
					cin = c + " " + schedule[shift[b][c]]["c/in"]
					#將上一步字串轉為日期時間格式
					cinarray = time.strptime(cin, "%m/%d/%Y %I:%M:%S %p")
					#將上一步轉出的日期時間格式，轉為時間數值
					cinstamp = int(time.mktime(cinarray))
					#將正確上班時間值加3小時半(為了檢查需要)
					cinstampup = cinstamp + 12600
					#將正確上班時間值減3小時半(為了檢查需要)
					cinstampdown = cinstamp - 12600
					#利用目前這次的日期與班別的正確下班時間組合成字串
					cout = c + " " + schedule[shift[b][c]]["c/out"]
					#將上一步字串轉為日期時間格式
					coutarray = time.strptime(cout, "%m/%d/%Y %I:%M:%S %p")
					#將上一步轉出的日期時間格式，轉為時間數值
					coutstamp = int(time.mktime(coutarray))
					#將正確下班時間值加3小時半(為了檢查需要)
					coutstampup = coutstamp + 12600
					#將正確下班時間值減3小時半(為了檢查需要)
					coutstampdown = coutstamp - 12600
				#如果這次的班別上班時間為PM下班時間為AM，表示下班時間為跨日
				if "AM" in schedule[shift[b][c]]["c/out"] and "PM" in schedule[shift[b][c]]["c/in"]:
					#因為是跨日，所以將下班時間值加一天
					coutstamp += 86400
					#將跨日的下班時間值加3小時半(為了檢查需要)
					coutstampup = coutstamp + 12600
					#將跨日的下班時間值減3小時半(為了檢查需要)
					coutstampdown = coutstamp - 12600
				#如果打卡時間介於正確上班時間正負3.5小時間
				if cinstampdown < bstamp < cinstampup:
					#如果打卡記錄早於或等於正確上班時間
					if bstamp <= cinstamp + 59:
						#上班打卡正常，把資料放進final清單中，範例(部門, 姓名, 打卡記錄, 班別, c/in)
						final.append([a, b, attendance[a][b][indextemp], shift[b][c], "c/in", "\n"])
						#離開避免重複判斷
						continue
					else:
						#上班遲到，把資料放進final清單中，範例(部門, 姓名, 打卡記錄, 班別, c/in, 遲到幾分鐘)
						final.append([a, b, attendance[a][b][indextemp], shift[b][c],"c/in", "遲到" + str(abs(int((cinstamp - bstamp)/60))) + "分鐘\n"])
						#離開避免重複判斷
						continue
				#如果打卡時間介於正確下班時間正負3.5小時間
				if coutstampdown < bstamp < coutstampup:
					#如果打卡時間晚於或等於正確下班時間
					if bstamp >= coutstamp:
						#下班打卡正常，把資料放進final清單中，範例(部門, 姓名, 打卡記錄, 班別, c/out)
						final.append([a, b, attendance[a][b][indextemp], shift[b][c], "c/out", "\n"])
						#離開避免重複判斷
						continue
					else:
						#下班打卡太早，把資料放進final清單中，範例(部門, 姓名, 打卡記錄, 班別, c/out, 早退幾分鐘)
						final.append([a, b, attendance[a][b][indextemp], shift[b][c],"c/out", "早退" + str(abs(int((coutstamp - bstamp)/60))) + "分鐘\n"])
						continue
				#如果上面的條件都沒有達到，且打卡時間是核對範圍的第一天
				if ("/"+daystart+"/"+year) in c[-7:]:
					#把資料放進final清單中，範例(部門, 姓名, 打卡記錄, n/a, n/a, 可能是上一期核對範圍最後一天跨日班的下班時間)
					final.append([a, b, attendance[a][b][indextemp], "n/a", "n/a", "可能是上一期核對範圍最後一天跨日班的下班時間\n"])
					continue
				#如果上面的條件都沒有達到，且打卡時間是AM
				if "AM" in attendance[a][b][indextemp]:
					#把資料放進final清單中，範例(部門, 姓名, 打卡記錄, n/a, n/a, 可能漏打上班卡，所以此下班記錄無法自動核對)
					final.append([a, b, attendance[a][b][indextemp], "n/a", "n/a", "可能漏打上班卡，所以此下班記錄無法自動核對\n"])
					continue
				#有些打卡記錄與班表對不上，把資料放進final清單中，範例(部門, 姓名, 打卡記錄, n/a, n/a, 打卡記錄與班表對不上)
				final.append([a, b, attendance[a][b][indextemp], "n/a", "n/a", "打卡記錄與班表對不上\n"])
#檢查是否沒打卡或是放假，從shift拿出姓名
for a in shift.keys():
	#從shift[姓名]拿出日期
	for b in shift[a].keys():
		#如果目前日期的班表不是放假
		if shift[a][b] != "OFF" and shift[a][b] != "事假" and shift[a][b] != "病假" and shift[a][b] != "年假" and shift[a][b] != "公假" and shift[a][b] != "喪假" and shift[a][b] != "" and shift[a][b] != " " and shift[a][b] != "	":
			#用來判斷是否打上班卡的變數
			inyes = False
			#用來判斷是否打下班卡的變數
			outyes = False
			#從final將資料取出
			for c in final:
				#如果final取出的資料名字與目前班表姓名相同
				if c[1] == a:
					#暫時存放部門名稱的變數
					dep = c[0]
					#如果這次的班別上班時間為PM下班時間為AM，表示下班時間為跨日
					if "AM" in schedule[shift[a][b]]["c/out"] and "PM" in schedule[shift[a][b]]["c/in"]:
						#將shift[姓名]拿出的日期字串改為清單
						btemp = b.split("/")
						#如果月份是大月
						if btemp[0] == "1" or btemp[0] == "3" or btemp[0] == "5" or btemp[0] == "7" or btemp[0] == "8" or btemp[0] == "10":
							#如果日期是31天
							if btemp[1] == "31":
								#將月份加1
								btemp[0] = str(int(btemp[0]) + 1)
								#將日期改為1
								btemp[1] = "1"
						#如果月份是小月
						if btemp[0] == "4" or btemp[0] == "6" or btemp[0] == "9" or btemp[0] == "11":
							#如果日期是30號
							if btemp[1] == "30":
								#將月份加1
								btemp[0] = str(int(btemp[0]) + 1)
								#將日期改為1
								btemp[1] = "1"
						#如果月份是2月
						if btemp[0] == "2":
							#如果日期是28號
							if btemp[1] == "28":
								#將月份加1
								btemp[0] = str(int(btemp[0]) + 1)
								#將日期改為1
								btemp[1] = "1"
						#如果月份是12月
						if btemp[0] == "12":
							#如果日期是31號
							if btemp[1] == "31":
								#將年份加1
								btemp[2] = str(int(year) + 1)
								#將月份改為1月
								btemp[0] = "1"
								#將日期改為1
								btemp[1] = "1"
						else:
							#將日期轉為int加1再轉回字串
							btemp[1] = str(int(btemp[1]) + 1)
						#將日期清單轉為字串用"/"分隔
						btemp  = "/".join(btemp)
						#如果該日期字串存在打卡記錄中
						if btemp in c[2]:
							#如果是"c/out"
							if c[4] == "c/out":
								#將判斷是否打下班卡變數改為True
								outyes = True
						#如果下班打卡日期會落在下一次核對的日期
						if btemp == nextday:
							#將判斷是否打下班卡變數改為True，這樣才不會顯示沒打卡
							outyes = True
					#如果班表需要上班的日期有在打卡記錄中
					elif b in c[2]:
						#如果打卡記錄是"c/out"
						if c[4] == "c/out":
							#將判斷是否打下班卡變數改為True
							outyes = True
					#如果班表需要上班的日期有在打卡記錄中
					if b in c[2]:
						#如果打卡記錄是"c/in"
						if c[4] == "c/in":
							#將判斷是否打上班卡變數改為True
							inyes = True 
			#如果是否打上班卡變數為False
			if inyes == False:
				#把資料放進final清單中，範例(部門, 姓名, 班表日期, 班別, c/in, 上班沒打卡)
				final.append([dep, a, b, shift[a][b], "c/in", "上班沒打卡\n"])
			#如果是否打下班卡變數為False
			if outyes == False:
				#把資料放進final清單中，範例(部門, 姓名, 班表日期, 班別, c/out, 下班沒打卡)
				final.append([dep, a, b, shift[a][b], "c/out", "下班沒打卡\n"])
		#如果班表沒有班別，表示為休假
		else:
			#將attendance的keys部門，一個個丟出來(這是為了取部門名稱)
			for d in attendance.keys():
				#如果attendance[部門]裡有這個名字(這是為了取部門名稱)
				if a in attendance[d]:
					#把資料放進final清單中，範例(部門, 姓名, 班表日期, 班別)
					final.append([d, a, b, shift[a][b], "\n"])
#建立final.txt可以寫入
with open("final.txt", "w") as f:
	#將final內容一行一行丟出來
	for a in final:
		#將final內容一行一行轉為字串，寫入final.txt
		f.write(",".join(a))