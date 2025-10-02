"""
Vector Expression Consistent Generator for Stable Diffusion

This module provides functionality to generate consistent facial expressions
and character poses across multiple images using vector embeddings and 
expression control parameters.
"""

import json
import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict


@dataclass
class ExpressionVector:
    """Represents a facial expression as a vector of parameters."""
    happiness: float = 0.0  # Range: -1.0 to 1.0
    sadness: float = 0.0
    anger: float = 0.0
    surprise: float = 0.0
    fear: float = 0.0
    disgust: float = 0.0
    neutral: float = 1.0
    
    def to_array(self) -> np.ndarray:
        """Convert expression to numpy array."""
        return np.array([
            self.happiness,
            self.sadness,
            self.anger,
            self.surprise,
            self.fear,
            self.disgust,
            self.neutral
        ])
    
    @classmethod
    def from_array(cls, arr: np.ndarray) -> 'ExpressionVector':
        """Create expression from numpy array."""
        return cls(
            happiness=float(arr[0]),
            sadness=float(arr[1]),
            anger=float(arr[2]),
            surprise=float(arr[3]),
            fear=float(arr[4]),
            disgust=float(arr[5]),
            neutral=float(arr[6])
        )
    
    def normalize(self) -> 'ExpressionVector':
        """Normalize the expression vector to sum to 1.0."""
        arr = self.to_array()
        total = np.sum(np.abs(arr))
        if total > 0:
            arr = arr / total
        return ExpressionVector.from_array(arr)


class VectorExpressionGenerator:
    """
    Generator for consistent facial expressions across multiple images.
    
    This class manages expression vectors and generates prompts and
    embeddings for consistent character expression generation.
    """
    
    def __init__(self, seed: Optional[int] = None):
        """
        Initialize the expression generator.
        
        Args:
            seed: Random seed for reproducibility
        """
        self.seed = seed
        if seed is not None:
            np.random.seed(seed)
        
        self.base_expressions = self._initialize_base_expressions()
        self.custom_expressions: Dict[str, ExpressionVector] = {}
    
    def _initialize_base_expressions(self) -> Dict[str, ExpressionVector]:
        """Initialize common base expression presets."""
        return {
            'neutral': ExpressionVector(neutral=1.0),
            'happy': ExpressionVector(happiness=0.8, neutral=0.2),
            'very_happy': ExpressionVector(happiness=1.0),
            'sad': ExpressionVector(sadness=0.8, neutral=0.2),
            'very_sad': ExpressionVector(sadness=1.0),
            'angry': ExpressionVector(anger=0.8, neutral=0.2),
            'very_angry': ExpressionVector(anger=1.0),
            'surprised': ExpressionVector(surprise=0.8, neutral=0.2),
            'very_surprised': ExpressionVector(surprise=1.0),
            'fearful': ExpressionVector(fear=0.8, neutral=0.2),
            'disgusted': ExpressionVector(disgust=0.8, neutral=0.2),
            'smiling': ExpressionVector(happiness=0.6, neutral=0.4),
            'laughing': ExpressionVector(happiness=0.9, surprise=0.1),
            'crying': ExpressionVector(sadness=0.9, neutral=0.1),
            'shocked': ExpressionVector(surprise=0.7, fear=0.3),
            'annoyed': ExpressionVector(anger=0.4, disgust=0.2, neutral=0.4),
        }
    
    def get_expression(self, name: str) -> Optional[ExpressionVector]:
        """
        Get an expression by name.
        
        Args:
            name: Name of the expression
            
        Returns:
            ExpressionVector if found, None otherwise
        """
        if name in self.base_expressions:
            return self.base_expressions[name]
        elif name in self.custom_expressions:
            return self.custom_expressions[name]
        return None
    
    def add_custom_expression(self, name: str, expression: ExpressionVector):
        """
        Add a custom expression to the generator.
        
        Args:
            name: Name for the custom expression
            expression: The expression vector
        """
        self.custom_expressions[name] = expression
    
    def interpolate_expressions(
        self, 
        expr1: ExpressionVector, 
        expr2: ExpressionVector, 
        t: float
    ) -> ExpressionVector:
        """
        Interpolate between two expressions.
        
        Args:
            expr1: First expression
            expr2: Second expression
            t: Interpolation parameter (0.0 to 1.0)
            
        Returns:
            Interpolated expression
        """
        arr1 = expr1.to_array()
        arr2 = expr2.to_array()
        interpolated = (1 - t) * arr1 + t * arr2
        return ExpressionVector.from_array(interpolated)
    
    def generate_expression_sequence(
        self,
        start_expr: str,
        end_expr: str,
        num_frames: int
    ) -> List[ExpressionVector]:
        """
        Generate a sequence of expressions transitioning from start to end.
        
        Args:
            start_expr: Name of starting expression
            end_expr: Name of ending expression
            num_frames: Number of frames in sequence
            
        Returns:
            List of expression vectors
        """
        expr1 = self.get_expression(start_expr)
        expr2 = self.get_expression(end_expr)
        
        if expr1 is None or expr2 is None:
            raise ValueError(f"Expression not found: {start_expr} or {end_expr}")
        
        sequence = []
        for i in range(num_frames):
            t = i / (num_frames - 1) if num_frames > 1 else 0
            sequence.append(self.interpolate_expressions(expr1, expr2, t))
        
        return sequence
    
    def expression_to_prompt(
        self,
        expression: ExpressionVector,
        base_prompt: str = ""
    ) -> str:
        """
        Convert an expression vector to a text prompt for Stable Diffusion.
        
        Args:
            expression: The expression vector
            base_prompt: Base prompt to append expression to
            
        Returns:
            Text prompt including expression descriptors
        """
        arr = expression.to_array()
        expr_names = [
            'happy', 'sad', 'angry', 'surprised', 
            'fearful', 'disgusted', 'neutral'
        ]
        
        # Find dominant expressions (threshold > 0.2)
        dominant = []
        for i, val in enumerate(arr):
            if val > 0.2:
                intensity = "very " if val > 0.7 else ""
                dominant.append(f"{intensity}{expr_names[i]}")
        
        if not dominant:
            dominant = ['neutral expression']
        
        expression_text = " and ".join(dominant)
        
        if base_prompt:
            return f"{base_prompt}, {expression_text}"
        return expression_text
    
    def generate_consistent_seed_sequence(
        self,
        base_seed: int,
        num_images: int,
        variation: int = 1000
    ) -> List[int]:
        """
        Generate a sequence of related seeds for consistent generation.
        
        Args:
            base_seed: Starting seed value
            num_images: Number of seeds to generate
            variation: Maximum variation from base seed
            
        Returns:
            List of seed values
        """
        np.random.seed(base_seed)
        seeds = [base_seed]
        
        for i in range(1, num_images):
            # Generate seeds close to the base seed for consistency
            offset = np.random.randint(-variation, variation)
            seeds.append(base_seed + offset)
        
        return seeds
    
    def save_expression(self, expression: ExpressionVector, filepath: str):
        """Save an expression to a JSON file."""
        with open(filepath, 'w') as f:
            json.dump(asdict(expression), f, indent=2)
    
    def load_expression(self, filepath: str) -> ExpressionVector:
        """Load an expression from a JSON file."""
        with open(filepath, 'r') as f:
            data = json.load(f)
        return ExpressionVector(**data)
    
    def save_expression_sequence(
        self,
        sequence: List[ExpressionVector],
        filepath: str
    ):
        """Save an expression sequence to a JSON file."""
        data = [asdict(expr) for expr in sequence]
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_expression_sequence(self, filepath: str) -> List[ExpressionVector]:
        """Load an expression sequence from a JSON file."""
        with open(filepath, 'r') as f:
            data = json.load(f)
        return [ExpressionVector(**expr_data) for expr_data in data]
    
    def list_available_expressions(self) -> List[str]:
        """List all available expression names."""
        return list(self.base_expressions.keys()) + list(self.custom_expressions.keys())


def create_expression_config(
    expression_name: str,
    seed: int,
    num_images: int = 1,
    output_file: str = "expression_config.json"
) -> Dict:
    """
    Create a configuration file for batch generation.
    
    Args:
        expression_name: Name of the expression to use
        seed: Random seed for generation
        num_images: Number of images to generate
        output_file: Path to save configuration
        
    Returns:
        Configuration dictionary
    """
    generator = VectorExpressionGenerator(seed=seed)
    expression = generator.get_expression(expression_name)
    
    if expression is None:
        raise ValueError(f"Expression '{expression_name}' not found")
    
    seeds = generator.generate_consistent_seed_sequence(seed, num_images)
    
    config = {
        "expression": expression_name,
        "expression_vector": asdict(expression),
        "seeds": seeds,
        "num_images": num_images,
        "base_seed": seed
    }
    
    with open(output_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    return config


if __name__ == "__main__":
    # Example usage
    print("Vector Expression Consistent Generator")
    print("=" * 50)
    
    # Create generator
    generator = VectorExpressionGenerator(seed=42)
    
    # List available expressions
    print("\nAvailable expressions:")
    for expr_name in generator.list_available_expressions():
        print(f"  - {expr_name}")
    
    # Generate a happy expression prompt
    happy_expr = generator.get_expression('happy')
    prompt = generator.expression_to_prompt(
        happy_expr,
        "portrait of a young woman"
    )
    print(f"\nExample prompt: {prompt}")
    
    # Generate expression sequence
    print("\nGenerating expression sequence from 'neutral' to 'happy'...")
    sequence = generator.generate_expression_sequence('neutral', 'happy', 5)
    for i, expr in enumerate(sequence):
        prompt = generator.expression_to_prompt(expr)
        print(f"  Frame {i}: {prompt}")
    
    # Generate consistent seeds
    seeds = generator.generate_consistent_seed_sequence(42, 5)
    print(f"\nConsistent seeds: {seeds}")
    
    print("\n" + "=" * 50)
    print("Generator ready for use!")
