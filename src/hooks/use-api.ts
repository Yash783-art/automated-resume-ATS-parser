import useSWR from 'swr';
import { useAuth } from '@clerk/nextjs';

const API_BASE_URL = ''; 

const fetcher = async ([url, userId]: [string, string]) => {
  const res = await fetch(`${API_BASE_URL}${url}`, {
    headers: {
      'X-Clerk-User-Id': userId,
    },
  });

  if (!res.ok) {
    const error = new Error('An error occurred while fetching the data.');
    const info = await res.json().catch(() => ({}));
    // @ts-ignore
    error.info = info;
    // @ts-ignore
    error.status = res.status;
    throw error;
  }

  return res.json();
};

export function useApi<T = any>(path: string | null) {
  const { userId } = useAuth();

  const { data, error, mutate, isLoading } = useSWR<T>(
    path && userId ? [path, userId] : null,
    fetcher,
    {
      revalidateOnFocus: false,
      shouldRetryOnError: false,
    }
  );

  return {
    data,
    isLoading,
    isError: error,
    mutate,
  };
}

export async function apiPost(path: string, body: any, userId: string) {
  if (!userId) {
    console.error("❌ API Error: No User ID found. Are you logged in?");
    throw new Error("Authentication required");
  }
  
  const url = `${API_BASE_URL}${path}`;
  console.log(`🚀 API Request: POST ${url}`);
  
  try {
    const res = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Clerk-User-Id': userId,
      },
      body: JSON.stringify(body),
    });
    
    if (!res.ok) throw new Error(`API Error: ${res.status}`);
    return res.json();
  } catch (err) {
    console.error(`❌ API Error for ${url}:`, err);
    throw err;
  }
}

export async function apiUpload(path: string, formData: FormData, userId: string) {
  const res = await fetch(`${API_BASE_URL}${path}`, {
    method: 'POST',
    headers: {
      'X-Clerk-User-Id': userId,
    },
    body: formData,
  });
  
  if (!res.ok) throw new Error('Upload failed');
  return res.json();
}
