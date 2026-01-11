"use client";

import { useEffect } from 'react';
import { useAuth } from '@clerk/nextjs';
import ApiClient from '@/lib/api';

export default function AuthBridge() {
  const { getToken } = useAuth();

  useEffect(() => {
    ApiClient.setAuthTokenProvider(async () => {
      try {
        const token = await getToken();
        return token || null;
      } catch {
        return null;
      }
    });
  }, [getToken]);

  return null;
}
