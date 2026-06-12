# Assignment 19

## Question

Simple Digital Counter and Theme Toggle App

Build a single-screen mobile application using React Native. The app functions as a digital counter that allows users to increment, decrement, and reset a number displayed on the screen. To make the app more interactive, it must also include a "Theme Toggle" button that switches the screen's background and text colors between a Light Mode and a Dark Mode.

Implementation Rules:

Core Layout: The application must use standard React Native components: View, Text, and TouchableOpacity (or Button). The counter UI should be perfectly centered on the screen.

State Management: Use the useState hook to manage two pieces of state: the current counter value (integer) and the active theme mode (boolean or string).

Counter Logic:
The counter should start at 0.
The "Increment" button must increase the count by 1.
The "Decrement" button must decrease the count by 1, but it should never let the counter go below 0 (prevent negative numbers).
The "Reset" button must bring the count back to 0.

Dynamic Styling:
Light Mode (Default): White background with dark text.
Dark Mode: Dark gray/black background with white text.
Clicking the "Toggle Theme" button should instantly swap these styles across the entire screen.

You must have the followings:
1. UI Layout and Component Structure
2. Counter State and Validation Logic
3. Dynamic Theme Toggling
4. Code Cleanliness and Best Practices
