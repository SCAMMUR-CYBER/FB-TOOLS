#AUTO SPAMSHARE TOOL
#MACK BY ARTHUR KEITH GRAYSON 
#ENJOY
#======IMPORT======#
import os
import requests 
import rich
import httpx
import threading
from queue import Queue

class ShareManager:
	def __init__(self, tokens, link, total_shares):
		self.tokens = tokens
		self.link = link
		self.total_shares = total_shares
		self.success_count = 0
		self.lock = threading.Lock()
		self.queue = Queue()

	def share_post(self, token):
		url = f"https://b-graph.facebook.com/v13.0/me/feed"
		payload = {
		'link': self.link,
		'published': '0',
		'privacy': '{"value":"SELF"}',
		'access_token': token
		}
		try:
			response = requests.post(url, data=payload).json()
			if 'id' in response:
				with self.lock:
					self.success_count += 1
					print(f'\033[1;32mSuccess Post Shared.💚')
			else:
				print(f'\033[1;31mFailed to share post: {response}❌')
		except requests.exeptions.RequestExeception as e:
			print(f'\033[1;31mNetwork error: {e}')

	def worker(self):
		while self.success_count < self.total_shares:
			try:
				token = self.queue.get(timeout=0.5)
				self.share_post(token)
				self.queue.task_done()
				if self.success_count>= self.total_shares:
					break
			except Exception:
				break

	def start_sharing(self):
		while self.success_count < self.total_shares:
			for token in self.tokens:
				self.queue.put(token)
				threads = []
				for _ in range(min(30, len(self.tokens))):
					thread = threading.Thread(target=self.worker)
					threads.append(thread)
					thread.start()
				for thread in threads:
					thread.join()
		print(f'\n\033[1;32mCompleted Success Post Shared. {self.success_count}/{self.total_shares}')
			
def load_tokens(file_path):
	if not os.path.exists(file_path):
		print(f'\033[1;31mToken file not found.')
		return []
	with open(file_path, 'r') as f:
		return [line.strip() for line in f if line.strip()]

def menu():
	token_file = "/sdcard/tokens.txt"
	tokens = load_tokens(token_file)
	if not tokens:
	    print(f'\033[1;31mNo valid tokens found. exiting')
	    return
	link = input("\033[1;37mEnter the post link to share: ").strip()
	try:
		total_shares = int(input("Enter the total number of shares: ").strip())
		if total_shares <= 0:
			print(f'\033[1;31mShare count must be greater than 0.')
			return
	except ValueError:
		print(f'\033[1;31mInvalid input. please enter a number')
		return
	manager = ShareManager(tokens, link, total_shares)
	manager.start_sharing()

if __name__ == "__main__":
    menu()