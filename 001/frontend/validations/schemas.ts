import { z } from 'zod';

export const analysisSchema = z.object({
  content: z.string()
    .min(10, "Le texte doit contenir au moins 10 caractères")
    .max(5000, "Le texte ne doit pas dépasser 5000 caractères"),
  type: z.enum(['summary', 'quiz', 'mindmap']),
  language: z.enum(['fr', 'en']).optional().default('fr')
});

export const userSchema = z.object({
  email: z.string().email("Email invalide"),
  password: z.string()
    .min(8, "Le mot de passe doit contenir au moins 8 caractères")
    .regex(/[A-Z]/, "Doit contenir au moins une majuscule")
    .regex(/[0-9]/, "Doit contenir au moins un chiffre"),
  fullName: z.string().min(2, "Le nom doit contenir au moins 2 caractères")
}); 