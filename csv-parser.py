import os

# Path to the directory containing CSV files and images
dir_path = 'meets'
image_dir = 'images'

# HTML content to be constructed directly
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Results</title>
    <link rel="stylesheet" type="text/css" href="css/reset.css"> 
    <link rel="stylesheet" href="css/style.css">
    <script>
        window.addEventListener('scroll', function() {
            const button = document.getElementById('back-to-top');
            if (window.pageYOffset > 300) {
                button.style.display = 'block';
            } else {
                button.style.display = 'none';
            }
        });

        function scrollToTop() {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
    </script>
</head>
<body>
    <footer>
        <img src="images/athletic_logo.png" alt="Athletic.net Logo" class="footer-logo">
        <a href="index.html" class="footer-button">Home Page</a>
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
        <h1>All 2024 Event Summaries</h1>
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
                
                # Define the path to the image using the updated naming convention IMG_{athlete_id}.jpg
                image_path = os.path.join(image_dir, f"IMG_{athlete_id}.jpg")

                # Check if the image exists in the images folder; if not, use a default image
                if os.path.exists(image_path):
                    image_src = f"images/IMG_{athlete_id}.jpg"
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
                    <td data-label="Profile"><img src="{image_src}" alt="Profile Picture of {result[2]}"></td>
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
    <button id="back-to-top" onclick="scrollToTop()">Back to Top</button>
</body>
</html>
"""

# Save the HTML content to a file
html_file_path = 'results.html'
with open(html_file_path, 'w') as file:
    file.write(html_content)

print(f'HTML file generated: {html_file_path}')
