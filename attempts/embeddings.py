import numpy as np
import cv2

def spread_spectrum_watermarking(image, watermark, alpha=0.1):
    try:
        # Ensure watermark and image have the same dimensions
        if image.shape[:2] != watermark.shape[:2]:
            raise ValueError("Image and watermark must have the same dimensions.")

        # Convert watermark to binary mask (0 or 1)
        _, watermark_binary = cv2.threshold(watermark, 127, 255, cv2.THRESH_BINARY)

        # Generate pseudorandom noise
        rng = np.random.default_rng()
        noise = rng.integers(0, 2, size=image.shape[:2], dtype=np.uint8)

        # Expand dimensions of the noise to match the image
        noise = np.expand_dims(noise, axis=-1)

        # Reshape the watermark to match the dimensions of the noise
        watermark_binary = np.expand_dims(watermark_binary, axis=-1)

        # Combine watermark and noise
        combined = (1 - alpha) * image + alpha * noise * watermark_binary

        # Clip values to [0, 255]
        combined = np.clip(combined, 0, 255).astype(np.uint8)

        return combined
    except Exception as e:
        print(f"Error: {e}")
        return None

# Example usage:
if __name__ == "__main__":
    # Load an example image and watermark (replace with your own)
    image_path = "./assets/wm-nowm/train/no-watermark/african-american-slavery-man-woman-161890.jpeg"
    watermark_path = "./assets/watermark/watermark_image.jpg"
    image = cv2.imread(image_path)
    watermark = cv2.imread(watermark_path, cv2.IMREAD_GRAYSCALE)

    if image is not None and watermark is not None:
        # Resize watermark to match image dimensions
        watermark = cv2.resize(watermark, (image.shape[1], image.shape[0]))

        # Apply spread spectrum watermarking
        watermarked_image = spread_spectrum_watermarking(image, watermark, alpha=0.1)

        if watermarked_image is not None:
            # Save the watermarked image
            cv2.imwrite("watermarked_image.jpg", watermarked_image)
            print("Watermarked image saved as watermarked_image.jpg")
        else:
            print("Watermarking failed.")
    else:
        print("Error loading image or watermark.")
