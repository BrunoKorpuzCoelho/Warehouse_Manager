Version 1.0.3 - 15th October 2024
Updates & Enhancements
1. New Supplier Management Route
Added a new route for creating suppliers:
Endpoint: /create-new-supplier
Method: POST, GET
Permissions: Only accessible to users with the can_manage_suppliers permission.
Functionality: Allows authorized users to add a new supplier, including contact details, type, country, address, and payment terms. Success and error handling were enhanced to provide clear feedback.
2. Product Management Enhancements
Implemented dynamic filters for products:
New Feature: Ability to filter products by brand and product type directly via the frontend.
Improvement: Refined backend handling of product search queries to support more precise searches.
Route Adjustments: Updated product search endpoints to handle queries by name and type, avoiding lookup by IDs.
New Route for Product Actions:
Endpoint: /change-product-status
Method: POST
Functionality: Allows toggling the status of a product between 'Active' and 'Inactive' with improved error handling and user feedback.
3. Dark Mode Toggle Feature
Enhanced the dark mode functionality:
Default Setting: Dark mode is now set as the default user interface mode.
User Control: Users can still toggle between dark and light modes. Their preference is saved using localStorage, ensuring a seamless experience across sessions.
CSS Adjustments: Updated styles to improve readability and contrast in dark mode, and aligned color schemes for better consistency.
4. UI & Layout Improvements
Refined Color Palette:
Adjusted various color schemes across the application, particularly in dark mode, to improve visual appeal and consistency.
Enhanced contrast for better readability, especially on darker backgrounds.
Form Layouts:
Improved form layouts to ensure cleaner and more professional data entry screens.
Example: Supplier creation form now displays input fields in pairs, allowing for a more organized and balanced interface.
Table Adjustments:
Refined the display of product information tables to accommodate more efficient filtering and sorting.
Added new action buttons for generating QR codes and viewing product details, accessible directly from the product management dashboard.
5. Error Handling & Feedback
Improved user feedback for various actions:
Flash Messages: Added more descriptive and user-friendly flash messages for actions like adding new suppliers and changing product status.
Error Logging: Enhanced backend error logging for easier debugging and faster response to issues.
Code Improvements
Backend Refactoring:
Optimized various backend routes to streamline data processing and reduce response times.
Refactored certain functions to increase code maintainability and readability.
JavaScript Enhancements:
Improved event handling for UI interactions, such as toggling dark mode and applying filters on product lists.
Simplified the logic for dark mode detection and switching, reducing code redundancy.
