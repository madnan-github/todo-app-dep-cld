import { NextResponse } from 'next/server';

export async function GET() {
  try {
    // Basic health check - just return that the service is running
    const healthStatus = {
      status: 'healthy',
      timestamp: new Date().toISOString(),
      service: 'frontend',
      version: process.env.npm_package_version || '0.1.0',
      environment: process.env.NODE_ENV || 'development',
    };

    return NextResponse.json(healthStatus, { status: 200 });
  } catch (error) {
    const errorStatus = {
      status: 'unhealthy',
      timestamp: new Date().toISOString(),
      service: 'frontend',
      environment: process.env.NODE_ENV || 'development',
      error: error instanceof Error ? error.message : 'Unknown error',
    };

    return NextResponse.json(errorStatus, { status: 503 });
  }
}