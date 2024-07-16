from PIL import Image

# Function to convert text to binary
def text_to_binary(text):
    binary_message = ''.join(format(ord(char), '08b') for char in text)
    return binary_message

# Function to hide a message in an image
def hide_message_in_image(image_path, message, output_path):
    # Open the image
    img = Image.open("astronaut.png")

    # Convert the message to binary
    binary_message = text_to_binary(message)

    # Check if the message is too long to hide in the image
    if len(binary_message) > img.width * img.height:
        print("Message is too long to hide in the image.")
        return

    # Iterate through the pixels and hide the message in the least significant bits
    binary_message += '1111111111111110'  # Adding a sentinel value to mark the end of the message
    data_index = 0

    img_data = img.load()
    for x in range(img.width):
        for y in range(img.height):
            pixel = list(img_data[x, y])
            for color_channel in range(3):  # R, G, B channels
                if data_index < len(binary_message):
                    pixel[color_channel] = int(format(pixel[color_channel], '08b')[:-1] + binary_message[data_index], 2)
                    data_index += 1
            img_data[x, y] = tuple(pixel)

    # Save the modified image
    img.save(output_path)
    print("Message hidden successfully.")

# Function to extract a message from an image
def extract_message_from_image(image_path):
    # Open the stego image
    img = Image.open(image_path)

    binary_message = ""
    img_data = img.load()

    for x in range(img.width):
        for y in range(img.height):
            pixel = list(img_data[x, y])
            for color_channel in range(3):  # R, G, B channels
                binary_message += format(pixel[color_channel], '08b')[-1]

    # Find the index of the sentinel value to extract the message
    end_index = binary_message.find('1111111111111110')
    if end_index != -1:
        binary_message = binary_message[:end_index]

    # Convert the binary message back to text
    message = ""
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i+8]
        message += chr(int(byte, 2))

    return message

# Example usage
image_path = "original_image.png"
message = "This is a hidden message."
output_path = "stego_image.png"

# Hide the message in the image
hide_message_in_image(image_path, message, output_path)

# Extract the hidden message from the image
extracted_message = extract_message_from_image(output_path)
print("Extracted Message:", extracted_message)
