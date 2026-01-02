import Link from "next/link";

export default function Home() {
  return (
    <div className="min-h-[calc(100vh-4rem)] flex items-center justify-center">
      <div className="text-center px-4">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          Welcome to Todo App
        </h1>
        <p className="text-lg text-gray-600 mb-8 max-w-md mx-auto">
          A simple, secure todo application to help you stay organized.
          Create an account to get started.
        </p>
        <div className="flex gap-4 justify-center">
          <Link
            href="/register"
            className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium"
          >
            Get Started
          </Link>
          <Link
            href="/login"
            className="px-6 py-3 bg-white text-gray-700 rounded-lg hover:bg-gray-100 font-medium border border-gray-300"
          >
            Sign In
          </Link>
        </div>
      </div>
    </div>
  );
}
