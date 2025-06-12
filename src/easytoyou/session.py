"""
Session management for EasyToYou decoder
"""

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import bs4
import time
import logging
from typing import Optional, Dict, Any

from .exceptions import LoginError, NetworkError

logger = logging.getLogger(__name__)

class SessionManager:
    """Manages HTTP session with easytoyou.eu"""
    
    def __init__(self, base_url: str = "https://easytoyou.eu"):
        self.base_url = base_url
        self.session: Optional[requests.Session] = None
        self.is_authenticated = False
        
        # Enhanced headers to avoid bot detection
        self.headers = {
            "Connection": "keep-alive",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "DNT": "1",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"'
        }
    
    def setup_session(self) -> requests.Session:
        """Setup session with retry strategy and connection pooling"""
        self.session = requests.Session()
        
        # Retry strategy
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        
        adapter = HTTPAdapter(
            max_retries=retry_strategy,
            pool_connections=10,
            pool_maxsize=20
        )
        
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        self.session.headers.update(self.headers)
        
        return self.session
    
    def login(self, username: str, password: str) -> bool:
        """
        Login to easytoyou.eu
        
        Args:
            username: easytoyou.eu username
            password: easytoyou.eu password
            
        Returns:
            True if login successful, False otherwise
            
        Raises:
            LoginError: If login fails
            NetworkError: If network request fails
        """
        logger.info("Attempting to login...")
        
        if not self.session:
            self.setup_session()
        
        try:
            # Get login page
            login_page = f"{self.base_url}/login"
            response = self.session.get(login_page, timeout=30)
            response.raise_for_status()
            
            # Add delay to avoid rate limiting
            time.sleep(1)
            
            # Parse login form for hidden fields
            soup = bs4.BeautifulSoup(response.content, 'html.parser')
            login_form = soup.find('form')
            
            login_data = {
                "loginname": username,
                "password": password
            }
            
            # Add hidden fields
            if login_form:
                for hidden_input in login_form.find_all('input', type='hidden'):
                    if hidden_input.get('name') and hidden_input.get('value'):
                        login_data[hidden_input['name']] = hidden_input['value']
            
            # Update headers for POST request
            post_headers = self.headers.copy()
            post_headers.update({
                "Content-Type": "application/x-www-form-urlencoded",
                "Origin": self.base_url,
                "Referer": login_page
            })
            
            # Submit login
            resp = self.session.post(
                login_page,
                headers=post_headers,
                data=login_data,
                allow_redirects=True,
                timeout=30
            )
            resp.raise_for_status()
            
            # Check if login successful
            if "/account" in resp.url or "dashboard" in resp.url.lower():
                logger.info("Login successful!")
                self.is_authenticated = True
                return True
            else:
                logger.error(f"Login failed. Redirected to: {resp.url}")
                self.is_authenticated = False
                
                # Check for error messages
                soup = bs4.BeautifulSoup(resp.content, 'html.parser')
                error_msgs = soup.find_all(['div', 'span'], class_=['error', 'alert-danger'])
                error_text = ""
                for msg in error_msgs:
                    error_text += msg.get_text().strip() + " "
                
                raise LoginError(f"Login failed: {error_text}")
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Login request failed: {e}")
            raise NetworkError(f"Network error during login: {e}")
        except Exception as e:
            logger.error(f"Unexpected error during login: {e}")
            raise LoginError(f"Login failed: {e}")
    
    def get(self, url: str, **kwargs) -> requests.Response:
        """Make GET request with session"""
        if not self.session:
            raise NetworkError("Session not initialized")
        return self.session.get(url, **kwargs)
    
    def post(self, url: str, **kwargs) -> requests.Response:
        """Make POST request with session"""
        if not self.session:
            raise NetworkError("Session not initialized")
        return self.session.post(url, **kwargs)
    
    def close(self):
        """Close session"""
        if self.session:
            self.session.close()
            self.session = None
            self.is_authenticated = False