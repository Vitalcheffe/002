export interface User {
  id: string;
  email: string;
  created_at: string;
}

export interface Analysis {
  id: string;
  user_id: string;
  content: string;
  type: 'summary' | 'quiz' | 'mindmap';
  result: any;
  created_at: string;
}

export interface AnalysisResult {
  summary?: string;
  quiz?: Question[];
  mindmap?: MindMapNode[];
}

export interface Question {
  question: string;
  options: string[];
  correct_answer: number;
}

export interface MindMapNode {
  id: string;
  label: string;
  children: string[];
} 