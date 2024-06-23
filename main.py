from rembg import remove
from PIL import Image

def main():
    input_path = input("Image Path: ")
    output_path = input("Output Path: ")
    open_image = input("Open image after processing? (Y/n): ")

    try:
        input_image = Image.open(input_path)
    except FileNotFoundError:
        print(f"Error: File not found at '{input_path}'. Please check the path.")
        return
    except Exception as e:
        print(f"Error opening image: {e}")
        return

    try:
        output_image = remove(input_image)
        output_image.save(output_path)
        print("Background Removed Successfully!")

        if open_image.lower() == "y":
            output_image.show()
    except Exception as e:
        print(f"Error processing image: {e}")

if __name__ == "__main__":
    main()
