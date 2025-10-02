"""
Example integration with Stable Diffusion pipelines

This module demonstrates how to use the Vector Expression Generator
with various Stable Diffusion implementations.
"""

from vector_expression_generator import VectorExpressionGenerator
import json


def generate_prompts_for_batch(
    expression_names: list,
    base_prompt: str,
    base_seed: int,
    seed_variation: int = 500
):
    """
    Generate a set of prompts and seeds for batch generation.
    
    Args:
        expression_names: List of expression names to generate
        base_prompt: Base prompt for all images
        base_seed: Starting seed value
        seed_variation: Maximum seed variation for consistency
        
    Returns:
        List of dictionaries with prompt and seed for each image
    """
    generator = VectorExpressionGenerator(seed=base_seed)
    seeds = generator.generate_consistent_seed_sequence(
        base_seed,
        len(expression_names),
        variation=seed_variation
    )
    
    batch = []
    for expr_name, seed in zip(expression_names, seeds):
        expr = generator.get_expression(expr_name)
        if expr is None:
            raise ValueError(f"Expression '{expr_name}' not found")
        
        prompt = generator.expression_to_prompt(expr, base_prompt)
        batch.append({
            'expression': expr_name,
            'prompt': prompt,
            'seed': seed
        })
    
    return batch


def create_animation_config(
    start_expression: str,
    end_expression: str,
    num_frames: int,
    base_prompt: str,
    base_seed: int,
    output_file: str = 'animation_config.json'
):
    """
    Create configuration for expression animation sequence.
    
    Args:
        start_expression: Starting expression name
        end_expression: Ending expression name
        num_frames: Number of frames in animation
        base_prompt: Base prompt for all frames
        base_seed: Starting seed value
        output_file: Path to save configuration
        
    Returns:
        Configuration dictionary
    """
    generator = VectorExpressionGenerator(seed=base_seed)
    
    # Generate expression sequence
    sequence = generator.generate_expression_sequence(
        start_expression,
        end_expression,
        num_frames
    )
    
    # Generate consistent seeds
    seeds = generator.generate_consistent_seed_sequence(
        base_seed,
        num_frames,
        variation=100  # Small variation for smooth animation
    )
    
    # Create frame configurations
    frames = []
    for i, (expr, seed) in enumerate(zip(sequence, seeds)):
        prompt = generator.expression_to_prompt(expr, base_prompt)
        frames.append({
            'frame': i,
            'prompt': prompt,
            'seed': seed,
            'expression_vector': {
                'happiness': expr.happiness,
                'sadness': expr.sadness,
                'anger': expr.anger,
                'surprise': expr.surprise,
                'fear': expr.fear,
                'disgust': expr.disgust,
                'neutral': expr.neutral
            }
        })
    
    config = {
        'animation_type': 'expression_transition',
        'start_expression': start_expression,
        'end_expression': end_expression,
        'num_frames': num_frames,
        'base_prompt': base_prompt,
        'base_seed': base_seed,
        'frames': frames
    }
    
    with open(output_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    return config


def webui_batch_script_generator(
    batch_data: list,
    negative_prompt: str = "low quality, blurry, deformed",
    steps: int = 30,
    cfg_scale: float = 7.5,
    width: int = 512,
    height: int = 512
):
    """
    Generate a batch script for AUTOMATIC1111's Stable Diffusion Web UI.
    
    Args:
        batch_data: List of dicts with 'prompt' and 'seed'
        negative_prompt: Negative prompt for all images
        steps: Number of sampling steps
        cfg_scale: CFG scale value
        width: Image width
        height: Image height
        
    Returns:
        String containing batch script commands
    """
    script_lines = [
        "# Batch generation script for SD Web UI",
        "# Copy and paste these into the Web UI or use with API",
        ""
    ]
    
    for i, item in enumerate(batch_data):
        script_lines.append(f"# Image {i+1}: {item['expression']}")
        script_lines.append(f"Prompt: {item['prompt']}")
        script_lines.append(f"Negative: {negative_prompt}")
        script_lines.append(f"Seed: {item['seed']}")
        script_lines.append(f"Steps: {steps}, CFG: {cfg_scale}, Size: {width}x{height}")
        script_lines.append("")
    
    return "\n".join(script_lines)


def diffusers_pipeline_example():
    """
    Example showing how to use with the diffusers library.
    
    Note: This is a template. Uncomment and modify when using with actual pipeline.
    """
    example_code = '''
# Example using with diffusers pipeline:

from diffusers import StableDiffusionPipeline
from vector_expression_generator import VectorExpressionGenerator
import torch

# Initialize pipeline
pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float16
)
pipe = pipe.to("cuda")

# Initialize expression generator
generator = VectorExpressionGenerator(seed=42)

# Generate images with different expressions
base_prompt = "portrait of a young woman, professional lighting, detailed face"
expressions = ['neutral', 'happy', 'sad', 'surprised']
seeds = generator.generate_consistent_seed_sequence(12345, len(expressions))

for expr_name, seed in zip(expressions, seeds):
    expr = generator.get_expression(expr_name)
    prompt = generator.expression_to_prompt(expr, base_prompt)
    
    # Generate image
    image = pipe(
        prompt,
        negative_prompt="low quality, blurry",
        num_inference_steps=30,
        guidance_scale=7.5,
        generator=torch.Generator("cuda").manual_seed(seed)
    ).images[0]
    
    # Save image
    image.save(f"output_{expr_name}_{seed}.png")
    print(f"Generated: {expr_name}")
    '''
    
    return example_code


if __name__ == "__main__":
    print("=" * 70)
    print("Stable Diffusion Integration Examples")
    print("=" * 70 + "\n")
    
    # Example 1: Batch generation
    print("Example 1: Batch Prompt Generation")
    print("-" * 70)
    expressions = ['neutral', 'smiling', 'happy', 'laughing']
    batch = generate_prompts_for_batch(
        expressions,
        "portrait photo, professional lighting, high quality",
        base_seed=12345,
        seed_variation=300
    )
    
    print(f"Generated {len(batch)} prompts:\n")
    for item in batch:
        print(f"  {item['expression']:10} (seed={item['seed']})")
        print(f"    {item['prompt']}\n")
    
    # Example 2: Animation config
    print("\nExample 2: Animation Configuration")
    print("-" * 70)
    config = create_animation_config(
        'neutral',
        'very_happy',
        num_frames=8,
        base_prompt="anime character, detailed face, colorful",
        base_seed=9999,
        output_file='/tmp/animation.json'
    )
    print(f"✓ Animation config created: {config['num_frames']} frames")
    print(f"  {config['start_expression']} → {config['end_expression']}")
    print(f"  Config saved to: /tmp/animation.json")
    
    # Example 3: Web UI script
    print("\nExample 3: Web UI Batch Script")
    print("-" * 70)
    script = webui_batch_script_generator(batch[:2])  # First 2 items
    print(script)
    
    # Example 4: Diffusers template
    print("\nExample 4: Diffusers Pipeline Template")
    print("-" * 70)
    code = diffusers_pipeline_example()
    print("Template code available in diffusers_pipeline_example()")
    print("See the function documentation for usage.")
    
    print("\n" + "=" * 70)
    print("Integration examples complete!")
    print("=" * 70 + "\n")
