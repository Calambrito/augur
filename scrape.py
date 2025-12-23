import requests
import csv
import time
from typing import List, Dict


class DhakaRestaurantScraper:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://serpapi.com/search"
        self.api_calls_made = 0
        self.max_api_calls = 250

        # Major Dhaka locations (17 total)
        self.locations = [
            "Gulshan",
            "Banani",
            "Baridhara",
            "Bashundhara",
            "Uttara",
            "Mirpur",
            "Dhanmondi",
            "Mohammadpur",
            "Badda",
            "Rampura",
            "Khilgaon",
            "Malibagh",
            "Old Dhaka",
            "Motijheel",
            "Tejgaon",
            "Farmgate",
            "Niketan"
        ]

        # Cuisine types (14 total)
        self.cuisines = [
            "Bengali",
            "Chinese",
            "Indian",
            "Thai",
            "Italian",
            "Korean",
            "Japanese",
            "Mexican",
            "BBQ",
            "Biryani/Kacchi",
            "Pizza",
            "Burger",
            "Fast Food",
            "Cafe"
        ]

    def search_restaurants(self, query: str, start: int = 0) -> Dict:
        """Make a single SerpAPI call"""
        if self.api_calls_made >= self.max_api_calls:
            return {}

        params = {
            "engine": "google_maps",
            "q": query,
            "ll": "@23.8103,90.4125,12z",
            "type": "search",
            "api_key": self.api_key,
            "start": start
        }

        try:
            response = requests.get(self.base_url, params=params)
            self.api_calls_made += 1
            print(f"  API calls: {self.api_calls_made}/{self.max_api_calls}", end="\r")
            return response.json()
        except Exception as e:
            print(f"\n  ⚠️ Error: {e}")
            return {}

    def extract_restaurant_data(self, result: Dict, cuisine: str, location: str) -> Dict:
        """Extract data from a single restaurant result"""
        return {
            "name": result.get("title", "N/A"),
            "rating": result.get("rating", "N/A"),
            "reviews": result.get("reviews", "N/A"),
            "cuisine": cuisine,
            "price": result.get("price", "N/A"),
            "location": location
        }

    def build_queries(self) -> List[tuple]:
        """Build all location × cuisine combinations"""
        queries = []
        
        # Generate: "{cuisine} restaurant in {location}, Dhaka"
        for location in self.locations:
            for cuisine in self.cuisines:
                query = f"{cuisine} restaurant in {location}, Dhaka"
                queries.append((query, cuisine, location))
        
        return queries

    def scrape_all_restaurants(self) -> List[Dict]:
        """Main scraping logic with smart query distribution"""
        all_restaurants = []
        seen_names = set()

        queries = self.build_queries()
        total_queries = len(queries)
        
        # Calculate pages per query based on API budget
        # We want to maximize coverage while staying under limit
        pages_per_query = max(1, self.max_api_calls // total_queries)
        
        print("=" * 70)
        print(f"📋 Total query combinations: {total_queries}")
        print(f"📄 Pages per query: {pages_per_query}")
        print(f"🔢 Estimated API calls: {total_queries * pages_per_query}")
        print(f"💰 Available API calls: {self.max_api_calls}")
        print("=" * 70)

        for idx, (query, cuisine, location) in enumerate(queries, 1):
            if self.api_calls_made >= self.max_api_calls:
                print("\n\n🛑 API quota exhausted. Stopping.")
                break

            print(f"\n[{idx}/{total_queries}] 🔍 {query}")

            # Fetch pages for this query
            for page in range(pages_per_query):
                if self.api_calls_made >= self.max_api_calls:
                    print("\n🛑 API quota exhausted mid-query.")
                    return all_restaurants

                data = self.search_restaurants(query, start=page * 20)
                
                if not data or "local_results" not in data:
                    break

                results = data["local_results"]
                new_count = 0

                for r in results:
                    restaurant = self.extract_restaurant_data(r, cuisine, location)
                    
                    # Avoid duplicates based on name
                    if restaurant["name"] not in seen_names:
                        seen_names.add(restaurant["name"])
                        all_restaurants.append(restaurant)
                        new_count += 1

                print(f"  ✓ Found {new_count} new restaurants (Total: {len(all_restaurants)})")

                # If we got fewer than 20 results, no point in fetching next page
                if len(results) < 20:
                    break

                time.sleep(1.0)  # Rate limiting

        return all_restaurants

    def save_to_csv(self, restaurants: List[Dict], filename="dhaka_restaurants_final.csv"):
        """Save results to CSV"""
        if not restaurants:
            print("\n⚠️ No data to save")
            return

        keys = ["name", "rating", "reviews", "cuisine", "price", "location"]

        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(restaurants)

        print(f"\n💾 Saved {len(restaurants)} restaurants to {filename}")

    def print_summary(self, restaurants: List[Dict]):
        """Print detailed summary statistics"""
        print("\n" + "=" * 70)
        print("📊 FINAL SUMMARY")
        print("=" * 70)
        print(f"API calls used: {self.api_calls_made}/{self.max_api_calls}")
        print(f"Total unique restaurants: {len(restaurants)}")
        
        # Location distribution
        location_counts = {}
        for r in restaurants:
            loc = r["location"]
            location_counts[loc] = location_counts.get(loc, 0) + 1
        
        print("\n📍 Top Locations:")
        for loc, count in sorted(location_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"  {loc}: {count} restaurants")
        
        # Cuisine distribution
        cuisine_counts = {}
        for r in restaurants:
            cui = r["cuisine"]
            cuisine_counts[cui] = cuisine_counts.get(cui, 0) + 1
        
        print("\n🍽️ Top Cuisines:")
        for cui, count in sorted(cuisine_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"  {cui}: {count} restaurants")
        
        # Rating distribution
        rated = [r for r in restaurants if r["rating"] != "N/A"]
        if rated:
            avg_rating = sum(float(r["rating"]) for r in rated) / len(rated)
            print(f"\n⭐ Average rating: {avg_rating:.2f} ({len(rated)} restaurants with ratings)")


def main():
    API_KEY = "699a6138e9160b67099517585d40af42ba9ce64bbd448fb5a9b219f161e67dbd"

    print("=" * 70)
    print("🍽️  DHAKA RESTAURANT SCRAPER - QUERY-BASED LOCATION")
    print("=" * 70)

    scraper = DhakaRestaurantScraper(API_KEY)
    
    # Run the scraper
    restaurants = scraper.scrape_all_restaurants()
    
    # Save results
    scraper.save_to_csv(restaurants)
    
    # Print summary
    scraper.print_summary(restaurants)
    
    print("\n" + "=" * 70)
    print("✅ COMPLETE!")
    print("=" * 70)


if __name__ == "__main__":
    main()