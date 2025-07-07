import requests
import json
import time
from datetime import datetime

# Your working configuration
url = "https://api.tuesday.so/api/v1/leads/people/search"
headers = {
    'sec-ch-ua-platform': '"Windows"',
    'Authorization': 'Bearer eyJraWQiOiJ0cGFMN09ENEhaaWY1aCtJcWNJdDJ5OWdRR3ByMnpPbXZHU3R3eld5VzBFPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiIwMDk2YTA5ZC05NzUyLTRkMjEtYTI0Yy0zZmM5YzE1Njg3MGMiLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAudXMtZWFzdC0xLmFtYXpvbmF3cy5jb21cL3VzLWVhc3QtMV8yN1M4M0dycnAiLCJ2ZXJzaW9uIjoyLCJjbGllbnRfaWQiOiI3YzludGVmZW1uNnVudjc4bzcxcnZ2Nm9jOCIsIm9yaWdpbl9qdGkiOiJmNWQ4ZTJjZi1jN2U1LTQyMWItOWJiYy1iYzFjNzFhNzg3MjciLCJ0b2tlbl91c2UiOiJhY2Nlc3MiLCJzY29wZSI6ImF3cy5jb2duaXRvLnNpZ25pbi51c2VyLmFkbWluIG9wZW5pZCBwcm9maWxlIGVtYWlsIiwiYXV0aF90aW1lIjoxNzUxMjYwOTU1LCJleHAiOjE3NTE5MDQzNjEsImlhdCI6MTc1MTg2MTE2MSwianRpIjoiM2UxZWQ2NTctMzM3Zi00NTdmLTk1YWEtZTRlNGIyMTlmMzU2IiwidXNlcm5hbWUiOiJnb29nbGVfMTEyNjM0Mzk5MDEyMzQ3OTE5NjA2In0.fBr-MnGYVJI3Qw-ifeEJPZhYMMXUT9RuAzIk7Iza2-lGw6_H6u9W2d8YyAFxA_zXNsuNATe_mqWp6GRUqYemFYI4wBuqmtoMzZQ6AwyE32P9IIBftZF3JbPxNrWjg2qA0IqcV17mPAc7gPFLuOs9I6SEXEfvfPTmH49tzAlnW_GuNd1GPEcE2OAoWfUcCZWhZAlfcKw4SdITP_fknQOmJp0MKe-mFINnugQG9Uah4q5O8nmJsMVhveUQbvxT1KbFqoYHSQsCbaMkYI7u-WQP_ysrPV6_QwfaAmhyhD9K-wFBFY5Us_dZxRv_BsU5QRoqJK9gLdR0LxJVpo4BVlIpsQ',
    'workspace_id': 'ws19g6pmcf2c7jp',
    'Referer': '',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    'Content-Type': 'application/json'
}

def scrape_and_print(start_page=1, end_page=100):
    """
    Scrape data from start_page to end_page and print the results,
    along with the time between requests in minutes and seconds.
    """
    total_records = 0
    
    # Track the start time
    start_time = time.time()

    for page in range(start_page, end_page + 1):
        print(f"Scraping page {page}...")
        
        # Your working payload
        payload = json.dumps({
            "page": page,
            "per_page": 200,
            "apply_sheet_filter": True
        })
        
        try:
            # Track the request start time
            request_start_time = time.time()

            # Your working request
            response = requests.request("POST", url, headers=headers, data=payload)

            print(f"Page {page} - Status Code: {response.status_code}")

            if response.status_code in [200, 201]:
                # Parse the response
                data = response.json()

                # Print response structure for first page
                if page == start_page:
                    print(f"Response keys: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")
                    print(f"Response sample: {str(data)[:200]}...")

                # Print fetched records for each page
                if data and 'data' in data and 'people' in data['data']:
                    people = data['data']['people']

                    if people:  # If there are people records
                        print(f"Page {page} - Fetched {len(people)} records.")
                        total_records += len(people)
                    else:
                        print(f"Page {page} - No people found in response")
                else:
                    print(f"Page {page} - Unexpected data structure")
                    print(f"Data keys: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")

            else:
                print(f"Page {page} - Error: {response.status_code}")
                print(f"Response: {response.text}")

            # Calculate time taken for this request and print
            request_end_time = time.time()
            elapsed_time = request_end_time - request_start_time
            elapsed_minutes = int(elapsed_time // 60)
            elapsed_seconds = int(elapsed_time % 60)
            print(f"Time taken for page {page}: {elapsed_minutes}m {elapsed_seconds}s")
        
        except Exception as e:
            print(f"Page {page} - Exception: {str(e)}")
        
        # Small delay to be respectful
        time.sleep(0.5)

    # Calculate the overall time taken
    end_time = time.time()
    total_elapsed_time = end_time - start_time
    total_minutes = int(total_elapsed_time // 60)
    total_seconds = int(total_elapsed_time % 60)

    print(f"\nScraping completed!")
    print(f"Total records fetched: {total_records}")
    print(f"Total time taken: {total_minutes}m {total_seconds}s")

if __name__ == "__main__":
    # Configuration
    START_PAGE = 63800
    END_PAGE = 64000

    print(f"Starting scrape from page {START_PAGE} to {END_PAGE}")
    scrape_and_print(START_PAGE, END_PAGE)
