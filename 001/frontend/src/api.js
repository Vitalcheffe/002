const API_BASE_URL = process.env.API_BASE_URL;

export const analyzeContent = async (content, type) => {
  try {
    const response = await fetch(`${API_BASE_URL}/analyze`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ content, type }),
    });
    return await response.json();
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
}; 