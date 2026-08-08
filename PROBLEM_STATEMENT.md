# 📌 Problem Statement — Inventory & Sales Management System

## Background

Small and medium retail stores — electronics shops, accessory outlets, general stores — largely manage their inventory and billing manually, using notebooks, WhatsApp messages, or scattered spreadsheets. As the number of products and daily transactions grows, this manual approach becomes unreliable and error-prone.

## Problem

Retailers currently face the following issues in their day-to-day operations:

- No centralized record of products, their prices, and available stock
- Stock levels are not updated in real time when a sale is made, leading to overselling or stockouts
- Bills are calculated manually, including discounts and GST, resulting in frequent errors
- No easy way to identify which products are running low and need restocking
- No visibility into how much inventory value or stock is held per product category
- No quick way to search for a specific product among a growing catalog
- No invoice or transaction proof generated for sales made
- Records are not saved reliably, so data is lost between sessions
- No way to track which products were sold on a given day

## What Is Required

Design and build a command-line application that a small retail store can use to manage its inventory and sales operations. The application must:

1. Allow adding new products with a unique ID, name, category, price, and initial stock
2. Allow updating/restocking the quantity of existing products
3. Allow selling products, automatically validating available stock and applying a discount percentage and GST
4. Automatically reduce stock quantity when a sale is made
5. Allow searching for a product by its ID or name
6. Generate a report of products whose stock has fallen below a defined threshold
7. Generate a category-wise summary showing total products, total stock, and total inventory value
8. Display all unique product categories added so far
9. Display all unique products sold on the current day
10. Generate a formatted invoice for a completed sale, including subtotal, discount, GST, and grand total
11. Save all data (inventory, sales, categories) so it persists between program runs, and reload it automatically on the next run
12. Handle invalid or unexpected user input gracefully, without the program crashing
