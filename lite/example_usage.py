"""
Example usage of Vector Expression Consistent Generator

This script demonstrates how to use the expression generator
for creating consistent character expressions in Stable Diffusion.
"""

from vector_expression_generator import (
    VectorExpressionGenerator,
    ExpressionVector,
    create_expression_config
)
import json


def example_1_basic_usage():
    """Example 1: Basic expression generation"""
    print("=" * 60)
    print("Example 1: Basic Expression Generation")
    print("=" * 60)
    
    generator = VectorExpressionGenerator(seed=42)
    
    # Get a predefined expression
    happy = generator.get_expression('happy')
    prompt = generator.expression_to_prompt(
        happy,
        "portrait of a person, professional photo"
    )
    print(f"\nPrompt for 'happy' expression:")
    print(f"  {prompt}")
    
    # List all available expressions
    print(f"\nAvailable expressions ({len(generator.list_available_expressions())}):")
    for expr in generator.list_available_expressions():
        print(f"  - {expr}")


def example_2_custom_expression():
    """Example 2: Creating custom expressions"""
    print("\n" + "=" * 60)
    print("Example 2: Custom Expression Creation")
    print("=" * 60)
    
    generator = VectorExpressionGenerator(seed=42)
    
    # Create a custom "contemplative" expression
    contemplative = ExpressionVector(
        happiness=0.0,
        sadness=0.3,
        anger=0.0,
        surprise=0.0,
        fear=0.0,
        disgust=0.0,
        neutral=0.7
    )
    
    generator.add_custom_expression('contemplative', contemplative)
    
    prompt = generator.expression_to_prompt(
        contemplative,
        "portrait, thoughtful pose"
    )
    print(f"\nCustom 'contemplative' expression:")
    print(f"  {prompt}")


def example_3_expression_sequence():
    """Example 3: Generate expression animation sequence"""
    print("\n" + "=" * 60)
    print("Example 3: Expression Animation Sequence")
    print("=" * 60)
    
    generator = VectorExpressionGenerator(seed=42)
    
    # Generate sequence from neutral to happy
    sequence = generator.generate_expression_sequence(
        'neutral',
        'happy',
        num_frames=6
    )
    
    print("\nExpression sequence (neutral → happy):")
    for i, expr in enumerate(sequence):
        prompt = generator.expression_to_prompt(expr)
        print(f"  Frame {i+1}: {prompt}")
    
    # Save sequence to file
    generator.save_expression_sequence(sequence, '/tmp/expression_sequence.json')
    print("\n✓ Sequence saved to /tmp/expression_sequence.json")


def example_4_consistent_seeds():
    """Example 4: Generate consistent seeds for batch generation"""
    print("\n" + "=" * 60)
    print("Example 4: Consistent Seed Generation")
    print("=" * 60)
    
    generator = VectorExpressionGenerator(seed=42)
    
    base_seed = 12345
    seeds = generator.generate_consistent_seed_sequence(
        base_seed,
        num_images=8,
        variation=500
    )
    
    print(f"\nBase seed: {base_seed}")
    print(f"Generated {len(seeds)} consistent seeds:")
    for i, seed in enumerate(seeds):
        print(f"  Image {i+1}: seed={seed}")


def example_5_batch_config():
    """Example 5: Create batch generation configuration"""
    print("\n" + "=" * 60)
    print("Example 5: Batch Generation Configuration")
    print("=" * 60)
    
    # Create config for generating multiple images with happy expression
    config = create_expression_config(
        expression_name='happy',
        seed=42,
        num_images=4,
        output_file='/tmp/batch_config.json'
    )
    
    print("\nBatch configuration created:")
    print(json.dumps(config, indent=2))
    print("\n✓ Configuration saved to /tmp/batch_config.json")


def example_6_expression_interpolation():
    """Example 6: Interpolate between expressions"""
    print("\n" + "=" * 60)
    print("Example 6: Expression Interpolation")
    print("=" * 60)
    
    generator = VectorExpressionGenerator(seed=42)
    
    sad = generator.get_expression('sad')
    happy = generator.get_expression('happy')
    
    print("\nInterpolating between 'sad' and 'happy':")
    for t in [0.0, 0.25, 0.5, 0.75, 1.0]:
        interpolated = generator.interpolate_expressions(sad, happy, t)
        prompt = generator.expression_to_prompt(interpolated)
        print(f"  t={t:.2f}: {prompt}")


def example_7_prompt_generation():
    """Example 7: Generate prompts for different expressions"""
    print("\n" + "=" * 60)
    print("Example 7: Prompt Generation for All Base Expressions")
    print("=" * 60)
    
    generator = VectorExpressionGenerator(seed=42)
    base_prompt = "portrait photo, professional lighting"
    
    print(f"\nBase prompt: \"{base_prompt}\"\n")
    
    key_expressions = [
        'neutral', 'happy', 'sad', 'angry', 
        'surprised', 'smiling', 'laughing'
    ]
    
    for expr_name in key_expressions:
        expr = generator.get_expression(expr_name)
        if expr:
            prompt = generator.expression_to_prompt(expr, base_prompt)
            print(f"{expr_name:12} → {prompt}")


def main():
    """Run all examples"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  Vector Expression Consistent Generator - Examples  ".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "=" * 58 + "╝")
    print("\n")
    
    try:
        example_1_basic_usage()
        example_2_custom_expression()
        example_3_expression_sequence()
        example_4_consistent_seeds()
        example_5_batch_config()
        example_6_expression_interpolation()
        example_7_prompt_generation()
        
        print("\n" + "=" * 60)
        print("All examples completed successfully!")
        print("=" * 60 + "\n")
        
    except Exception as e:
        print(f"\nError running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
