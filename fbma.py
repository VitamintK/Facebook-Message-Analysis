from bs4 import BeautifulSoup
import pandas as pd
f = open("C:\\Users\\kevin\\Downloads\\facebook-vitamintK\\html\\messages.htm", 'r', encoding="UTF8")

"""shape of the html page:
<div class = "thread">
	person1, person2
-	<div class = "message">
-		<div class="message_header">
-			<span class="user">Kevin Wang</span>
-			<span class="meta">Thursday, October 15, 2015 at 1:10am PDT</span>
-		</div>
-	</div>
-	<p>actual message text</p>
.
.
.
</div>"""
#handrolling my own semi-html parser cause fuck
def make_df():
	msgs = pd.DataFrame(columns = ["time", "sender", "members", "text"])
	df_pre_dict = []
	kkk = None
	def do_stuff(chunk):
		if(chunk[1] == "/"):
			print("ALERT ALERT")
			chunk = chunk[7:]
		s = BeautifulSoup(chunk).find("div", class_ = "thread")
		members = [x.strip() for x in next(s.strings).split(",")]
		try:
			print(members)
		except:
			print('-------------')
		msg_dict = {"members": members}
		for msg in s.children:
			try: 
				if msg.name == "p":
					msg_dict["text"] = msg.text
				elif msg.name == "div":
					halal = msg.div.contents
					msg_dict["time"] = halal[1].text
					msg_dict["sender"] = halal[0].text
			except AttributeError:
				print("sucks 2 suk")
			if msg_dict.get("text") and msg_dict.get("sender"):
				df_pre_dict.append(msg_dict)
				msg_dict = {"members": members}
	x = f.read(1)
	in_a_tag = False
	tags = []
	tag = ""
	chunk = ""
	while(x):
		x = f.read(1)
		if(x == "<"):
			in_a_tag = True #we in here
		elif(x == ">"):
			if(tag == "/h1"):
				tag = ""
				in_a_tag = False
				break
			else:
				tag = ""
				in_a_tag = False
		else:
			if(in_a_tag):
				tag+=x

	print("we are now at the start of the threads")
	x = f.read(1) 
	while(x):
		chunk+= x
		if(x == ">"):
			if(in_a_tag):
				in_a_tag = False
				if(tag[0] == "/"):
					try:
						popped = tags.pop()
					except:
						break
					if popped.split()[0] == tag.split()[0][1:]:
						if popped == 'div class="thread"':
							try:
								print(chunk[:100])
							except:
								for i in chunk[:100]:
									print(ord(i))
							do_stuff(chunk)
							chunk = ""
						tag = ""
					else:
						raise ValueError("END TAG IS TOTALLY DIFFERENT THAN MOST RECENT START TAG {}, {}".format(popped, tag.split()[0]))
				else:
					tags.append(tag)
					tag = ""
			else:
				raise ValueError("WE FUCKED UP {}".format(tag))
		elif(in_a_tag):
			tag += x
		elif(x == "<"):
			assert (not in_a_tag), "rip"
			in_a_tag = True
		x = f.read(1)

	msgs = pd.DataFrame(df_pre_dict)
	msgs['time'] =  pd.to_datetime(msgs['time'])
	if(input("save to hdf?  type n to not save.") != 'n'):
		msgs.to_hdf("msgs.h5", 'table', append=False)
		print("saved to msgs.hd5")
	else:
		print("not saved")
	if input("save to csv?  type n to not save. ") != 'n':
		msgs.to_csv("msgs.csv")
		print("saved to msgs.csv")
	else:
		print("not saved")
	return msgs

def make_wordlist(messages: pd.DataFrame):
	wordlist = []
	for row in msgs.itertuples(): #itertuples is faster so use it instead
		for word in row[3].split():
			wordlist.append({"word": word, "sender": row[2], "members": row[1], "time": row[4]})
	return pd.DataFrame(wordlist)

if __name__ == "__main__":
	#import timeit
	#y = timeit.timeit('h = test2()', 'from __main__ import test2', number=1) #727 seconds,	460 seconds METHOD: msgs['time'] =  pd.to_datetime(msgs['time']) #(batch)
	#x = timeit.timeit('g = test1()', 'from __main__ import test1', number=1) #1119 seconds,598 seconds METHOD: msg_dict["time"] = pd.to_datetime(halal[1].text) #(as they come)
	#z = timeit.timeit('j = make_df()', 'from __main__ import make_df', number=1) #around 550 seconds...
	if input("reanalyze messages.htm?  type n to not. ") != 'n':
		make_df()
	else:
		print("k")

msgs = pd.read_hdf("msgs.h5", "table", encoding = "ISO-8859-1", parse_dates = [4], keep_default_na = False)
#msgs = pd.read_csv("msgs.csv", encoding = "ISO-8859-1", parse_dates = [4], keep_default_na = False)
