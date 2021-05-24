from transformers import pipeline
from transformers import GPT2LMHeadModel,  GPT2Tokenizer, GPT2Config, GPT2LMHeadModel
import torch
import os
from transformers import AutoTokenizer, AutoModelWithLMHead

class TextGenerator():
	def __init__(self):
		if os.path.isdir("model/"):
			print("using local model")
			self.model = GPT2LMHeadModel.from_pretrained('model/')
			self.tokenizer = GPT2Tokenizer.from_pretrained('model/')
		else:
			print("using gyre/200wordrpgmodel model")
			self.model = AutoModelWithLMHead.from_pretrained("gyre/200wordrpgmodel")
			self.tokenizer = AutoTokenizer.from_pretrained("gyre/200wordrpgmodel")

		self.device = torch.device("cpu")
		self.model.to(self.device)
		self.model.eval()
    
	def create_textblock(self, text_on_screen=""):
		prompt="<|startoftext|>" + text_on_screen
		raw_prompt_length = len(text_on_screen)
		prompt_length = len(prompt.split(' '))
		generated = torch.tensor(self.tokenizer.encode(prompt)).unsqueeze(0)
		generated = generated.to(self.device)
		sample_outputs = self.model.generate(
										generated, 
										do_sample=True,   
										top_k=50, 
										max_length = list(generated.size())[1] + 10,
										top_p=0.95, 
										num_return_sequences=1
										)
		new_block = self.tokenizer.decode(sample_outputs[0], skip_special_tokens=True)
		return new_block[raw_prompt_length:]