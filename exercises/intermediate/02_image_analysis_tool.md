# Exercise 2: Image Analysis Tool

## 🎯 Objective
Send images to Claude for analysis

## ⏱️ Time
30 minutes

## 📚 Prerequisites
- Module 2 Vision

## 🎓 Difficulty Level
⭐⭐ Intermediate

## 📝 Instructions

### Part 1: Base64 Encoding
Write a helper function to encode a local image file to base64.

### Part 2: Vision Request
Send the base64 image to Claude and ask for a description.

## 💻 Starter Code

```python
import base64

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# TODO: Call API with image content block
# TODO: derive the media_type from the file extension (image/jpeg, image/png, image/gif, image/webp)
```

## ✅ Expected Output

```
Description of the image.
```

## 🧪 Test Cases

Test with JPG and PNG.

## 🎁 Hints

<details>
<summary>Hint 1: Content Block</summary>

Use `type: image` in message content.
</details>


## ✨ Solution

<details>
<summary>Click to view solution</summary>

```python
import base64
import mimetypes
import sys

import anthropic

client = anthropic.Anthropic()

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def describe(image_path, question="What is in this image?"):
    media_type = mimetypes.guess_type(image_path)[0]
    if media_type not in ("image/jpeg", "image/png", "image/gif", "image/webp"):
        raise ValueError(f"Unsupported image type: {media_type}")
    message = client.messages.create(
        model="claude-sonnet-5-5",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": [
                {"type": "image", "source": {"type": "base64", "media_type": media_type, "data": encode_image(image_path)}},
                {"type": "text", "text": question},
            ],
        }],
    )
    return message.content[0].text

if __name__ == "__main__":
    print(describe(sys.argv[1]))
```
</details>

## 🚀 Extensions

Ask specific questions about the image.

## 📖 Learning Outcomes

- ✅ Multimodal capabilities
- ✅ Image handling

## 🔗 Related Lessons
- [Vision](../../modules/module2_core_api/06_vision_images.md)

## ❓ Common Issues

File size too large: the API rejects images over 5 MB (and very large images are downscaled), so resize before sending. Make sure `media_type` matches the real file format.

## 🎉 Completion

Congratulations! You've completed the exercise.
