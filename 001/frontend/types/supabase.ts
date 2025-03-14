export type Profile = {
  id: string;
  email: string;
  full_name: string | null;
  avatar_url: string | null;
  created_at: string;
};

export type Analysis = {
  id: string;
  user_id: string;
  content: string;
  type: 'summary' | 'quiz' | 'mindmap';
  result: any;
  status: 'pending' | 'completed' | 'error';
  created_at: string;
};

export type Subscription = {
  id: string;
  user_id: string;
  plan_type: 'free' | 'premium' | 'enterprise';
  status: 'active' | 'cancelled' | 'expired';
  valid_until: string;
  created_at: string;
}; 