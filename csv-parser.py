import os

# Path to the directory containing CSV files and images
dir_path = 'meets'
image_dir = 'images/athletes'

# HTML content to be constructed directly
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Event Summaries</title>
    <link rel="icon" href="images/favicon.ico" type="image/x-icon">
    <link rel="stylesheet" type="text/css" href="css/reset.css"> 
    <link rel="stylesheet" href="css/style.css">
    <script>
        // Handle scroll events and back-to-top button
        window.addEventListener('scroll', function() {
            const button = document.getElementById('back-to-top');
            const modal = document.getElementById('image-modal');
            // Show or hide the back-to-top button based on scroll position if modal is not open
            if (window.pageYOffset > 300 && modal.style.display !== 'block') {
                button.style.display = 'block';
            } else {
                button.style.display = 'none';
            }
        });

        // Scroll to top function
        function scrollToTop() {
            const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
            if (prefersReducedMotion) {
                window.scrollTo({ top: 0 });
            } else {
                window.scrollTo({ top: 0, behavior: 'smooth' });
            }
        }

        // Toggle modal visibility
        function toggleModal(imageSrc, altText) {
            const modal = document.getElementById('image-modal');
            const modalImg = document.getElementById('modal-img');
            const modalCaption = document.getElementById('modal-caption');
            const backToTopButton = document.getElementById('back-to-top');

            modal.style.display = 'block';
            modalImg.src = imageSrc;
            modalCaption.textContent = altText;

            // Hide the back-to-top button when the modal is open
            backToTopButton.style.display = 'none';

            // Add event listener for keydown to close modal on "Escape"
            document.addEventListener('keydown', handleModalKeydown);
        }

        // Close the modal
        function closeModal() {
            const modal = document.getElementById('image-modal');
            modal.style.display = 'none';

            // Re-enable the back-to-top button based on scroll position
            const button = document.getElementById('back-to-top');
            if (window.pageYOffset > 300) {
                button.style.display = 'block';
            }

            // Remove keydown event listener when modal is closed
            document.removeEventListener('keydown', handleModalKeydown);
        }

        // Handle keydown event to close modal when "Escape" is pressed
        function handleModalKeydown(event) {
            if (event.key === 'Escape') {
                closeModal();
            }
        }

        // Close the modal when clicking outside the image
        window.onclick = function(event) {
            const modal = document.getElementById('image-modal');
            if (event.target === modal) {
                closeModal();
            }
        }

        // Handle keydown event for profile images (open modal on Enter)
        function handleImageKeydown(event, imageSrc, altText) {
            if (event.key === 'Enter') {
                toggleModal(imageSrc, altText);
            }
        }

        // Toggle between dark and light mode
        function toggleDarkMode() {
            const root = document.documentElement;  // Refers to the <html> element
            const currentTheme = root.getAttribute("data-theme");
            
            // Toggle between light and dark
            const newTheme = currentTheme === "dark" ? "light" : "dark";
            root.setAttribute("data-theme", newTheme);
            console.log('Theme switched to:', newTheme); // Debugging line to verify it's working
        }
    </script>
</head>
<body>
    <!-- Image Modal -->
    <div id="image-modal" class="modal">
        <img class="modal-content" id="modal-img" alt="Profile Pic Fullscreen View">
        <div id="modal-caption"></div>
    </div>

    <!-- It's weird to have a footer at the top but it turns into a navbar on small viewports -->
    <footer>
        <img src="images/athletic_logo.png" alt="Athletic.net Logo" class="footer-logo">
        <a href="index.html" class="footer-button" tabindex="0">Home Page</a>
        <button class="footer-button" onclick="toggleDarkMode()" tabindex="0">Change Mode</button>
    </footer>
    <main>
        <nav class="event-list">
            <ul>
"""

# Loop through each file in the directory
event_count = 0
for filename in os.listdir(dir_path):
    if filename.endswith('.csv'):
        event_count += 1
        file_path = os.path.join(dir_path, filename)
        
        # Extract event name from the filename (assuming the filename has meaningful event info)
        event_name = os.path.splitext(filename)[0].replace('_', ' ')

        # Add the event to the list of event names for navigation
        html_content += f'<li><a href="#event-{event_count}" class="event-link">{event_name}</a></li>'

html_content += """
            </ul>
        </nav>
        <br>
        <h1>All 2024 Event Summaries</h1>
        <br>
"""

# Resetting the event count for sections
event_count = 0

# Medal icons for the top 3 teams
medals = ["&#129351;", "&#129352;", "&#129353;"]  # Gold, Silver, Bronze

# Loop through each file again to create event sections
for filename in os.listdir(dir_path):
    if filename.endswith('.csv'):
        event_count += 1
        file_path = os.path.join(dir_path, filename)
        
        # Extract event name from the filename (assuming the filename has meaningful event info)
        event_name = os.path.splitext(filename)[0].replace('_', ' ')

        # Reading the file manually as it contains inconsistent formatting
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # Variables to store team scores and individual results
        team_scores = []
        individual_results = []

        # Flags to detect sections
        in_team_scores = False
        in_individual_results = False

        # Loop through lines to capture the relevant data
        for line in lines:
            line = line.strip()

            if line.startswith("Place,Team,Score"):
                in_team_scores = True
                in_individual_results = False
                continue
            elif line.startswith("Place,Grade,Name,Athlete Link,Time,Team,Team Link,Profile Pic"):
                in_team_scores = False
                in_individual_results = True
                continue
            elif not line:  # Ignore empty lines
                continue

            if in_team_scores and len(team_scores) < 3:
                team_scores.append(line.split(','))
            elif in_individual_results and len(individual_results) < 3:
                individual_results.append(line.split(','))

        # Add a new section for each event
        html_content += f"""
        <div class="spacer" id="spacer-{event_count}"></div>
        <section id="event-{event_count}" class="event">
        <br>
            <h2>{event_name}</h2>
            <h3>Team Scores</h3>
            <br>
            <div class="podium">
        """

        # Add team scores to the HTML content with medal icons
        for idx, score in enumerate(team_scores):
            medal_icon = medals[idx] if idx < 3 else ""
            position_class = "first-place" if idx == 0 else "second-place" if idx == 1 else "third-place"
            html_content += f"""
            <div class="{position_class}">
                <p><b>{medal_icon} {score[1]}</b></p>
                <p>Score: {score[2]}</p>
            </div>
            """

        # Closing the podium div
        html_content += """
            </div>
            <br>
            <h3>Top 3 Results</h3>
            <br>
            <table class="athlete-table">
                <thead>
                    <tr>
                        <th>Place</th>
                        <th>Grade</th>
                        <th>Name</th>
                        <th>Time</th>
                        <th>Team</th>
                        <th>Profile</th>
                    </tr>
                </thead>
                <tbody>
        """

        # Create the HTML content for athletes in a table format
        for result in individual_results:
            if len(result) >= 7:  # Ensure all required data is present
                athlete_link = result[3]
                
                # Extract athlete ID from the link (e.g., https://www.athletic.net/athlete/19229177/cross-country)
                athlete_id = athlete_link.split('/')[-2]
                
                # Define the path to the image using the updated naming convention {athlete_id}.jpg
                image_path = os.path.join(image_dir, f"{athlete_id}.jpg")

                # Check if the image exists in the images folder; if not, use a default image
                if os.path.exists(image_path):
                    image_src = f"images/athletes/{athlete_id}.jpg"
                else:
                    image_src = f"images/default.jpg"
                
                # Add athlete result to the HTML table
                html_content += f"""
                <tr>
                    <td data-label="Place">{result[0]}</td>
                    <td data-label="Grade">{result[1]}</td>
                    <td data-label="Name"><a href="{athlete_link}" target="_blank">{result[2]}</a></td>
                    <td data-label="Time">{result[4]}</td>
                    <td data-label="Team">{result[5]}</td>
                    <td data-label="Profile">
                        <!-- Add tabindex and handleImageKeydown for keyboard accessibility -->
                        <img src="{image_src}" alt="Profile Picture of {result[2]}" 
                             onclick="toggleModal('{image_src}', '{result[2]}')" 
                             onkeydown="handleImageKeydown(event, '{image_src}', '{result[2]}')" tabindex="0">
                    </td>
                </tr>
                """

        # Closing the table and event section
        html_content += """
                </tbody>
            </table>
        </section>
        """

# Closing the main and other HTML tags
html_content += """
    </main>
    <button id="back-to-top" onclick="scrollToTop()" tabindex="0">Back to Top</button>
</body>
</html>
"""

# Save the HTML content to a file
html_file_path = 'results.html'
with open(html_file_path, 'w') as file:
    file.write(html_content)

print(f'HTML file generated: {html_file_path}')