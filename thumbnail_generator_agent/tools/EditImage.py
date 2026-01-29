"""Tool for editing existing thumbnail images using Google's Gemini 3 Pro Image model."""

import os
from typing import Literal

from google import genai
from pydantic import Field, field_validator

from agency_swarm import BaseTool

from thumbnail_generator_agent.tools.image_utils import (
    get_images_dir,
    MODEL_NAME,
    load_image_by_name,
    extract_image_from_response,
    load_text_style_reference,
)

from dotenv import load_dotenv

load_dotenv()


class EditImage(BaseTool):
    """Edit existing thumbnail images.
    
    Use this tool to make adjustments to previously generated thumbnails based on feedback.
    Images are saved to: ap/mnt/generated_thumbnails/{video_title}/.
    """

    video_title: str = Field(
        ...,
        description="Title of the video this thumbnail is for. Used to locate the existing thumbnail in video-specific folders.",
    )
    input_image_name: str = Field(
        ...,
        description="Name of the existing thumbnail file to edit (without extension, e.g., 'problem_angle_v1').",
    )
    edit_prompt: str = Field(
        ...,
        description=(
            "Text prompt describing the specific edits to make to the thumbnail. "
            "Be precise about what to change (e.g., 'Make the text larger', 'Change facial expression to more excited', "
            "'Add more yellow highlights', 'Adjust background to darker blue'). "
            "Only describe the changes you want to make, and nothing else."
        ),
    )
    output_image_name: str = Field(
        ...,
        description="The name for the edited thumbnail file (without extension, e.g., 'problem_angle_v2')",
    )
    aspect_ratio: Literal["16:9"] = Field(
        default="16:9",
        description="The aspect ratio of the thumbnail (YouTube standard is 16:9)",
    )

    @field_validator("input_image_name")
    @classmethod
    def _input_name_not_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("input_image_name must not be empty")
        return value

    @field_validator("edit_prompt")
    @classmethod
    def _prompt_not_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("edit_prompt must not be empty")
        return value

    @field_validator("output_image_name")
    @classmethod
    def _output_name_not_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("output_image_name must not be empty")
        return value

    async def run(self) -> str:
        """Edit a thumbnail image using the Gemini API."""

        # Step 1: Get API key from environment
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise RuntimeError("GOOGLE_API_KEY environment variable is required")

        print(f"Editing thumbnail with prompt: {self.edit_prompt}")

        # Step 2: Initialize the Google AI client
        client = genai.Client(api_key=api_key)

        # Step 3: Get video-specific images directory
        images_dir = get_images_dir(self.video_title)
        
        # Step 4: Load input image
        image, image_path, load_error = load_image_by_name(self.input_image_name, images_dir)
        if load_error:
            raise FileNotFoundError(load_error)
        print(f"Loaded image: {image_path}")

        # Step 4.5: Check if edit involves text and load text style reference if needed
        text_keywords = ["text", "font", "word", "title", "label", "typography", "letter", "heading"]
        involves_text = any(keyword in self.edit_prompt.lower() for keyword in text_keywords)

        text_style_ref = None
        if involves_text:
            # Use neutral tone for edits (we don't have background info)
            text_style_ref = load_text_style_reference(tone="neutral")

        # Step 5: Add brand color reminder to edit prompt
        enhanced_prompt = self.edit_prompt.strip() + " Maintain brand colors: accent color #fcd53a (bright yellow) and background color #0c102d (dark navy blue)."

        try:
            print(f"Generating edited thumbnail...")

            # Prepare contents for the API call
            contents = [enhanced_prompt]

            # Add text style reference if editing involves text
            if text_style_ref:
                contents.append(text_style_ref)
                contents.append("Use the above image as a reference for text styling.")

            contents.append(image)

            # Generate edited image using Gemini 3 Pro Image
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
            edited_image, text_output = extract_image_from_response(response)

            if edited_image is None:
                raise RuntimeError(f"No image was generated. Text output: {text_output}")

            # Save the edited image
            filename = f"{self.output_image_name}.png"
            filepath = os.path.join(images_dir, filename)
            edited_image.save(filepath, "PNG")
            
            print(f"Edited thumbnail saved to: {filepath}")
            return f"Edited thumbnail: {filepath}"
            
        except Exception as e:
            print(f"Error editing thumbnail: {str(e)}")
            raise


if __name__ == "__main__":
    import asyncio
    
    # Example usage with Google Gemini 3 Pro Image
    tool = EditImage(
        video_title="Anthropic Just Made Code‑Execution Agents Easy (But Dangerous)",
        input_image_name="anthropic_agents_gone_rogue_v1",
        edit_prompt="Make the text 'AGENTS GONE ROGUE' larger and more prominent. Add more yellow glow effect around the text.",
        output_image_name="anthropic_agents_gone_rogue_v2",
        aspect_ratio="16:9",
    )
    try:
        result = asyncio.run(tool.run())
        print(result)
    except Exception as exc:
        print(f"Thumbnail editing failed: {exc}")

