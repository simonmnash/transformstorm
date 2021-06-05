from transformers import GPT2LMHeadModel,  GPT2Tokenizer, GPT2LMHeadModel
import torch, os
from transformers import AutoTokenizer, AutoModelForCausalLM


class TextGenerator():
	def __init__(self, model_path=None, model_name=None):
		if len(model_path) > 0 and os.path.isdir(model_path):
			print("using local model")
			self.model = GPT2LMHeadModel.from_pretrained(model_path)
			self.tokenizer = GPT2Tokenizer.from_pretrained(model_path)
		else:
			print(f"using {model_name}")
			self.model = AutoModelForCausalLM.from_pretrained(model_name)
			self.tokenizer = AutoTokenizer.from_pretrained(model_name)

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