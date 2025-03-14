import { analysisSchema } from '../validations/schemas';

describe('Validation Schemas', () => {
  it('should validate correct analysis input', () => {
    const validInput = {
      content: 'Contenu valide avec plus de 10 caractères',
      type: 'summary' as const
    };
    
    expect(() => analysisSchema.parse(validInput)).not.toThrow();
  });

  it('should reject short content', () => {
    const invalidInput = {
      content: 'Court',
      type: 'summary' as const
    };
    
    expect(() => analysisSchema.parse(invalidInput)).toThrow();
  });
}); 