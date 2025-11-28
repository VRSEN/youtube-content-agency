"""Tool for generating thumbnail images using Google's Gemini 2.5 Flash Image model."""

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
)

from dotenv import load_dotenv

load_dotenv()


class GenerateImage(BaseTool):
    """Generate thumbnail images using Google's Gemini 3 Pro Image model.
    
    Images are saved to: /app/mnt/generated_thumbnails/
    
    IMPORTANT: reference images are automatically loaded for the generation, so you don't need to describe the charachter, the colors or the style, you can simply say "put the charachter from the reference images on the right side of the thumbnail". You don't need to describe the style and branding, simply explain the scene and what to show on the thumbnail, including visual elements, text and face expression. 

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
    file_name: str = Field(
        ...,
        description="The name for the generated thumbnail file (without extension, e.g., 'problem_angle_v1')",
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

        # Step 2: Automatically load all reference images from reference_thumbnails folder
        reference_images = load_all_reference_images()
        if reference_images:
            print(f"Using {len(reference_images)} reference image(s) for style matching")
        else:
            print("No reference images found - generating without style reference")

        # Step 3: Initialize the Google AI client
        client = genai.Client(api_key=api_key)

        # Step 4: Get video-specific images directory
        images_dir = get_images_dir(self.video_title)

        self.prompt = self.prompt.strip() + " Use attached previous thumbnails from our channel as a reference. Generate a new thumbnail as close as possible to the same style, using our branding, colors, style, similar elements, and the same person from references."

        def generate_single_variant():
            """Generate a single thumbnail"""
            try:
                print(f"Generating thumbnail...")

                # Prepare contents for the API call
                # If we have reference images, include them before the prompt
                if reference_images:
                    contents = reference_images + [self.prompt]
                else:
                    contents = [self.prompt]

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

