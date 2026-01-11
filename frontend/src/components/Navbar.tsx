import Link from 'next/link';
import { Music, Menu, X } from 'lucide-react';
import { useState } from 'react';
import { UserButton, SignedIn, SignedOut, SignInButton } from '@clerk/nextjs';

export default function Navbar() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <nav className="bg-white/80 dark:bg-zinc-950/80 backdrop-blur-md border-b border-zinc-200 dark:border-zinc-800 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link href="/" className="flex items-center space-x-2">
              <div className="bg-indigo-600 p-2 rounded-lg">
                <Music className="w-6 h-6 text-white" />
              </div>
              <span className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-indigo-600 to-purple-600">
                EuphonicAI
              </span>
            </Link>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-8">
            <Link href="/" className="text-zinc-600 dark:text-zinc-300 hover:text-indigo-600 dark:hover:text-indigo-400 transition-colors font-medium">
              Home
            </Link>
            <Link href="#features" className="text-zinc-600 dark:text-zinc-300 hover:text-indigo-600 dark:hover:text-indigo-400 transition-colors font-medium">
              Features
            </Link>
            
            <SignedIn>
              <div className="flex items-center gap-4 pl-4 border-l border-zinc-200 dark:border-zinc-800">
                <UserButton 
                  afterSignOutUrl="/"
                  appearance={{
                    elements: {
                      userButtonAvatarBox: 'w-10 h-10 border-2 border-indigo-500/20',
                      userButtonPopoverCard: 'shadow-2xl border border-zinc-200 rounded-2xl overflow-hidden',
                      userButtonPopoverActionButton: 'hover:bg-zinc-50 transition-all',
                      userButtonPopoverActionButtonText: 'font-medium',
                    }
                  }}
                />
              </div>
            </SignedIn>
            
            <SignedOut>
              <SignInButton mode="modal">
                <button className="bg-indigo-600 text-white px-5 py-2 rounded-full font-medium hover:bg-indigo-700 transition-all shadow-md hover:shadow-lg">
                  Sign In
                </button>
              </SignInButton>
            </SignedOut>
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden flex items-center space-x-4">
            <SignedIn>
              <UserButton 
                afterSignOutUrl="/"
                appearance={{
                  elements: {
                    userButtonAvatarBox: 'w-9 h-9 border-2 border-indigo-500/20',
                  }
                }}
              />
            </SignedIn>
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="p-2 text-zinc-600 dark:text-zinc-300 hover:bg-zinc-100 dark:hover:bg-zinc-900 rounded-lg transition-colors"
            >
              {isOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Navigation */}
      {isOpen && (
        <div className="md:hidden bg-white dark:bg-zinc-950 border-b border-zinc-200 dark:border-zinc-800 animate-in slide-in-from-top duration-300">
          <div className="px-4 pt-2 pb-6 space-y-1">
            <Link
              href="/"
              className="block px-3 py-3 text-zinc-600 dark:text-zinc-300 hover:text-indigo-600 font-medium rounded-xl hover:bg-zinc-50 dark:hover:bg-zinc-900"
              onClick={() => setIsOpen(false)}
            >
              Home
            </Link>
            <Link
              href="#features"
              className="block px-3 py-3 text-zinc-600 dark:text-zinc-300 hover:text-indigo-600 font-medium rounded-xl hover:bg-zinc-50 dark:hover:bg-zinc-900"
              onClick={() => setIsOpen(false)}
            >
              Features
            </Link>
            <SignedOut>
              <div className="pt-4">
                <SignInButton mode="modal">
                  <button className="w-full bg-indigo-600 text-white px-5 py-3 rounded-xl font-bold shadow-lg shadow-indigo-500/20">
                    Sign In
                  </button>
                </SignInButton>
              </div>
            </SignedOut>
          </div>
        </div>
      )}
    </nav>
  );
}
