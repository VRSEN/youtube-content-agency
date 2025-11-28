import os
import io
import base64
from pathlib import Path
import asyncio
from PIL import Image

# Model name for Gemini Image Generation
MODEL_NAME = "gemini-3-pro-image-preview"

# Base directory for generated thumbnails (in project root)
BASE_DIR = Path(__file__).parent.parent.parent / "mnt" / "generated_thumbnails"
BASE_DIR.mkdir(parents=True, exist_ok=True)

# Reference thumbnails directory (in agent folder)
REFERENCE_DIR = Path(__file__).parent.parent / "reference_thumbnails"

OUTPUT_FORMAT = "png"


def get_images_dir(video_title: str = None) -> str:
    """
    Get the images directory, optionally organized by video title.
    
    Args:
        video_title: Optional video title to organize images (sanitized folder name)
        
    Returns:
        Path to generated_thumbnails directory or video-specific subdirectory
    """
    if video_title:
        # Sanitize video title for folder name
        safe_title = "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in video_title)
        safe_title = safe_title.replace(' ', '_')[:50]  # Limit length
        images_dir = BASE_DIR / safe_title
    else:
        images_dir = BASE_DIR
    
    images_dir.mkdir(parents=True, exist_ok=True)
    return str(images_dir)


def create_filename(file_name, variant_num, num_variants, output_format):
    """Create filename for image variant"""
    if num_variants == 1:
        image_name = file_name
    else:
        image_name = f"{file_name}_variant_{variant_num}"
    filename = f"{image_name}.{output_format}"
    return image_name, filename


def extract_image_from_response(response):
    """Extract image from Gemini API response"""
    image = None
    text_output = ""
    
    for part in response.candidates[0].content.parts:
        if part.text is not None:
            text_output += part.text
        elif part.inline_data is not None:
            image = Image.open(io.BytesIO(part.inline_data.data))
    
    return image, text_output


def process_variant_result(variant_num, image, file_name, num_variants, compress_func, images_dir):
    """Process a single variant result - save image and create result dict"""
    # Create filename for this variant
    image_name, filename = create_filename(file_name, variant_num, num_variants, OUTPUT_FORMAT)
    filepath = os.path.join(images_dir, filename)
    
    # Save the image
    image.save(filepath, OUTPUT_FORMAT)
    
    # Convert image to compressed base64 for preview
    compressed_b64 = compress_func(image)
    
    print(f"Variant {variant_num} saved to: {filepath}")
    
    return {
        "variant": variant_num,
        "file_path": filepath,
        "image_name": image_name,
        "base64": compressed_b64,
    }


async def run_parallel_variants(variant_func, num_variants):
    """Run multiple variants in parallel using asyncio"""
    loop = asyncio.get_event_loop()
    
    # Create tasks for all variants
    tasks = [
        loop.run_in_executor(None, variant_func, i + 1)
        for i in range(num_variants)
    ]
    
    # Wait for all tasks to complete
    completed_results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Filter out None results and exceptions
    results = []
    for result in completed_results:
        if result is not None and not isinstance(result, Exception):
            results.append(result)
        elif isinstance(result, Exception):
            print(f"Variant generation error: {result}")
    
    return results


def create_result_summary(results, operation_name):
    """Create result summary text with file paths"""    
    result_text = f"Generated {len(results)} variant(s) successfully!\n"
    for result in results:
        result_text += f"  - {result['image_name']} → {result['file_path']}\n"
    return result_text


def load_all_reference_images() -> list[Image.Image]:
    """
    Automatically load all reference images from the reference_thumbnails folder.
    
    Supports: .png, .jpg, .jpeg, .webp
    
    Returns:
        List of PIL Image objects (empty list if no images found)
    """
    if not REFERENCE_DIR.exists():
        print(f"Reference directory not found: {REFERENCE_DIR}")
        return []
    
    images = []
    supported_extensions = {'.png', '.jpg', '.jpeg', '.webp'}
    
    # Find all image files in the reference directory
    image_files = [
        f for f in REFERENCE_DIR.iterdir() 
        if f.is_file() and f.suffix.lower() in supported_extensions
    ]
    
    if not image_files:
        print(f"No reference images found in {REFERENCE_DIR}")
        return []
    
    print(f"Found {len(image_files)} reference image(s) in {REFERENCE_DIR}")
    
    for image_path in sorted(image_files):
        try:
            image = Image.open(image_path)
            print(f"  ✓ Loaded: {image_path.name}")
            images.append(image)
        except Exception as e:
            print(f"  ✗ Failed to load {image_path.name}: {str(e)}")
            continue
    
    return images


def compress_image_for_base64(image, max_size=(800, 800), quality=65):
    """Compress image for base64 output while keeping original uncompressed and aspect ratio"""
    # Create a copy to avoid modifying the original
    compressed_image = image.copy()
    
    # Calculate new size while maintaining aspect ratio
    original_width, original_height = compressed_image.size
    max_width, max_height = max_size
    
    # Calculate scaling factor to fit within max_size while maintaining aspect ratio
    width_ratio = max_width / original_width
    height_ratio = max_height / original_height
    scale_factor = min(width_ratio, height_ratio, 1.0)  # Don't upscale
    
    # Only resize if the image is larger than max_size
    if scale_factor < 1.0:
        new_width = int(original_width * scale_factor)
        new_height = int(original_height * scale_factor)
        compressed_image = compressed_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    # Convert to RGB if necessary (for JPEG compression)
    if compressed_image.mode in ('RGBA', 'LA', 'P'):
        # Create a white background
        background = Image.new('RGB', compressed_image.size, (255, 255, 255))
        if compressed_image.mode == 'P':
            compressed_image = compressed_image.convert('RGBA')
        background.paste(compressed_image, mask=compressed_image.split()[-1] if compressed_image.mode == 'RGBA' else None)
        compressed_image = background
    
    # Save as JPEG with compression
    buffer = io.BytesIO()
    compressed_image.save(buffer, format='JPEG', quality=quality, optimize=True)
    buffer.seek(0)
    compressed_base64 = base64.b64encode(buffer.getvalue()).decode()
    return compressed_base64

