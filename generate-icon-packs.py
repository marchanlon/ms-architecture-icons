#!/usr/bin/env python3
"""
Generate icon pack JSON files from SVG files.

This script iterates through all .svg files in the icons folder and creates
a JSON output file (azure-icon-pack.json) with each SVG's content (without
the opening and closing svg tags).
"""

import json
import re
from pathlib import Path


def extract_svg_body(svg_content):
    """
    Extract the content of an SVG file, removing the opening and closing <svg> tags.
    
    Args:
        svg_content (str): The full SVG file content
        
    Returns:
        str: The SVG body content without outer svg tags
    """
    # Pattern to match opening <svg ...> tag and extract everything after it
    # and pattern to match closing </svg> tag
    pattern = r'<svg[^>]*>(.*)</svg>'
    match = re.search(pattern, svg_content, re.DOTALL | re.IGNORECASE)
    
    if match:
        return match.group(1).strip()
    
    # If no match, return empty string
    return ""


def generate_icon_pack(icons_dir="icons", output_file="azure-icon-pack.json", prefix="azure"):
    """
    Generate an icon pack JSON file from all SVG files in the icons directory.
    
    Args:
        icons_dir (str): Path to the icons directory (default: "icons")
        output_file (str): Output JSON filename (default: "azure-icon-pack.json")
    """
    icons_path = Path(icons_dir)
    
    if not icons_path.exists():
        print(f"Error: {icons_dir} directory not found")
        return
    
    # Find all SVG files recursively
    svg_files = sorted(icons_path.rglob("*.svg"))
    
    if not svg_files:
        print(f"No SVG files found in {icons_dir}")
        return
    
    icon_pack = {
        "prefix": prefix,
        "icons": {}
    }
    
    for svg_file in svg_files:
        try:
            # Read the SVG file
            with open(svg_file, 'r', encoding='utf-8') as f:
                svg_content = f.read()
            
            # Extract the body (content without opening/closing svg tags)
            svg_body = extract_svg_body(svg_content)
            
            # Extract simplified file key from filename
            # "00028-icon-service-Batch-AI.svg" -> "Batch-AI"
            file_key = svg_file.name.lower()

            # Remove leading numbers and "icon-service-" if present
            match = re.match(r'^(\d+-icon-service-)(.+)\.svg$', file_key)
            if match:
                file_key = match.group(2)
            # else, keep file_key as is
            
            # Keep only letters, numbers, and hyphens
            file_key = re.sub(r'[^a-zA-Z0-9-]', '', file_key)
            
            # Add to icon pack
            icon_pack["icons"][file_key] = {
                "body": svg_body
            }
            
            print(f"✓ Processed: {file_key}")
        
        except Exception as e:
            print(f"✗ Error processing {svg_file}: {e}")
    
    # Write the output JSON file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(icon_pack, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Successfully generated {output_file}")
    print(f"  Total icons: {len(icon_pack['icons'])}")

if __name__ == "__main__":
    generate_icon_pack(icons_dir="icons/Azure_Public_Service_Icons", output_file="packs/azure-icon-pack.json", prefix="azure")
