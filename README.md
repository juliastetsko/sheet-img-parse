# Image Size Fetcher

This script fetches the sizes of images from URLs stored in a Google Sheet and updates the corresponding cells in the sheet with the sizes.

## Prerequisites

Before running the script, make sure you have the following:

- Python 3.7 or higher installed
- Required Python packages installed (`aiohttp`, `gspread`, `oauth2client`)
- Google Cloud project with access to Google Sheets API enabled
- Service account JSON key file with appropriate permissions
- Google Sheet with the URLs of images to fetch sizes from

## Setup

1. Clone the repository or download the script 
  ```bash
    git clone git@github.com:juliastetsko/sheet-img-parse.git
   ```
2. Install required Python packages using `pip install -r requirements.txt`.
3. Set up a service account and generate a JSON key file. 
4. Set environment variables:
   - `GSPREAD_ACCOUNT_JSON`: Path to the service account JSON key file.
   - `GOOGLE_SHEET_LINK`: Link to the Google Sheet containing the URLs.

## Configuration

- `WORKSHEET_TITLE`: Title of the worksheet within the Google Sheet.
- `BATCH_SIZE`: Number of URLs to process in each batch.

## Usage

The script fetches the image sizes in batches, updating the corresponding cells in the Google Sheet.


