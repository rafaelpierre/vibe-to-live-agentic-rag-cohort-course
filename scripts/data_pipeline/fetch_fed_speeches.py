"""
Federal Reserve Speeches and Testimony Scraper

This script:
1. Fetches the RSS feed from federalreserve.gov
2. Parses each speech/testimony URL
3. Scrapes the full text content
4. Saves to JSONL format with metadata

Usage:
    uv run python fetch_fed_speeches.py [--limit N] [--output PATH]
"""

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET

import httpx
from bs4 import BeautifulSoup

RSS_FEED_URL = "https://www.federalreserve.gov/feeds/speeches_and_testimony.xml"
DEFAULT_OUTPUT_DIR = Path(__file__).parent.parent.parent / "data" / "fed_speeches"


def fetch_rss_feed(url: str = RSS_FEED_URL) -> str:
    """
    Fetch the RSS feed content.

    Args:
        url: RSS feed URL

    Returns:
        RSS XML content as string
    """
    print(f"📡 Fetching RSS feed from {url}...")

    try:
        response = httpx.get(url, follow_redirects=True, timeout=30.0)
        response.raise_for_status()
        print(f"✅ RSS feed fetched successfully ({len(response.text)} bytes)")
        return response.text
    except httpx.HTTPError as e:
        print(f"❌ Error fetching RSS feed: {e}")
        sys.exit(1)


def parse_rss_feed(xml_content: str) -> list[dict[str, Any]]:
    """
    Parse RSS feed and extract item metadata.

    Args:
        xml_content: RSS XML content

    Returns:
        List of speech metadata dictionaries
    """
    print("🔍 Parsing RSS feed...")

    root = ET.fromstring(xml_content)
    items = []

    for item in root.findall(".//item"):
        title_elem = item.find("title")
        link_elem = item.find("link")
        desc_elem = item.find("description")
        category_elem = item.find("category")
        pubdate_elem = item.find("pubDate")

        if title_elem is None or link_elem is None:
            continue

        title = title_elem.text.strip() if title_elem.text else ""
        url = link_elem.text.strip() if link_elem.text else ""

        # Parse title to extract author and subject
        # Format is usually: "Author, Subject"
        parts = title.split(",", 1)
        author = parts[0].strip() if len(parts) > 0 else ""
        subject = parts[1].strip() if len(parts) > 1 else ""

        items.append(
            {
                "title": title,
                "url": url,
                "author": author,
                "subject": subject,
                "description": desc_elem.text.strip()
                if desc_elem is not None and desc_elem.text
                else "",
                "category": category_elem.text.strip()
                if category_elem is not None and category_elem.text
                else "",
                "pub_date": pubdate_elem.text.strip()
                if pubdate_elem is not None and pubdate_elem.text
                else "",
            }
        )

    print(f"✅ Found {len(items)} speeches/testimonies")
    return items


def scrape_speech_content(url: str) -> str | None:
    """
    Scrape the full text content from a speech URL.

    Args:
        url: Speech URL

    Returns:
        Full text content or None if failed
    """
    try:
        response = httpx.get(url, follow_redirects=True, timeout=30.0)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "lxml")

        # The main content is typically in a div with class "col-xs-12 col-sm-8 col-md-8"
        # or in the article tag
        content_div = soup.find("div", class_="col-xs-12 col-sm-8 col-md-8")
        if not content_div:
            content_div = soup.find("article")

        if not content_div:
            # Fallback: try to find the main content area
            content_div = soup.find("div", id="content")

        if not content_div:
            print(f"  ⚠️  Could not find content div for {url}")
            return None

        # Extract all paragraph text
        paragraphs = content_div.find_all("p")
        text_content = "\n\n".join(
            p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)
        )

        # Clean up extra whitespace
        text_content = re.sub(r"\n{3,}", "\n\n", text_content)
        text_content = re.sub(r" {2,}", " ", text_content)

        return text_content.strip()

    except httpx.HTTPError as e:
        print(f"  ❌ HTTP error scraping {url}: {e}")
        return None
    except Exception as e:
        print(f"  ❌ Error scraping {url}: {e}")
        return None


def save_to_jsonl(speeches: list[dict[str, Any]], output_path: Path) -> None:
    """
    Save speeches to JSONL file.

    Args:
        speeches: List of speech dictionaries
        output_path: Output file path
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        for speech in speeches:
            f.write(json.dumps(speech, ensure_ascii=False) + "\n")

    print(f"✅ Saved {len(speeches)} speeches to {output_path}")


def save_metadata(speeches: list[dict[str, Any]], output_dir: Path) -> None:
    """
    Save summary metadata to JSON file.

    Args:
        speeches: List of speech dictionaries
        output_dir: Output directory
    """
    metadata = {
        "total_speeches": len(speeches),
        "scraped_at": datetime.now(timezone.utc).isoformat(),
        "source": RSS_FEED_URL,
        "authors": sorted(set(s["author"] for s in speeches if s.get("author"))),
        "date_range": {
            "earliest": min(
                (s["pub_date"] for s in speeches if s.get("pub_date")), default=None
            ),
            "latest": max(
                (s["pub_date"] for s in speeches if s.get("pub_date")), default=None
            ),
        },
    }

    metadata_path = output_dir / "metadata.json"
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

    print(f"✅ Saved metadata to {metadata_path}")


def main():
    """Main entry point for the scraper."""
    parser = argparse.ArgumentParser(
        description="Scrape Federal Reserve speeches and testimony"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Limit number of speeches to scrape (default: all)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help=f"Output directory (default: {DEFAULT_OUTPUT_DIR})",
    )

    args = parser.parse_args()

    print("🏦 Federal Reserve Speeches Scraper")
    print("=" * 60)

    # Fetch and parse RSS feed
    rss_content = fetch_rss_feed()
    items = parse_rss_feed(rss_content)

    # Limit if specified
    if args.limit:
        items = items[: args.limit]
        print(f"📊 Limiting to {args.limit} speeches")

    # Scrape each speech
    print(f"\n📝 Scraping {len(items)} speeches...")
    speeches = []

    for i, item in enumerate(items, 1):
        print(f"\n[{i}/{len(items)}] {item['title']}")
        print(f"  URL: {item['url']}")

        content = scrape_speech_content(item["url"])

        if content:
            speech = {
                **item,
                "content": content,
                "content_length": len(content),
                "scraped_at": datetime.now(timezone.utc).isoformat(),
            }
            speeches.append(speech)
            print(f"  ✅ Scraped ({len(content)} characters)")
        else:
            print(f"  ⚠️  Skipped (no content)")

    # Save results
    print(f"\n💾 Saving results...")
    output_file = args.output / "speeches.jsonl"
    save_to_jsonl(speeches, output_file)
    save_metadata(speeches, args.output)

    # Summary
    print("\n" + "=" * 60)
    print(f"✅ Scraping complete!")
    print(f"   Total speeches: {len(speeches)}")
    print(f"   Successfully scraped: {len([s for s in speeches if s.get('content')])}")
    print(f"   Output: {output_file}")
    print(f"   Metadata: {args.output / 'metadata.json'}")

    # Show sample
    if speeches:
        print(f"\n📄 Sample (first speech):")
        sample = speeches[0]
        print(f"   Title: {sample['title']}")
        print(f"   Author: {sample['author']}")
        print(f"   Date: {sample['pub_date']}")
        print(f"   Content: {sample['content'][:200]}...")


if __name__ == "__main__":
    main()
