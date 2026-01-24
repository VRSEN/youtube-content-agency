"""Tool for generating thumbnail images using Google's Gemini image model."""

import os
from typing import Literal

from google import genai
from pydantic import Field, field_validator

from agency_swarm import BaseTool

from thumbnail_generator_agent.tools.image_utils import (
    get_images_dir,
    MODEL_NAME,
    extract_image_from_response,
    load_all_reference_images,
    load_reference_image_by_name,
    BACKGROUND_DIR,
    EMOTION_DIR,
)

from dotenv import load_dotenv

load_dotenv()


class GenerateImage(BaseTool):
    """Generate thumbnail images using Google's Gemini image model.

    Images are saved to: /app/mnt/generated_thumbnails/

    Provide background and emotion reference image names to attach those files to the request.
    Reference thumbnails can be optionally attached for style guidance.

    This tool is stateless and does not allow reusing previous prompts. Use EditImage tool to make changes to the previous thumbnail.
    """

    video_title: str = Field(
        ...,
        description="Title of the video this thumbnail is for. Used to organize files into video-specific folders.",
    )
    prompt: str = Field(
        ...,
        description=(
            "The text prompt describing the thumbnail image to generate. Be specific about the visual elements."
            "Start with 'Generate a YouTube thumbnail image based on the reference images' and describe the thumbnail in detail."
        ),
    )
    background_image_name: str = Field(
        ...,
        description=(
            "Background reference image file name from thumbnail backgrounds/ "
            "(with or without extension, e.g., 'Neutral.jpg' or 'Neutral')."
        ),
    )
    emotion_image_name: str = Field(
        ...,
        description=(
            "Emotion reference image file name from Emotion References/ "
            "(with or without extension, e.g., 'serious.jpg' or 'serious')."
        ),
    )
    file_name: str = Field(
        ...,
        description="The name for the generated thumbnail file (without extension, e.g., 'problem_angle_v1')",
    )
    use_reference_thumbnails: bool = Field(
        default=False,
        description=(
            "Attach reference_thumbnails images for optional style guidance. "
            "Disabled by default."
        ),
    )
    aspect_ratio: Literal["16:9"] = Field(
        default="16:9",
        description="The aspect ratio of the thumbnail (YouTube standard is 16:9)",
    )

    @field_validator("prompt")
    @classmethod
    def _prompt_not_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("prompt must not be empty")
        return value

    @field_validator("file_name")
    @classmethod
    def _filename_not_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("file_name must not be empty")
        return value

    async def run(self) -> list:
        """Generate thumbnail images using the Gemini API."""

        # Step 1: Get API key from environment
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise RuntimeError("GOOGLE_API_KEY environment variable is required")

        print(f"Generating thumbnail with prompt: {self.prompt}")

        # Step 2: Load background and emotion reference images
        background_image, background_path = load_reference_image_by_name(
            self.background_image_name,
            BACKGROUND_DIR,
        )
        emotion_image, emotion_path = load_reference_image_by_name(
            self.emotion_image_name,
            EMOTION_DIR,
        )
        print(f"Using background reference: {background_path}")
        print(f"Using emotion reference: {emotion_path}")

        # Step 3: Optionally load reference thumbnails for style
        reference_images = []
        if self.use_reference_thumbnails:
            reference_images = load_all_reference_images()
            if reference_images:
                print(f"Using {len(reference_images)} reference image(s) for style matching")
            else:
                print("No reference images found - generating without style reference")

        # Step 4: Get video-specific images directory
        images_dir = get_images_dir(self.video_title)

        if self.use_reference_thumbnails and reference_images:
            self.prompt = (
                self.prompt.strip()
                + " Use attached previous thumbnails from our channel as a reference. "
                + "Generate a new thumbnail as close as possible to the same style, "
                + "using our branding, colors, style, similar elements, and the same person from references."
            )

        # Step 5: Initialize the Google AI client
        client = genai.Client(api_key=api_key)

        def generate_single_variant():
            """Generate a single thumbnail"""
            try:
                print(f"Generating thumbnail...")

                # Prepare contents for the API call (images first, then prompt)
                contents = []
                if reference_images:
                    contents.extend(reference_images)
                contents.extend([background_image, emotion_image, self.prompt])

                # Generate image using Gemini 3 Pro Image
                response = client.models.generate_content(
                    model=MODEL_NAME,
                    contents=contents,
                    config=genai.types.GenerateContentConfig(
                        image_config=genai.types.ImageConfig(
                            aspect_ratio=self.aspect_ratio,
                        )
                    ),
                )

                # Extract the generated image
                image, text_output = extract_image_from_response(response)

                if image is None:
                    raise RuntimeError(f"No image was generated. Text output: {text_output}")

                # Save the image
                filename = f"{self.file_name}.png"
                filepath = os.path.join(images_dir, filename)
                image.save(filepath, "PNG")
                
                print(f"Thumbnail saved to: {filepath}")
                return filepath
                
            except Exception as e:
                print(f"Error generating thumbnail: {str(e)}")
                raise

        # Step 5: Generate the thumbnail
        filepath = generate_single_variant()
        
        if not filepath:
            raise RuntimeError("Thumbnail generation failed")

        # Step 6: Return file path
        return f"Generated thumbnail: {filepath}"

if __name__ == "__main__":
    import asyncio
    
    # Example usage with Google Gemini 3 Pro Image
    # Reference images are automatically loaded from reference_thumbnails/ folder
    tool = GenerateImage(
        video_title="How to Build AI Agents with Agency Swarm",
        prompt=(
            "Generate a YouTube thumbnail image with a shocked/excited person's face on the left side, "
            "looking at a glowing AI agent swarm visualization on the right. Bold text overlay says 'AGENTS EVERYWHERE'. "
            "Professional YouTuber thumbnail style, dramatic lighting, high contrast, 4K quality."
        ),
        file_name="test_thumbnail",
        aspect_ratio="16:9",
    )
    try:
        result = asyncio.run(tool.run())
        print(result)
    except Exception as exc:
        print(f"Thumbnail generation failed: {exc}")

