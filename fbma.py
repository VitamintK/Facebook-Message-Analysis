from bs4 import BeautifulSoup

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
def do_stuff(chunk):
	s = BeautifulSoup(chunk)
	return s
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
x = f.read(5) #eat the first <div> tag that encapsulates all the threads.  not really necessary to have it I think.
x = f.read(1) 
while(x):
	if(x == ">"):
		if(in_a_tag):
			in_a_tag = False
			if(tag[0] == "/"):
				popped = tags.pop()
				if popped.split()[0] == tag.split()[0][1:]:
					if popped == 'div class="thread"':
						do_stuff(chunk)
						break
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
	chunk+= x
	x = f.read(1)