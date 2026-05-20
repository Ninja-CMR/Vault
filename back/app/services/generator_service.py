import secrets
import string
import math
from app.schemas.generator import GeneratePasswordSchema, GeneratedPasswordResponseSchema

class PasswordGeneratorService:
    @staticmethod
    def generate_password(options: GeneratePasswordSchema) -> GeneratedPasswordResponseSchema:
        # 1. Construire le pool de caractères
        pool = ""
        if options.include_lowercase:
            pool += string.ascii_lowercase
        if options.include_uppercase:
            pool += string.ascii_uppercase
        if options.include_numbers:
            pool += string.digits
        if options.include_symbols:
            pool += string.punctuation

        if not pool:
            # Fallback si rien n'est sélectionné
            pool = string.ascii_lowercase

        # 2. Utiliser un générateur sécurisé
        password = ''.join(secrets.choice(pool) for _ in range(options.length))

        # 3. Calculer l'entropie et la robustesse
        entropy = PasswordGeneratorService.calculate_entropy(len(pool), options.length)
        strength = PasswordGeneratorService.calculate_strength(entropy)

        return GeneratedPasswordResponseSchema(
            password=password,
            strength=strength,
            entropy_score=round(entropy, 2)
        )

    @staticmethod
    def calculate_entropy(pool_size: int, length: int) -> float:
        """Calcul de l'entropie: log2(pool_size^length) = length * log2(pool_size)"""
        if pool_size <= 0:
            return 0
        return length * math.log2(pool_size)

    @staticmethod
    def calculate_strength(entropy: float) -> str:
        """Catégorisation de la robustesse basée sur l'entropie."""
        if entropy < 40:
            return "Faible (Weak)"
        elif entropy < 60:
            return "Moyenne (Moderate)"
        elif entropy < 80:
            return "Forte (Strong)"
        else:
            return "Très Forte (Very Strong)"
