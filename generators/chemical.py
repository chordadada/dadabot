import random
from .chem_generator import OrganicGenerator, InorganicGenerator

def generate_iupac_name() -> str:
    if random.choice([True, False]):
        generator = OrganicGenerator()
    else:
        generator = InorganicGenerator()
    
    name, formula = generator.generate()
    return f"{name} ({formula})"
		
