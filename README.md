# Trenzo-EzoN
Stable Diffusion with Vector Expression Consistent Generator

## Overview

Trenzo-EzoN is a Stable Diffusion toolkit featuring a powerful **Vector Expression Consistent Generator** that enables you to create consistent facial expressions across multiple generated images using vector embeddings and expression control parameters.

## Features

- **Vector Expression Consistent Generator**: Generate consistent character expressions
- **16 Predefined Expressions**: Including neutral, happy, sad, angry, surprised, and more
- **Custom Expression Creation**: Define your own expressions with 7-dimensional vectors
- **Expression Interpolation**: Smooth transitions between expressions for animations
- **Consistent Seed Generation**: Maintain character consistency across generations
- **Batch Configuration**: Streamlined workflow for generating multiple variations

## Quick Start

### Installation

```bash
pip install -r requirements.txt
```

### Basic Usage

```python
from lite.vector_expression_generator import VectorExpressionGenerator

# Create generator
generator = VectorExpressionGenerator(seed=42)

# Generate a prompt with expression
expression = generator.get_expression('happy')
prompt = generator.expression_to_prompt(
    expression,
    "portrait of a young woman, professional lighting"
)
print(prompt)
# Output: "portrait of a young woman, professional lighting, very happy"

# Generate consistent seeds for batch generation
seeds = generator.generate_consistent_seed_sequence(42, num_images=5)
```

### Expression Animation

```python
# Generate a 10-frame expression transition
sequence = generator.generate_expression_sequence(
    start_expr='neutral',
    end_expr='happy',
    num_frames=10
)

# Use each frame for animation
for i, expr in enumerate(sequence):
    prompt = generator.expression_to_prompt(expr, "character portrait")
    # Generate image with your Stable Diffusion pipeline
```

## Documentation

See [lite/README.md](lite/README.md) for comprehensive documentation, API reference, and advanced usage examples.

## Running Examples

```bash
cd lite
python example_usage.py
```

This will demonstrate all features of the expression generator with 7 detailed examples.

## Available Expressions

- `neutral`, `happy`, `very_happy`, `sad`, `very_sad`
- `angry`, `very_angry`, `surprised`, `very_surprised`
- `fearful`, `disgusted`, `smiling`, `laughing`, `crying`
- `shocked`, `annoyed`

Plus the ability to create unlimited custom expressions!

## Use Cases

1. **Character Consistency**: Generate multiple images of the same character with different expressions
2. **Animation Sequences**: Create smooth expression transitions for video
3. **Emotion Studies**: Generate comprehensive emotion reference sheets
4. **Interactive Applications**: Dynamic expression generation based on user input
5. **Batch Generation**: Efficiently generate large sets of consistent character images

## License

MIT License - See [LICENSE](LICENSE) for details
