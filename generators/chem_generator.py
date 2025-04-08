# chem_generator.py
import random
from typing import Dict, List, Tuple

class OrganicGenerator:
    def __init__(self):
        self.rules = {
            "алканы": {
                "root": ["мет", "эт", "проп", "бут", "пент"],
                "suffix": ["ан"],
                "formula": lambda n: f"C{n}H{2*n + 2}"
            },
            "алкены": {
                "root": ["проп", "бут", "пент"],
                "suffix": ["ен", "диен"],
                "formula": lambda n: f"C{n}H{2*n}"
            },
            "циклоалканы": {
                "root": ["циклопроп", "циклобут"],
                "suffix": ["ан"],
                "formula": lambda n: f"C{n}H{2*n}"
            }
        }

    def generate(self) -> tuple:
        compound_type = random.choice(list(self.rules.keys()))
        
        while True:
            data = self.rules[compound_type]
            n = random.randint(3, 8)
            prefix = self._get_prefix(compound_type)
            root = random.choice(data["root"])
            
            if self._validate_combination(compound_type, root):
                break
        
        suffix = random.choice(data["suffix"])
        formula = data["formula"](n)
        number = self._numbering(compound_type)
        
        return f"{number}{prefix}{root}{suffix}", formula

    def _get_prefix(self, c_type: str) -> str:
        if "цикло" in c_type: 
            return ""
        return random.choice(["", "2-метил", "3-этил", "5-бутил", "4-пропил"])

    def _numbering(self, c_type: str) -> str:
        if "цикло" not in c_type: 
            return ""
        return random.choice(["1-", "1,2-", "1,3-"])

    def _validate_combination(self, c_type: str, root: str) -> bool:
        if "цикло" in c_type: 
            return "цикло" in root
        return "цикло" not in root

class InorganicGenerator:
    def __init__(self):
        # Базы данных для генерации
        self.elements = {
            "металлы": {
                "Na": {"валентности": [1], "название": "натрий"},
                "Fe": {"валентности": [2, 3], "название": "железо"},
                "Al": {"валентности": [3], "название": "алюминий"}
            },
            "неметаллы": {
                "O": {"валентность": -2, "название": "кислород"},
                "Cl": {"валентность": -1, "название": "хлор"}
            },
            "кислотные_остатки": {
                "SO4": {"валентность": -2, "название": "сульфат"},
                "NO3": {"валентность": -1, "название": "нитрат"},
                "PO4": {"валентность": -3, "название": "фосфат"}
            }
        }

        self.compound_types = {
            "оксиды": {
                "шаблон_названия": lambda elem, val: f"оксид {elem} ({val})" if val else f"оксид {elem}",
                "формула": self._generate_oxide
            },
            "кислоты": {
                "шаблон_названия": lambda acid: f"{acid} кислота",
                "формула": self._generate_acid
            },
            "соли": {
                "шаблон_названия": lambda metal, residue: f"{residue} {metal}",
                "формула": self._generate_salt
            }
        }

    def generate(self) -> Tuple[str, str]:
        """Генерирует неорганическое соединение и его формулу."""
        compound_type = random.choice(list(self.compound_types.keys()))
        
        if compound_type == "оксиды":
            element, valence = self._get_metal_with_valence()
            formula = self.compound_types[compound_type]["формула"](element, valence)
            name = self.compound_types[compound_type]["шаблон_названия"](
                self.elements["металлы"][element]["название"],
                valence if len(self.elements["металлы"][element]["валентности"]) > 1 else None
            )
        
        elif compound_type == "кислоты":
            formula, acid_name = self.compound_types[compound_type]["формула"]()
            name = self.compound_types[compound_type]["шаблон_названия"](acid_name)
        
        elif compound_type == "соли":
            metal, residue, formula = self.compound_types[compound_type]["формула"]()
            name = self.compound_types[compound_type]["шаблон_названия"](
                self.elements["металлы"][metal]["название"],
                self.elements["кислотные_остатки"][residue]["название"]
            )
        
        return name.title(), formula

    def _generate_oxide(self, metal: str, valence: int) -> str:
        """Генерирует формулу оксида: Fe2O3, Al2O3 и т.д."""
        oxygen_valence = self.elements["неметаллы"]["O"]["валентность"]
        lcm = abs(valence * oxygen_valence)
        metal_count = lcm // abs(valence)
        oxygen_count = lcm // abs(oxygen_valence)
        return f"{metal}{metal_count if metal_count > 1 else ''}O{oxygen_count if oxygen_count > 1 else ''}"

    def _generate_acid(self) -> Tuple[str, str]:
        """Генерирует кислоту: H2SO4 → серная кислота."""
        residue = random.choice(list(self.elements["кислотные_остатки"].keys()))
        h_count = abs(self.elements["кислотные_остатки"][residue]["валентность"])
        formula = f"H{h_count if h_count > 1 else ''}{residue}"
        acid_name = self._get_acid_name(residue)
        return formula, acid_name

    def _generate_salt(self) -> Tuple[str, str, str]:
        """Генерирует соль: Fe2(SO4)3 → сульфат железа(III)."""
        metal, metal_valence = self._get_metal_with_valence()
        residue = random.choice(list(self.elements["кислотные_остатки"].keys()))
        residue_valence = self.elements["кислотные_остатки"][residue]["валентность"]
        
        # Подбор коэффициентов
        lcm = abs(metal_valence * residue_valence)
        residue_count = lcm // abs(metal_valence)
        metal_count = lcm // abs(residue_valence)
        
        formula = f"{metal}{metal_count if metal_count > 1 else ''}({residue}){residue_count if residue_count > 1 else ''}"
        return metal, residue, formula

    def _get_metal_with_valence(self) -> Tuple[str, int]:
        """Возвращает случайный металл и его валентность."""
        metal = random.choice(list(self.elements["металлы"].keys()))
        valence = random.choice(self.elements["металлы"][metal]["валентности"])
        return metal, valence

    def _get_acid_name(self, residue: str) -> str:
        """Возвращает название кислоты по остатку."""
        names = {
            "SO4": "серная",
            "NO3": "азотная",
            "PO4": "фосфорная"
        }
        return names.get(residue, "неизвестная")

# Пример использования
# if __name__ == "__main__":
    # generator = InorganicGenerator()
    # for _ in range(5):
        # print(generator.generate())