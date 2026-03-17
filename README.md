# Shopify × Sketchfab 3D Embed Sync

## What it does
A Python script that automatically connects Shopify products to 3D model embeds from Sketchfab, storing the embed URL as a product metafield.

## The problem it solves
In retail, the ability to touch and feel a product drives purchase decisions.
This script explores how embedded 3D models on product pages could bridge that gap
for online shoppers - automating what would otherwise be a manual, model-by-model setup process.

## How it works
1. Fetches all products from a Shopify store via the Admin API
2. Searches Sketchfab for a 3D model matching the product title
3. Writes the embed URL back to Shopify as a custom metafield

## Limitations
Sketchfab's library contains mostly hobbyist and artistic models — matches are approximate rather than exact product replicas. This limitation will addressed in v2.

## Setup
1. Clone the repo
2. Install dependencies: `pip install requests python-dotenv`
3. Create a `.env` file based on `.env.example`
4. Run: `python main.py`

## What's next — v2
V2 will replace the Sketchfab search with AI image generation - using each product's name
and description to generate a relevant visual automatically, making the tool viable
for any store regardless of what 3D models exist on Sketchfab.

## Stack
- Python
- Shopify Admin API
- Sketchfab Data API v3
