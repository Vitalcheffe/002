import 'react-native-url-polyfill/auto';
import { createClient } from '@supabase/supabase-js';

const supabaseUrl = 'https://brvviulhbesqtahkopix.supabase.co';
const supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJydnZpdWxoYmVzcXRhaGtvcGl4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDE5MDg5ODYsImV4cCI6MjA1NzQ4NDk4Nn0.l1fd-Q9Z5ZsOHfU3vKe0TzAi7Q2F8M23_8ol0Uqjx7Q';

export const supabase = createClient(supabaseUrl, supabaseKey); 