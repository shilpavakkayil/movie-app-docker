"""
Movie Client

A command-line application that connects to the movie server and prints the number of films 
in the database for each input year.
"""

import argparse
import json
import sys
import time
from dataclasses import dataclass
from typing import Optional
import requests
from requests.exceptions import RequestException
from datetime import datetime


@dataclass
class AuthToken:
    bearer: str
    timeout: int
    created_at: float
    
    #method to check if the token is expired or not
    @property
    def is_expired(self):
        return time.time() - self.created_at >= self.timeout - 1 



class MovieClient:
    """Client class for interacting with the movie database server."""
    """ 
        Inputs:
            base_url: The base URL of the movie-server
            username: Username
            password: Password
    """
    def __init__(self, base_url: str = "http://localhost:8080", 
                 username: str = "username", password: str = "password"):
        
        self.base_url = base_url.rstrip('/')
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.token: Optional[AuthToken] = None
    
    """
        Method to authenticate with the server and get the bearer token
    """
    def authenticate(self):
        
        url = f"{self.base_url}/api/auth"
        payload = {
            "username": self.username,
            "password": self.password
        }
        
        try:
            response = self.session.post(
                url, 
                json=payload,
                timeout=10
            )
            response.raise_for_status()
            
            auth_data = response.json()
            self.token = AuthToken(
                bearer=auth_data["bearer"],
                timeout=auth_data["timeout"],
                created_at=time.time()
            )
            
        except RequestException as e:
            raise Exception(f"Authentication failed: {e}")
        except KeyError as e:
            raise Exception(f"Invalid authentication response: missing {e}")
        
    # Method to ensure that the authentication token is valid and not expired
    def _ensure_authenticated(self):
        if not self.token or self.token.is_expired:
            self.authenticate()
    
    def get_movies_page(self, year: int, page: int):
        """
        Get movies for a specific year and page.
        Input:
            year: The year to query
            page: The page number
        Returns:
            List of movie dictionaries
        """
        self._ensure_authenticated()
        
        movies_url = f"{self.base_url}/api/movies/{year}/{page}"
        headers = {"Authorization": f"Bearer {self.token.bearer}"}
        
        try:
            response = self.session.get(movies_url, headers=headers, timeout=10)
            
            if response.status_code == 404:
                # Year or page not found
                return []
            
            response.raise_for_status()
            
            # The server serves files, so we need to parse JSON if it's JSON
            content_type = response.headers.get('content-type', '')
            if 'application/json' in content_type:
                return response.json()
            else:
                # Assume it's a JSON file being served
                try:
                    return response.json()
                except json.JSONDecodeError:
                    return []
                    
        except RequestException as e:
            raise Exception(f"Failed to get movies for year {year}, page {page}: {e}")
    
    def count_movies(self, year: int):
        """
        Count total movies for a given year.
        
        Input:
            year: The year to count movies for
            
        Returns:
            Total number of movies for the year
        """
        total_count = 0
        page = 1
        
        while True:
            try:
                movies = self.get_movies_page(year, page)
                if not movies:
                    break
                
                total_count += len(movies)
                
                # if the movies is less than 10
                if len(movies) < 10:
                    break
                    
                page += 1
                
            except Exception as e:
                if "404" in str(e) or "not found" in str(e).lower():
                    break
                raise
        
        return total_count


def parse_arguments():
    # method to parse the command line arguments
    parser = argparse.ArgumentParser(
        description="Query movie database for film counts by year",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
                %(prog)s 1999                    # get movie count for one year
                %(prog)s 1999 2000 20001         # get movie count for multiple years
                %(prog)s --server localhost:8080 1999  """)
    
    parser.add_argument(
        'years',
        nargs='+',
        type=int,
        help='Year(s) for which the movie count has to be obtained'
    )
    
    parser.add_argument(
        '--server',
        default='http://localhost:8080',
        help='Server URL (default: http://localhost:8080)'
    )
    
    parser.add_argument(
        '--username',
        default='username',
        help='Username for authentication (default: username)'
    )
    
    parser.add_argument(
        '--password',
        default='password',
        help='Password for authentication (default: password)'
    )
    
    parser.add_argument(
        '--timeout',
        type=int,
        default=10,
        help='Request timeout in seconds (default: 10)'
    )
    
    return parser.parse_args()


def main():
    # the main function of the application
    try:
        args = parse_arguments()
        present_year = datetime.now().year
        # Validate years
        for year in args.years:
            if year < 1800 or year > present_year:
                print(f"Invalid {year}", file=sys.stderr)
                sys.exit(1)

        
    
        client = MovieClient(
            base_url=args.server,
            username=args.username,
            password=args.password
        )
        
        
        print(f"Connecting to server: {args.server}")
        print(f"Querying years: {', '.join([str(year) for year in args.years])}")
        
        results = []
        for year in sorted(args.years):
            try:
                print(f"Querying year {year}...", end=' ', flush=True)
                
                count = client.count_movies(year)
                results.append((year, count))
                
                
                print(f"found {count} movies")
                
            except Exception as e:
                print(f"Error querying year {year}: {e}", file=sys.stderr)
                results.append((year, 0))
            except KeyboardInterrupt:
                print("\nOperation cancelled by user", file=sys.stderr)
                sys.exit(1)
        
        # Display the results
        
        print("\nResults:")
        print("-" * 20)
        
        for year, count in results:
            print(f"{year}: {count} movies")
    
    except KeyboardInterrupt:
        print("\nOperation cancelled by user", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()