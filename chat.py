from transformers import AutoModelForCausalLM, AutoTokenizer, LlamaTokenizer, pipeline 
import torch

# Models that can be used
# 4bit/Redmond-Puffin-13B
# openaccess-ai-collective/minotaur-13b-fixed
# Weyaxi/Einstein-v4-7B
# jondurbin/bagel-20b-v04-llama
model_name = "Locutusque/OpenCerebrum-1.0-7b-SFT"
# Load the model
#model = AutoModelForCausalLM.from_pretrained(model_name, load)
# The above line is for GPUs, if you are getting bitsandbytes errors, use the below line instead
model = AutoModelForCausalLM.from_pretrained(model_name, load_in_4bit=True, device_map="auto")

tokenizer = AutoTokenizer.from_pretrained(model_name)

# Defining our pipeline. We are keeping max tokens as 512, this can be increased based on requirement
# However, we are keeping return_full_text as True
# Temperature is 0.1 because we don't want randomness. In Science, same question should lead to same answer
# Repetition penalty can be adjusted, but we are keeping it as 1.3 to allow repitition, but also penalize it a bit 
hg_pipeline = pipeline(
    model=model,
    tokenizer=tokenizer,
    return_full_text=True,
    task='text-generation',
    temperature=0.1,
    max_new_tokens=512,
    repetition_penalty=1.3,
    pad_token_id=tokenizer.eos_token_id
)

#####
## This method gets responses from the bot based on user_input
## user_input : It is an array of dictionary carrying context based on system/user/assistant parameters
## Returns a string containing the response from the model
#####
def get_bot_response(user_input):
	# outputs = model.generate(input_ids, max_new_tokens=100)
	# Send the input to the pipeline
	outputs = hg_pipeline(user_input)
	result = ''
	decoded_output = ''
	# Iterate through the outputs to get the content.
	# Usually, it contains only one element
	for output in outputs:
		# decoded_output += tokenizer.decode(output["generated_text"], skip_special_tokens=True)
		decoded_output = decoded_output + output["generated_text"][-1]["content"]
	# print(decoded_output)
	# Extracting only bot response, instead of the entire content. This line will extract
	# the last response from the bot which is the response to the current prompt
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
