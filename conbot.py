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
			split = str(mention.body).split(" ") # don't care about index 0
			
			for i in range(len(split)):
				split[i] = split[i].lower() # sanitize inputs

			if split[1] == "amendment":
				string = "Amendment "+split[2]+"\n"*2+">"+get_content(split[1]+split[2])
			elif split[1] == "bill of rights":
				string = "Bill of Rights "+"\n"*2+">"+get_content("billofrights")
			elif split[1] == "preamble":
				string = "Preamble "+"\n"*2+">"+get_content("preamble")
			elif split[1] == "article" and split[3] == "section":
				try:
					if split[5] == "clause": # if index 5 exists, this will work
						string = "Article "+split[2]+"section "+split[4]+"\n"*2+">"+get_content(split[1]+split[2]+split[3]+split[4]+split[5]+split[6])
				except IndexError: # if index 5 does not work
					string = "Article "+split[2]+"section "+"\n"*2+">"+get_content(split[1]+split[2]+split[3]+split[4])
			try:
				if string != "":
					mention.reply(string)
					reddit.inbox.mark_read([mention]) # mark mention as read
					print("Replied to: "+mention.parent_id)
			except praw.exceptions.APIException:
				print("Waiting 9 minutes")
				sleep(60*9)

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
		return ""

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