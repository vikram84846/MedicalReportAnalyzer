
import { Heart } from 'lucide-react';

export const Header = () => {
  return (
    <header className="bg-white shadow-sm border-b">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="p-2 bg-red-100 rounded-lg">
              <Heart className="w-6 h-6 text-red-500" />
            </div>
            <span className="text-xl font-bold text-gray-800">MedAnalyzer</span>
          </div>
          <nav className="hidden md:flex items-center gap-6">
            <a href="#" className="text-gray-600 hover:text-gray-800 transition-colors">About</a>
            <a href="#" className="text-gray-600 hover:text-gray-800 transition-colors">Privacy</a>
            <a href="#" className="text-gray-600 hover:text-gray-800 transition-colors">Support</a>
          </nav>
        </div>
      </div>
    </header>
  );
};
