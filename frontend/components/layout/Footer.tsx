import Link from 'next/link';

export default function Footer() {
  // Footer updated for Mascot System
  return (
    <footer className="bg-white dark:bg-gray-900 border-t border-gray-200 dark:border-gray-800">
      <div className="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col md:flex-row justify-between items-center">
          <div className="mb-4 md:mb-0">
            <p className="text-center md:text-left text-gray-500 dark:text-gray-400 text-sm">
              &copy; {new Date().getFullYear()} The Moon Drip Bar. All rights reserved.
            </p>
            <p className="text-center md:text-left text-gray-400 dark:text-gray-500 text-xs mt-1">
              Roasting Management System v0.5.2
            </p>
          </div>
          <div className="flex space-x-6">
            <Link
              href="/mascot-showcase"
              className="text-gray-400 hover:text-gray-500 dark:hover:text-gray-300"
            >
              Mascot System
            </Link>
            <Link
              href="/design-demo"
              className="text-gray-400 hover:text-gray-500 dark:hover:text-gray-300"
            >
              Design Demo
            </Link>
            <a href="#" className="text-gray-400 hover:text-gray-500 dark:hover:text-gray-300">
              <span className="sr-only">Documentation</span>
              Docs
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
}
