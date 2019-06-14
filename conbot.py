import praw
import os
from praw.models import Comment
from time import sleep

def main(): # god help our poor bot if he goes over the 30 requests per minute limit
	reddit = praw.Reddit("NOPE",user_agent="STILL NOPE")
	while True: # add overflow system?
		messages = get_messages(reddit)
		string = ""
		print("Found "+str(len(messages))+" new mentions")
		for mention in messages:
			string = ""
			print("Mention: "+mention.body)
			split = str(mention.body).split(" ") # don't care about index 0
			
			for i in range(len(split)):
				split[i] = split[i].lower() # sanitize inputs

			if split[1] == "amendment":
				string = "Amendment "+split[2]+"\n"*2
				content = get_content(split[1]+split[2])
			elif split[1] == "bill" and split[2] == "of" and split[3] and "rights":
				string = "Bill of Rights "+"\n"*2
				content = get_content("billofrights")
			elif split[1] == "preamble":
				string = "Preamble "+"\n"*2
				content = get_content("preamble")
			elif split[1] == "article":
				try:
					if split[3] == "section":
						try:
							if split[5] == "clause": # article section clause
								string = "Article "+split[2]+" section "+split[4]+" clause "+split[6]+"\n"*2
								content = get_content(split[1]+split[2]+split[3]+split[4]+split[5]+split[6])
						except IndexError: # article section
							string = "Article "+split[2]+" section "+split[4]+"\n"*2
							content = get_content(split[1]+split[2]+split[3]+split[4])
				except IndexError: # article
					string = "Article "+split[2]+"\n"*2
					content = get_content(split[1]+split[2])
			else: # doesnt understand comment
				content = ""
				reddit.inbox.mark_read([mention]) # mark mention as read 
			try:
				if content != "":
					mention.reply(string+content)
					reddit.inbox.mark_read([mention]) # mark mention as read
					print("Replied to: "+str(mention))
			except praw.exceptions.APIException:
				print("Waiting 9 minutes") # using too much and have to wait
				sleep(60*9)

			sleep(3) # PRAW limits to 1 request every 2 seconds, waiting 3 to be safe
			
		print("Waiting 30 seconds")
		sleep(30) # check for new mentions every 30(ish) seconds, prevents ratelimit problems

# Takes a command (i.e "amendment 1") and returns
# the correct (hopefully) part of constitution
# returns empty string if file does not exist
def get_content(command):
	try:
		with open(os.path.join(os.getcwd(),"constitution/"+command+".txt"),"r") as file:
			content = file.readlines()
		return "".join(content)
	except FileNotFoundError:
		return "" # just incase something isnt understood

# get unread mentions
def get_messages(reddit):
	unread_messages = []
	for item in reddit.inbox.unread(limit=25): # 25 limit to avoid ratelimit
		if isinstance(item, Comment):
			print("Added unread message "+str(item))
			unread_messages.append(item)
	return unread_messages

if __name__ == "__main__":
	main()