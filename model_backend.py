import torch
from transformers import AutoProcessor

try:
    from transformers import AutoModelForImageTextToText as AutoModelForVision2Seq
except ImportError:
    from transformers import AutoModelForVision2Seq


class ModelBackend:

    def __init__(self):

        model_id = "google/gemma-3-4b-it"

        print("Loading model on CUDA...")

        self.processor = AutoProcessor.from_pretrained(model_id)
        self.model = AutoModelForVision2Seq.from_pretrained(
            model_id,
            torch_dtype=torch.bfloat16,
            device_map="auto"
        )

        print("Model loaded successfully.")

    def generate(self, prompt, images=None):

        messages = [
            {
                "role": "system",
                "content": "You are a hospital triage AI. Follow formatting strictly."
            }
        ]

        # Handle single image only (Gemma is strict)
        if images and len(images) > 0:
            image = images[0].convert("RGB")
            user_content = "<image>\n" + prompt
        else:
            image = None
            user_content = prompt

        messages.append(
            {
                "role": "user",
                "content": user_content
            }
        )

        text = self.processor.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )

        if image is not None:
            inputs = self.processor(
                text=text,
                images=image,
                return_tensors="pt"
            )
        else:
            inputs = self.processor(
                text=text,
                return_tensors="pt"
            )

        inputs = {k: v.to(self.model.device) for k, v in inputs.items()}

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=512,
                temperature=0.2,
                do_sample=False
            )

        decoded = self.processor.decode(outputs[0], skip_special_tokens=True)

        return decoded
