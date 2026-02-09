import type { NextConfig } from "next";

const backendUrl = process.env.BACKEND_URL || 'http://localhost:8000';

const nextConfig: NextConfig = {
  output: 'standalone',
  async rewrites() {
    return [
      {
        source: "/api/:path*",
        destination: `${backendUrl}/api/:path*`,
      },
    ];
  },
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || `${backendUrl}/api`,
    NEXT_PUBLIC_USE_REWRITE_PROXY: 'true',
  },
};

export default nextConfig;
