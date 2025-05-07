import os
import re
import folder_paths
import json
import hashlib
import openai


class ChatGptHelper:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                 "enable_chatgpt": ("BOOLEAN", {
                    "default": True, "label_on": "Yes", "label_off": "No"
                }),
                "chatgpt_api_key": ("STRING", {"multiline": True, "default": ""}),
                "input_prompt_text": ("STRING", {"multiline": True, "default": ""}),
                "chatgpt_instruction_text": ("STRING", {"multiline": True, "default": ""}),
            }
        }

    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("updated_prompt",)
    FUNCTION = "update_prompt"
    OUTPUT_NODE = True
    CATEGORY = "utils"

    # Class variable to store the last inputs and outputs
    _cache = {}
    
    def update_prompt(self,enable_chatgpt,chatgpt_api_key, input_prompt_text, chatgpt_instruction_text,):
        # Handle case where inputs are not lists
        print("chatgpt_instruction_text---sss...")
        print(input_prompt_text)
        print(chatgpt_instruction_text)
        updated_prompt_text=input_prompt_text
        
        # Generate a cache key for this specific run
        input_data = {
            "input_prompt_text": input_prompt_text,
            "chatgpt_instruction_text": chatgpt_instruction_text
        }
        
        # Create a hash of the inputs to use as cache key
        cache_key = self._get_cache_key(input_data)
        
        # Check if we've already processed these exact inputs
        if cache_key in ChatGptHelper._cache:
            print("Using cached result for SaveTextFlorence node")
            return ChatGptHelper._cache[cache_key]
        if enable_chatgpt:    
            updated_prompt_text =self._update_prompt_chatgpt(self,chatgpt_api_key, input_prompt_text,chatgpt_instruction_text)
        #SaveTextFlorence._cache[cache_key] = result
        return updated_prompt_text

    def _get_cache_key(self, input_data):
        """Generate a unique hash for the input data to use as a cache key"""
        # Convert input data to a JSON string and hash it
        input_json = json.dumps(input_data, sort_keys=True)
        return hashlib.md5(input_json.encode()).hexdigest()

    def _update_prompt_chatgpt(self,chatgpt_api_key, prompt,chatgpt_instruction_text):
            # Set your OpenAI API key
        client = openai.OpenAI(api_key=chatgpt_api_key)  # or use `os.getenv("OPENAI_API_KEY")`
            
        original_prompt = prompt
            
        instruction = (
                "You are an AI prompt editor. Given an image prompt, update it by:\n"
                
                "1. Enhancing the prompt to generate a high-quality, natural, realistic image.\n"
                "2. Add visual clarity, lighting, and environment details where needed.\n"
                "3. Make the language flow naturally and sound like a professional image generation prompt.\n"
                "4. Do not add technical instructions or explain your changes.\n"
                "5. Return ONLY the updated prompt, no extra commentary or headers."
                + chatgpt_instruction_text 
            )
            
        response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an image prompt editor. Only return the final prompt with no extra text."},
                    {"role": "user", "content": instruction + "\n\n" + original_prompt}
                ],
                temperature=0.7
            )
            
        new_prompt = response.choices[0].message.content.strip()
        return new_prompt
        


    @classmethod
    def IS_CHANGED(cls, text, file, enable_replacement, image_style, gender_age_replacement, lora_trigger, negative_prompt_text):
        """
        Tells ComfyUI whether this node should be re-executed.
        Returns None to indicate the node should be considered cached.
        """
        return None

NODE_CLASS_MAPPINGS = {
    "ChatGptHelper": ChatGptHelper
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ChatGptHelper": "ChatGpt Helper to enhance prompt"
}
