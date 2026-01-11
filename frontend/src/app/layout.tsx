import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';
import {
  ClerkProvider,
  SignInButton,
  SignUpButton,
  SignedIn,
  SignedOut,
  UserButton,
} from '@clerk/nextjs';
import { dark } from '@clerk/themes';
import AuthBridge from '@/components/AuthBridge';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'Moodify - AI-Powered Music Recommendations',
  description: 'Discover music that matches your mood using AI-powered emotion detection',
  icons: {
    icon: '/favicon.ico',
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <ClerkProvider
      appearance={{
        baseTheme: undefined,
        variables: {
          colorPrimary: '#4f46e5', // indigo-600
          colorText: '#18181b', // zinc-900
          colorBackground: '#ffffff',
          borderRadius: '1rem',
        },
        elements: {
          card: 'shadow-2xl border border-zinc-200',
          formButtonPrimary: 'bg-indigo-600 hover:bg-indigo-700 text-sm font-bold transition-all shadow-lg shadow-indigo-500/20',
          footerActionLink: 'text-indigo-600 hover:text-indigo-700 font-bold',
          identityPreviewEditButtonIcon: 'text-indigo-600',
          formFieldInput: 'rounded-xl border-zinc-200 focus:ring-2 focus:ring-indigo-500 transition-all',
          socialButtonsBlockButton: 'rounded-xl border-zinc-200 hover:bg-zinc-50 transition-all',
          socialButtonsBlockButtonText: 'font-semibold',
        }
      }}
    >
      <html lang="en">
        <body className={inter.className}>
          <AuthBridge />
          <header className="p-4 flex items-center justify-end gap-3">
            <SignedOut>
              <SignInButton />
              <SignUpButton />
            </SignedOut>
            <SignedIn>
              <UserButton />
            </SignedIn>
          </header>
          {children}
        </body>
      </html>
    </ClerkProvider>
  );
}
