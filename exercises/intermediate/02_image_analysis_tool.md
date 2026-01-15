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
messages=[{
    "role": "user", 
    "content": [
        {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": b64_data}},
        {"type": "text", "text": "What is in this image?"}
    ]
}]
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

File size too large (>5MB).

## 🎉 Completion

Congratulations! You've completed the exercise.
