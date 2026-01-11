import { Music, Github, Twitter, Linkedin } from 'lucide-react';
import Link from 'next/link';

export default function Footer() {
  return (
    <footer className="bg-zinc-50 dark:bg-zinc-900 border-t border-zinc-200 dark:border-zinc-800 pt-16 pb-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-12 mb-12">
          <div className="col-span-1 md:col-span-1">
            <Link href="/" className="flex items-center space-x-2 mb-6">
              <div className="bg-indigo-600 p-1.5 rounded-lg">
                <Music className="w-5 h-5 text-white" />
              </div>
              <span className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-indigo-600 to-purple-600">
                EuphonicAI
              </span>
            </Link>
            <p className="text-zinc-500 dark:text-zinc-400 mb-6 max-w-xs">
              Personalizing your music experience through emotional intelligence and machine learning.
            </p>
            <div className="flex space-x-4">
              <a href="#" className="text-zinc-400 hover:text-indigo-600 transition-colors">
                <Github className="w-5 h-5" />
              </a>
              <a href="#" className="text-zinc-400 hover:text-indigo-600 transition-colors">
                <Twitter className="w-5 h-5" />
              </a>
              <a href="#" className="text-zinc-400 hover:text-indigo-600 transition-colors">
                <Linkedin className="w-5 h-5" />
              </a>
            </div>
          </div>

          <div>
            <h3 className="text-sm font-semibold text-zinc-900 dark:text-zinc-100 uppercase tracking-wider mb-4">
              Product
            </h3>
            <ul className="space-y-3">
              <li>
                <Link href="#features" className="text-zinc-600 dark:text-zinc-400 hover:text-indigo-600 transition-colors">
                  Features
                </Link>
              </li>
              <li>
                <Link href="#how-it-works" className="text-zinc-600 dark:text-zinc-400 hover:text-indigo-600 transition-colors">
                  How it Works
                </Link>
              </li>
              <li>
                <Link href="#" className="text-zinc-600 dark:text-zinc-400 hover:text-indigo-600 transition-colors">
                  Music Analysis
                </Link>
              </li>
            </ul>
          </div>

          <div>
            <h3 className="text-sm font-semibold text-zinc-900 dark:text-zinc-100 uppercase tracking-wider mb-4">
              Company
            </h3>
            <ul className="space-y-3">
              <li>
                <Link href="#" className="text-zinc-600 dark:text-zinc-400 hover:text-indigo-600 transition-colors">
                  About Us
                </Link>
              </li>
              <li>
                <Link href="#" className="text-zinc-600 dark:text-zinc-400 hover:text-indigo-600 transition-colors">
                  Privacy Policy
                </Link>
              </li>
              <li>
                <Link href="#" className="text-zinc-600 dark:text-zinc-400 hover:text-indigo-600 transition-colors">
                  Terms of Service
                </Link>
              </li>
            </ul>
          </div>

          <div>
            <h3 className="text-sm font-semibold text-zinc-900 dark:text-zinc-100 uppercase tracking-wider mb-4">
              Stay Connected
            </h3>
            <p className="text-zinc-600 dark:text-zinc-400 mb-4 text-sm">
              Subscribe to our newsletter for the latest updates.
            </p>
            <form className="flex space-x-2">
              <input
                type="email"
                placeholder="Email address"
                className="bg-white dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 px-4 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-600 w-full text-sm"
              />
              <button className="bg-indigo-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-indigo-700 transition-colors">
                Join
              </button>
            </form>
          </div>
        </div>
        <div className="border-t border-zinc-200 dark:border-zinc-800 pt-8 flex flex-col md:flex-row justify-between items-center">
          <p className="text-zinc-400 text-sm mb-4 md:mb-0">
            © 2026 EuphonicAI. All rights reserved.
          </p>
          <div className="flex space-x-6 text-sm text-zinc-400">
            <span>Made with ❤️ for music lovers</span>
          </div>
        </div>
      </div>
    </footer>
  );
}
