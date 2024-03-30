from transformers import AutoModelForCausalLM, AutoTokenizer, LlamaTokenizer, pipeline 
import torch

# Models that can be used
# 4bit/Redmond-Puffin-13B
# openaccess-ai-collective/minotaur-13b-fixed
# Weyaxi/Einstein-v4-7B
# jondurbin/bagel-20b-v04-llama
model_name = "Locutusque/OpenCerebrum-1.0-7b-SFT"  # Choose the desired model (small, medium, or large)
print('check 2')
# Load the model
#model = AutoModelForCausalLM.from_pretrained(model_name, load)

model = AutoModelForCausalLM.from_pretrained(model_name, load_in_4bit=True, device_map="auto")

tokenizer = AutoTokenizer.from_pretrained(model_name)
print('check 3')
hg_pipeline = pipeline(
    model=model,
    tokenizer=tokenizer,
    return_full_text=True,
    task='text-generation',
    temperature=0.1,
    max_new_tokens=512,
    repetition_penalty=1.1,
    pad_token_id=tokenizer.eos_token_id
)

# Chatting loop with greedy search
chat_history_ids = None
bot_input_ids = []
def get_bot_response(user_input):
	global model, tokenizer, bot_input_ids, chat_history_ids
	input_ids = tokenizer.apply_chat_template(user_input, return_tensors="pt").to("cuda")
	# outputs = model.generate(input_ids, max_new_tokens=100)
	outputs = hg_pipeline(user_input)
	result = ''
	decoded_output = ''
	for output in outputs:
		# decoded_output += tokenizer.decode(output["generated_text"], skip_special_tokens=True)
		decoded_output = decoded_output + output["generated_text"][-1]["content"]
	# print(decoded_output)
	result = decoded_output.split('<<USER>>')[-1].split('INST]')[-1][1:]
	return result

# print("Loading")
# context = [{"role": "system", "content": "You are a tutor for a student who explains everything with the simplest explanation and always have an answer"}]

# for i in range(5):
# 	user_input = input("user > ")
# 	context.append({"role": "user", "content": user_input})
# 	resp = get_bot_response(context)
# 	context.append({"role": "assistant", "content": resp})
# 	print(f"bot > {resp}")



# messages = [
#     {"role": "user", "content": "What is Pi?"},
#     # {"role": "assistant", "content": "What is the formula for area of square?"},
#     # {"role": "user", "content": "Do you have mayonnaise recipes?"}
# ]
