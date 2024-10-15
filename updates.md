# Version 1.0.3 - 15th October 2024
## Updates & Enhancements

### 1. New Supplier Management Route
- **Added a new route for creating suppliers**
  - **Endpoint**: `/create-new-supplier`
  - **Method**: `POST`, `GET`
  - **Permissions**: Accessible only to users with the `can_manage_suppliers` permission.
  - **Functionality**: Enables authorized users to add a new supplier, including details like contact information, type, country, address, and payment terms.
  - **Improvements**: Enhanced success and error handling to provide clear feedback to users.

### 2. Product Management Enhancements
- **Implemented dynamic product filters**:
  - **New Feature**: Ability to filter products by brand and type directly via the frontend.
  - **Backend Improvements**: Refined handling of search queries to allow more precise and accurate searches.
  - **Route Adjustments**: Updated product search endpoints to process queries by name and type, avoiding reliance on ID lookups.
- **New Route for Product Actions**:
  - **Endpoint**: `/change-product-status`
  - **Method**: `POST`
  - **Functionality**: Toggle product status between 'Active' and 'Inactive'. Includes improved error handling and user feedback.

### 3. Dark Mode Toggle Feature
- **Enhanced dark mode functionality**:
  - **Default Setting**: Dark mode is now set as the default UI mode.
  - **User Control**: Users can switch between dark and light modes, with preferences saved using `localStorage` to ensure a seamless experience across sessions.
  - **CSS Adjustments**: Updated styles to enhance readability and contrast in dark mode, aligning color schemes for better visual consistency.

### 4. UI & Layout Improvements
- **Refined Color Palette**:
  - Adjusted color schemes throughout the application, especially for dark mode, to improve visual appeal and consistency.
  - Enhanced contrast for improved readability on darker backgrounds.
- **Form Layouts**:
  - Improved form designs for cleaner and more professional data entry.
  - Example: Supplier creation form now displays input fields in pairs, leading to a more organized and balanced layout.
- **Table Adjustments**:
  - Refined product information tables to allow for more efficient filtering and sorting.
  - Added new action buttons for generating QR codes and viewing product details, directly accessible from the product management dashboard.

### 5. Error Handling & Feedback
- **Improved user feedback for various actions**:
  - **Flash Messages**: Added more descriptive and user-friendly messages for actions such as adding new suppliers and changing product status.
  - **Error Logging**: Enhanced backend logging for easier debugging and faster response to issues.
- **Code Improvements**:
  - **Backend Refactoring**: Optimized various routes to streamline data processing and reduce response times. Functions were refactored to increase maintainability and readability.
  - **JavaScript Enhancements**: Improved event handling for UI interactions (e.g., toggling dark mode, applying product filters). Simplified the logic for dark mode detection and switching, reducing code redundancy.
