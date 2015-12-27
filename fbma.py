from bs4 import BeautifulSoup
import pandas as pd
f = open("C:\\Users\\kevin\\Downloads\\facebook-vitamintK\\html\\messages.htm", 'r', encoding="UTF8")

if False:
	from collections import defaultdict
	words = defaultdict(int)


	for line in f:
		for word in line.split():
			words[word] += 1

	x = sorted(words.items(), key = lambda x: x[1], reverse = True)
	for i in x[:350]:
		print(i)
#f.read(1000)

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
	soups = [] #remove this on dec 25th
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
			#print(msg.encode("utf-8"))
			#time.sleep(1)
		#raise ValueError

		#soups.append(s)
		#return s
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
	#x = f.read(5) #eat the first <div> tag that encapsulates all the threads.  not really necessary to have it I think. ok nevermind it is.
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
						#true = True
					if popped.split()[0] == tag.split()[0][1:]:
						if popped == 'div class="thread"':
							try:
								print(chunk[:100])
							except:
								for i in chunk[:100]:
									print(ord(i))
							do_stuff(chunk)
							chunk = ""
						#else:
							#print(popped, tag)
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
		#print(tag)
		x = f.read(1)

	msgs = pd.DataFrame(df_pre_dict)
	if input("save to csv?  type n to not save. ") != 'n':
		msgs.to_csv("msgs.csv")
		print("saved to msgs.csv")
	else:
		print("not saved")

if __name__ == "__main__":
	if input("reanalyze messages.htm?  type n to not. ") != 'n':
		make_df()
	else:
		print("k")

msgs = pd.DataFrame.read_csv("msgs.csv", encoding = "ISO-8859-1", parse_dates = [4], keep_default_na = False)

#def make_words():
#