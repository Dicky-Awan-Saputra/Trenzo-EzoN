# Vector Expression Consistent Generator

A powerful tool for generating consistent facial expressions across multiple Stable Diffusion images using vector embeddings and expression control parameters.

## Features

- **Predefined Expression Library**: 16 base expressions including neutral, happy, sad, angry, surprised, and more
- **Custom Expression Creation**: Define your own expressions using vector parameters
- **Expression Interpolation**: Smoothly transition between expressions for animation sequences
- **Consistent Seed Generation**: Generate related seeds for consistent character appearance
- **Prompt Generation**: Automatically convert expressions to Stable Diffusion prompts
- **Batch Configuration**: Create configuration files for batch generation workflows
- **Save/Load Functionality**: Persist expressions and sequences to JSON files

## Installation

No additional dependencies required beyond numpy:

```bash
pip install numpy
```

## Quick Start

```python
from vector_expression_generator import VectorExpressionGenerator

# Create generator
generator = VectorExpressionGenerator(seed=42)

# Get an expression and generate prompt
happy = generator.get_expression('happy')
prompt = generator.expression_to_prompt(
    happy,
    "portrait of a young woman, professional photo"
)
print(prompt)
# Output: "portrait of a young woman, professional photo, happy"
```

## Expression Vector Structure

Each expression is represented as a 7-dimensional vector:

- `happiness`: Happiness/joy level (0.0 to 1.0)
- `sadness`: Sadness level (0.0 to 1.0)
- `anger`: Anger level (0.0 to 1.0)
- `surprise`: Surprise level (0.0 to 1.0)
- `fear`: Fear level (0.0 to 1.0)
- `disgust`: Disgust level (0.0 to 1.0)
- `neutral`: Neutral expression level (0.0 to 1.0)

## Available Base Expressions

- `neutral` - Neutral, calm expression
- `happy` - Moderately happy
- `very_happy` - Very happy/joyful
- `sad` - Moderately sad
- `very_sad` - Very sad/depressed
- `angry` - Moderately angry
- `very_angry` - Very angry/furious
- `surprised` - Moderately surprised
- `very_surprised` - Very surprised/shocked
- `fearful` - Fearful/scared
- `disgusted` - Disgusted
- `smiling` - Gentle smile
- `laughing` - Laughing expression
- `crying` - Crying expression
- `shocked` - Shocked (surprise + fear)
- `annoyed` - Annoyed (anger + disgust)

## Usage Examples

### Example 1: Generate a Sequence

```python
generator = VectorExpressionGenerator(seed=42)

# Generate 10-frame sequence from neutral to happy
sequence = generator.generate_expression_sequence(
    'neutral',
    'happy',
    num_frames=10
)

# Generate prompts for each frame
for i, expr in enumerate(sequence):
    prompt = generator.expression_to_prompt(
        expr,
        "portrait, detailed face"
    )
    print(f"Frame {i}: {prompt}")
```

### Example 2: Create Custom Expression

```python
from vector_expression_generator import ExpressionVector

# Create a "contemplative" expression
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

# Use it
expr = generator.get_expression('contemplative')
prompt = generator.expression_to_prompt(expr, "portrait")
```

### Example 3: Generate Consistent Seeds

```python
# Generate seeds that will produce similar-looking characters
seeds = generator.generate_consistent_seed_sequence(
    base_seed=12345,
    num_images=5,
    variation=500  # Small variation for consistency
)

print(seeds)
# Output: [12345, 12567, 12123, 12678, 12234]
```

### Example 4: Batch Configuration

```python
from vector_expression_generator import create_expression_config

# Create config for batch generation
config = create_expression_config(
    expression_name='happy',
    seed=42,
    num_images=4,
    output_file='batch_config.json'
)
```

### Example 5: Save and Load Expressions

```python
# Save an expression
happy = generator.get_expression('happy')
generator.save_expression(happy, 'happy_expression.json')

# Load an expression
loaded = generator.load_expression('happy_expression.json')

# Save a sequence
sequence = generator.generate_expression_sequence('neutral', 'happy', 5)
generator.save_expression_sequence(sequence, 'animation.json')

# Load a sequence
loaded_sequence = generator.load_expression_sequence('animation.json')
```

## Integration with Stable Diffusion

### Basic Integration

```python
# 1. Generate expression prompt
generator = VectorExpressionGenerator(seed=42)
expression = generator.get_expression('happy')
prompt = generator.expression_to_prompt(
    expression,
    "portrait of a young woman, detailed face, studio lighting"
)

# 2. Get consistent seeds
seeds = generator.generate_consistent_seed_sequence(42, num_images=4)

# 3. Use in your SD pipeline
# for seed in seeds:
#     image = sd_pipeline(prompt, seed=seed, ...)
```

### Animation Sequence

```python
# Generate expression transition animation
sequence = generator.generate_expression_sequence(
    'neutral',
    'laughing',
    num_frames=30
)

base_prompt = "anime character, detailed face, vibrant colors"

# Generate each frame
for i, expr in enumerate(sequence):
    prompt = generator.expression_to_prompt(expr, base_prompt)
    seed = 12345 + i  # Sequential seeds
    # image = sd_pipeline(prompt, seed=seed, ...)
    # save_image(image, f"frame_{i:03d}.png")
```

## Configuration File Format

Example configuration file (`expression_config_example.json`):

```json
{
  "presets": {
    "portrait_session": {
      "base_prompt": "portrait photo, professional lighting",
      "negative_prompt": "low quality, blurry",
      "expressions": ["neutral", "smiling", "happy"],
      "seed": 12345,
      "steps": 30,
      "cfg_scale": 7.5
    }
  },
  "custom_expressions": {
    "thoughtful": {
      "happiness": 0.0,
      "sadness": 0.2,
      "neutral": 0.8
    }
  }
}
```

## Tips for Best Results

1. **Use Consistent Seeds**: Use the `generate_consistent_seed_sequence()` method to maintain character consistency
2. **Small Variations**: Keep seed variations small (100-500) for similar-looking characters
3. **Interpolation**: Use `interpolate_expressions()` for smooth transitions
4. **Combine with ControlNet**: For best results, combine with ControlNet for pose consistency
5. **Base Prompts**: Keep base prompts descriptive but consistent across generation

## Advanced Usage

### Multi-Expression Batch Generation

```python
generator = VectorExpressionGenerator(seed=42)
base_seed = 12345
base_prompt = "portrait, professional lighting, detailed"

expressions = ['neutral', 'happy', 'sad', 'angry', 'surprised']
seeds = generator.generate_consistent_seed_sequence(base_seed, len(expressions))

for expr_name, seed in zip(expressions, seeds):
    expr = generator.get_expression(expr_name)
    prompt = generator.expression_to_prompt(expr, base_prompt)
    print(f"{expr_name}: seed={seed}")
    print(f"  Prompt: {prompt}")
    # Generate with SD pipeline...
```

### Expression Blending

```python
# Blend multiple expressions
happy = generator.get_expression('happy')
surprised = generator.get_expression('surprised')

# 70% happy, 30% surprised
blend_factor = 0.3
blended = generator.interpolate_expressions(happy, surprised, blend_factor)

prompt = generator.expression_to_prompt(blended, "portrait")
print(prompt)  # "portrait, happy and surprised"
```

## API Reference

### VectorExpressionGenerator

#### Methods

- `__init__(seed: Optional[int])`: Initialize generator with optional seed
- `get_expression(name: str)`: Get expression by name
- `add_custom_expression(name: str, expression: ExpressionVector)`: Add custom expression
- `interpolate_expressions(expr1, expr2, t: float)`: Interpolate between two expressions
- `generate_expression_sequence(start_expr, end_expr, num_frames)`: Generate sequence
- `expression_to_prompt(expression, base_prompt)`: Convert expression to prompt
- `generate_consistent_seed_sequence(base_seed, num_images, variation)`: Generate seeds
- `save_expression(expression, filepath)`: Save expression to JSON
- `load_expression(filepath)`: Load expression from JSON
- `list_available_expressions()`: List all expression names

### ExpressionVector

#### Attributes

- `happiness: float` (0.0 to 1.0)
- `sadness: float` (0.0 to 1.0)
- `anger: float` (0.0 to 1.0)
- `surprise: float` (0.0 to 1.0)
- `fear: float` (0.0 to 1.0)
- `disgust: float` (0.0 to 1.0)
- `neutral: float` (0.0 to 1.0)

#### Methods

- `to_array()`: Convert to numpy array
- `from_array(arr)`: Create from numpy array
- `normalize()`: Normalize vector to sum to 1.0

## Running Examples

Run the included example script:

```bash
python example_usage.py
```

This will demonstrate all major features of the expression generator.

## License

MIT License - See LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
