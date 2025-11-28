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
    process_variant_result,
    run_parallel_variants,
    create_result_summary,
    compress_image_for_base64,
    load_all_reference_images,
)

from dotenv import load_dotenv

load_dotenv()


class GenerateImage(BaseTool):
    """Generate thumbnail images using Google's Gemini 3 Pro Image model.
    
    Images are saved to: mnt/generated_thumbnails/
    
    IMPORTANT: Use brand colors - Accent: #fcd53a (yellow), Background: #0c102d (dark blue)
    """

    video_title: str = Field(
        ...,
        description="Title of the video this thumbnail is for. Used to organize files into video-specific folders.",
    )
    prompt: str = Field(
        ...,
        description=(
            "The text prompt describing the thumbnail image to generate. Be specific about the visual elements, "
            "facial expressions, colors, text placement, and overall composition. "
            "MUST include brand colors: accent color #fcd53a (bright yellow) and background color #0c102d (dark navy blue). "
            "Start with 'Generate a YouTube thumbnail image' and describe the thumbnail in detail."
        ),
    )
    file_name: str = Field(
        ...,
        description="The name for the generated thumbnail file (without extension, e.g., 'problem_angle_v1')",
    )
    num_variants: int = Field(
        default=1,
        description="Number of thumbnail variants to generate (1-4, default is 1)",
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

    @field_validator("num_variants")
    @classmethod
    def _validate_num_variants(cls, value: int) -> int:
        if value < 1 or value > 4:
            raise ValueError("num_variants must be between 1 and 4")
        return value

    async def run(self) -> list:
        """Generate thumbnail images using the Gemini API."""

        # Step 1: Get API key from environment
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise RuntimeError("GOOGLE_API_KEY environment variable is required")

        print(f"Generating thumbnail with prompt: {self.prompt}")
        print(f"Generating {self.num_variants} variant(s)")

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

        def generate_single_variant(variant_num: int):
            """Generate a single thumbnail variant"""
            try:
                print(f"Generating variant {variant_num}/{self.num_variants}")

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
                    print(
                        f"Warning: No image was generated for variant {variant_num}. "
                        f"Text output: {text_output}"
                    )
                    return None

                # Process variant result
                return process_variant_result(
                    variant_num,
                    image,
                    self.file_name,
                    self.num_variants,
                    compress_image_for_base64,
                    images_dir,
                )
            except Exception as e:
                print(f"Error generating variant {variant_num}: {str(e)}")
                return None

        # Step 5: Run variants in parallel
        results = await run_parallel_variants(generate_single_variant, self.num_variants)

        if not results:
            raise RuntimeError("No variants were successfully generated")

        # Step 6: Create and print result summary
        result_text = create_result_summary(results, "Generated")
        print(result_text)

        # Step 7: Return only file paths (remove base64 data)
        return result_text

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

