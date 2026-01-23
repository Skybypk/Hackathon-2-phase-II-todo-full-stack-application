import { UserRegister, UserLogin, Token, UserResponse } from '../types/auth';

const API_BASE_URLS = [
  process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000',
  'http://localhost:8000',
  'http://127.0.0.1:8000',
  'http://host.docker.internal:8000', // For Docker environments
];

class CustomAuthService {
  private apiBaseUrl: string | null = null;

  private async getApiUrl(): Promise<string> {
    if (this.apiBaseUrl) {
      return this.apiBaseUrl;
    }

    // Try each possible URL to find which one works
    for (const url of API_BASE_URLS) {
      try {
        // Increase timeout and add better error handling
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 10000); // 10 second timeout

        const response = await fetch(`${url}/`, {
          method: 'GET',
          cache: 'no-cache',
          signal: controller.signal
        });

        clearTimeout(timeoutId);

        if (response.ok) {
          this.apiBaseUrl = url;
          console.log(`Connected to backend at: ${url}`);
          return url;
        }
      } catch (error) {
        console.warn(`Failed to connect to ${url}:`, error);
        // URL didn't work, try the next one
        continue;
      }
    }

    // If none worked, return the primary URL and let the actual API calls handle the error
    this.apiBaseUrl = API_BASE_URLS[0];
    return this.apiBaseUrl;
  }

  private async makeRequest(endpoint: string, options: RequestInit) {
    let lastError: Error | null = null;

    // Try the cached URL first, then try others if that fails
    const urlsToTry = this.apiBaseUrl
      ? [this.apiBaseUrl, ...API_BASE_URLS.filter(url => url !== this.apiBaseUrl)]
      : API_BASE_URLS;

    for (const baseUrl of urlsToTry) {
      try {
        // Add timeout control for API requests
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 15000); // 15 second timeout

        const response = await fetch(`${baseUrl}${endpoint}`, {
          ...options,
          cache: 'no-cache',
          signal: controller.signal
        });

        clearTimeout(timeoutId);

        // Update the cached URL if this one works
        if (response.ok) {
          this.apiBaseUrl = baseUrl;
        }

        return response;
      } catch (error) {
        lastError = error as Error;
        console.warn(`Failed to connect to ${baseUrl}, trying next URL...`);
        continue;
      }
    }

    // If all URLs failed, throw the last error
    if (lastError) {
      throw lastError;
    } else {
      throw new Error('No backend URLs available');
    }
  }

  async register(userData: UserRegister): Promise<UserResponse> {
    try {
      const response = await this.makeRequest('/api/auth/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `Registration failed: ${response.status} ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Registration error:', error);
      if (error instanceof TypeError && (error.message.includes('fetch') || error.message.includes('network'))) {
        throw new Error('Failed to connect to the server. Please make sure the backend is running and accessible.');
      }
      if (error instanceof Error) {
        throw error;
      }
      throw new Error('An unexpected error occurred during registration');
    }
  }

  async login(credentials: UserLogin): Promise<Token> {
    try {
      const response = await this.makeRequest('/api/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(credentials),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `Login failed: ${response.status} ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Login error:', error);
      if (error instanceof TypeError && (error.message.includes('fetch') || error.message.includes('network'))) {
        throw new Error('Failed to connect to the server. Please make sure the backend is running and accessible.');
      }
      if (error instanceof Error) {
        throw error;
      }
      throw new Error('An unexpected error occurred during login');
    }
  }

  async getCurrentUser(token: string): Promise<UserResponse> {
    try {
      const response = await this.makeRequest('/api/auth/me', {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `Failed to get user: ${response.status} ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Get user error:', error);
      if (error instanceof TypeError && (error.message.includes('fetch') || error.message.includes('network'))) {
        throw new Error('Failed to connect to the server. Please make sure the backend is running and accessible.');
      }
      if (error instanceof Error) {
        throw error;
      }
      throw new Error('An unexpected error occurred while fetching user data');
    }
  }
}

export const customAuth = new CustomAuthService();