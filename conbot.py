import praw
import os
from time import sleep

def main():
	reddit = praw.Reddit("NOPE",user_agent="ALSO NOPE")
	while True:
		for mention in reddit.inbox.mentions():
			split = str(mention.body).split(" ") # don't care about index 0
			for i in range(len(split)):
				split[i] = split[i].lower()

			if split[1] == "amendment":
				mention.reply(get_content(split[1]+split[2]))
				print("Replied to: "+mention.parent_id)
			elif split[1] == "billofrights":
				mention.reply(get_content("billofrights"))
				print("Replied to: "+mention.parent_id)
			elif split[1] == "preamble":
				mention.reply(get_content("preamble"))
				print("Replied to: "+mention.parent_id)
			elif split[1] == "article" and split[3] == "section":
				try:
					if split[5] == "clause": # if index 5 exists, this will work
						mention.reply(get_content(split[1]+split[2]+split[3]+split[4]+split[5]+split[6]))
						print("Replied to: "+mention.parent_id)
				except IndexError: # if index 5 does not work
					mention.reply(get_content(split[1]+split[2]+split[3]+split[4]))
					print("Replied to: "+mention.parent_id)
			#reddit.inbox.mark_read(list(mention)) #  do this
		#leep(30) # check for new mentions every 30 seconds

# Takes a command (i.e "amendment 1") and returns
# the correct (hopefully) part of constitution
def get_content(command):
	# hey PSF, please add a flag to open() to enable relative file paths
	with open(os.path.join(os.getcwd(),"constitution/"+command+".txt"),"r") as file:
		content = file.readlines()
	return "".join(content)

if __name__ == "__main__":
	main()